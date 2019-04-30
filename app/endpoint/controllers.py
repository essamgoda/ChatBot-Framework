from bson import ObjectId
import json

from jinja2 import Template

from flask import Blueprint, request, abort
from app import app

from app.commons.logger import logger
from app.commons import build_response
from app.nlu.entity_extractor import EntityExtractor
from app.intents.models import Intent

from app.commons.redis_utils import r

from app.endpoint.utils import get_synonyms, SilentUndefined, split_sentence, call_api
from app.game.controllers import read_questions 

endpoint = Blueprint('api', __name__, url_prefix='/api')

# Loading ML Models at app startup
from app.nlu.classifiers.tf_intent_classifer import TfIntentClassifier

sentence_classifier = None
synonyms = None
entity_extraction = None

# token to verify that this bot is legit
verify_token = ''
# token to send messages through facebook messenger
access_token = ''

face_json={
    'currentNode': '',
    'complete': None,
    'context': {},
    'parameters': [],
    'extractedParameters': {},
    'speechResponse': '',
    'intent': {},
    'input': 'init_conversation',
    'missingParameters': []
    }
quick_replies_game = [
        {
        "content_type":"text",
        "title":"Play Game",
        "payload":"Let's Play Game ...",
        },
        {
        "content_type":"text",
        "title":"Ask Question",
        "payload":"Ask Question",
        }
    ]
#webhook
@endpoint.route('/webhook', methods=['GET'])
def webhook_verify():
    if request.args.get('hub.verify_token') == verify_token:
        return request.args.get('hub.challenge')
    return "Wrong verify token"

@endpoint.route('/webhook', methods=['POST'])
def webhook_action():
    request_json = request.get_json(silent=True)
    data = request_json
    print(data)
    for entry in data['entry']:
        messaging = entry['messaging']
        for message in messaging:
            if message.get('message'):

                user_id = message['sender']['id']
                user_details_url = "https://graph.facebook.com/v2.6/%s"%user_id
                user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':access_token}
                
                try:
                    user_details = call_api(user_details_url,"GET",'',user_details_params, True)
                    user_name=user_details['first_name']
                    userid=int(user_id)
                except Exception as e:
                    app.logger.warn("API call failed", e)
                
                if message['message'].get('text'):
                    msg=message['message']['text']

                    if message['message'].get('quick_reply'):
                        isCorrect=message['message']['quick_reply']['payload']
                        print(isCorrect,type(isCorrect))

                    if 'Play Game' in msg:
                        r.set(user_id+'_playing',1)
                        
                    if 'exit' in msg:
                        r.set(user_id+'_playing',0)
                        r.set(user_id+'_count',0)

                    if r.get(user_id+'_playing')=='1':
                        response = {
                            "access_token": access_token,
                            'recipient': {'id': user_id},
                            'message': {
                                'text':'',
                            }

                        }
                        r.incr(user_id+'_count')
                        count=int(r.get(user_id+'_count'))-1
                        questions=read_questions().get_json()

                        if len(questions)> count:
                            response['message']['text']=questions[count]['question']
                            answers=[]
                            for ans in questions[count]['Answers']:
                                a={
                                    'content_type':'text',
                                    'title':'',  
                                    'payload':''
                                    }
                                a['title']=ans['ans']
                                a['payload']=str(ans['isCorrect'])
                                answers.append(a)

                            if answers:
                                response['message']['quick_replies']=answers

                            msg='Play Game'
                        else:
                            r.set(user_id+'_playing',0)
                            r.set(user_id+'_count',0)
                            response['message']['text']='Thanks for playing...'
                       
                        print('/n',response)
                    else:
                        response = {
                                "access_token": access_token,
                                'recipient': {'id': user_id},
                                'message': {
                                    'text':'',
                                    'quick_replies':quick_replies_game
                                }

                            }
                        try:
                            global face_json
                            face_json['input']=msg
                            headers = {"Content-Type": "application/json"}
                            face_json = call_api(url='http://localhost:5000/api/v1',type="POST",headers=headers,parameters=face_json, is_json=True)
                            
                            for speechResponse in face_json['speechResponse']:
                                response['message']['text'] += speechResponse+'\n'
                        except Exception as e:
                            app.logger.warn("API call failed", e)
                       
                    if 'Play Game' in msg:
                        r.set(user_id+'_playing',1)
                    else:
                        r.set(user_id+'_playing',0)
                    
                elif message['message'].get('attachments'):
                    attachment_link = message["message"]["attachments"][0]["payload"]["url"]
                    
                    response = {
                            "access_token": access_token,
                            'recipient': {'id': user_id},
                            'message': {}
                        }
                    response['message']['text'] = "couldn't catch that..."

                else:
                    response = {
                        "access_token": access_token,
                        'recipient': {'id': user_id},
                        'message': {}
                    }
                    response['message']['text'] = "couldn't catch that..."


                headers = {"Content-Type": "application/json"}
                #r = requests.post('https://graph.facebook.com/v2.6/me/messages', params=params, headers=headers, json=response)
                try:
                    result = call_api('https://graph.facebook.com/v2.6/me/messages',
                                      "POST",headers,
                                      response, True)
                except Exception as e:
                    app.logger.warn("API call failed", e)

    return build_response.sent_ok()


# Request Handler
@endpoint.route('/v1', methods=['POST'])
def api():
    """
    Endpoint to converse with chatbot.
    Chat context is maintained by exchanging the payload between client and bot.
    sample input/output payload =>
    {
      "currentNode": "",
      "complete": false,
      "parameters": [],
      "extractedParameters": {},
      "missingParameters": [],
      "intent": {
      },
      "context": {},
      "input": "hello",
      "speechResponse": [
      ]
    }
    :param json:
    :return json:
    """
    request_json = request.get_json(silent=True)
    result_json = request_json

    if request_json:

        context = {}
        context["context"] = request_json["context"]

        if app.config["DEFAULT_WELCOME_INTENT_NAME"] in request_json.get(
                "input"):
            intent = Intent.objects(
                intentId=app.config["DEFAULT_WELCOME_INTENT_NAME"]).first()
            result_json["complete"] = True
            result_json["intent"]["intentId"] = intent.intentId
            result_json["intent"]["id"] = str(intent.id)
            result_json["input"] = request_json.get("input")
            template = Template(
                intent.speechResponse,
                undefined=SilentUndefined)
            result_json["speechResponse"] = split_sentence(template.render(**context))

            logger.info(request_json.get("input"), extra=result_json)
            return build_response.build_json(result_json)

        intent_id, confidence = predict(request_json.get("input"))
        intent = Intent.objects.get(id=ObjectId(intent_id))
        

        if intent.parameters:
            parameters = intent.parameters
        else:
            parameters = []

        if ((request_json.get("complete") is None) or (
                request_json.get("complete") is True)):
            result_json["intent"] = {
                "name": intent.name,
                "confidence": confidence,
                "id": str(intent.id)
            }

            if parameters:
                # Extract NER entities
                extracted_parameters = entity_extraction.predict(
                    intent_id, request_json.get("input"))

                missing_parameters = []
                result_json["missingParameters"] = []
                result_json["extractedParameters"] = {}
                result_json["parameters"] = []
                for parameter in parameters:
                    result_json["parameters"].append({
                        "name": parameter.name,
                        "type": parameter.type,
                        "required": parameter.required
                    })

                    if parameter.required:
                        if parameter.name not in extracted_parameters.keys():
                            result_json["missingParameters"].append(
                                parameter.name)
                            missing_parameters.append(parameter)

                result_json["extractedParameters"] = extracted_parameters

                if missing_parameters:
                    result_json["complete"] = False
                    current_node = missing_parameters[0]
                    result_json["currentNode"] = current_node["name"]
                    result_json["speechResponse"] = split_sentence(current_node["prompt"])
                else:
                    result_json["complete"] = True
                    context["parameters"] = extracted_parameters
            else:
                result_json["complete"] = True

        elif request_json.get("complete") is False:
            if "cancel" not in intent.name:
                intent_id = request_json["intent"]["id"]
                intent = Intent.objects.get(id=ObjectId(intent_id))

                extracted_parameter = entity_extraction.replace_synonyms({
                    request_json.get("currentNode"): request_json.get("input")
                })

                # replace synonyms for entity values
                result_json["extractedParameters"].update(extracted_parameter)

                result_json["missingParameters"].remove(
                    request_json.get("currentNode"))

                if len(result_json["missingParameters"]) == 0:
                    result_json["complete"] = True
                    context = {}
                    context["parameters"] = result_json["extractedParameters"]
                    context["context"] = request_json["context"]
                else:
                    missing_parameter = result_json["missingParameters"][0]
                    result_json["complete"] = False
                    current_node = [
                        node for node in intent.parameters if missing_parameter in node.name][0]
                    result_json["currentNode"] = current_node.name
                    result_json["speechResponse"] = split_sentence(current_node.prompt)
            else:
                result_json["currentNode"] = None
                result_json["missingParameters"] = []
                result_json["parameters"] = {}
                result_json["intent"] = {}
                result_json["complete"] = True

        if result_json["complete"]:
            if intent.apiTrigger:
                isJson = False
                parameters = result_json["extractedParameters"]
                headers = intent.apiDetails.get_headers()
                app.logger.info("headers %s"%headers)
                url_template = Template(
                    intent.apiDetails.url, undefined=SilentUndefined)
                rendered_url = url_template.render(**context)
                if intent.apiDetails.isJson:
                    isJson = True
                    request_template = Template(
                        intent.apiDetails.jsonData, undefined=SilentUndefined)
                    parameters = json.loads(request_template.render(**context))

                try:
                    result = call_api(rendered_url,
                                      intent.apiDetails.requestType,headers,
                                      parameters, isJson)
                except Exception as e:
                    app.logger.warn("API call failed", e)
                    result_json["speechResponse"] = ["Service is not available. Please try again later."]
                else:
                    context["result"] = result
                    template = Template(
                        intent.speechResponse, undefined=SilentUndefined)
                    result_json["speechResponse"] = split_sentence(template.render(**context))
            else:
                context["result"] = {}
                template = Template(intent.speechResponse,
                                    undefined=SilentUndefined)
                result_json["speechResponse"] = split_sentence(template.render(**context))

        return build_response.build_json(result_json)
    else:
        return abort(400)

def update_model(app, message, **extra):
    """
    Signal hook to be called after training is completed.
    Reloads ml models and synonyms.
    :param app:
    :param message:
    :param extra:
    :return:
    """
    global sentence_classifier

    sentence_classifier = TfIntentClassifier()
    sentence_classifier.load(app.config["MODELS_DIR"])
    synonyms = get_synonyms()
    global entity_extraction
    entity_extraction = EntityExtractor(synonyms)
    app.logger.info("Intent Model updated")

update_model(app,"Modles updated")

from app.nlu.tasks import model_updated_signal
model_updated_signal.connect(update_model, app)

from app.agents.models import Bot
def predict(sentence):
    """
    Predict Intent using Intent classifier
    :param sentence:
    :return:
    """
    bot = Bot.objects.get(name="default")
    predicted = sentence_classifier.predict(sentence)
    app.logger.info("predicted intent %s", predicted)
    if predicted["confidence"] < bot.config.get("confidence_threshold", .90):
        return Intent.objects(intentId=app.config["DEFAULT_FALLBACK_INTENT_NAME"]).first().id, 1.0
    else:
        return predicted["intent"], predicted["confidence"]
