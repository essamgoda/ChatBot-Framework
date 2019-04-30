# Bot-FrameWork

### An AI Chatbot framework built in Python

Building a chatbot can sound daunting, but it’s totally doable. Bot is an AI powered conversational dialog interface built in Python. With Bot it’s easy to create Natural Language conversational scenarios with no coding efforts whatsoever. The smooth UI makes it effortless to create and train conversations to the bot and it continuously gets smarter as it learns from conversations it has with people. Bot can live on any channel of your choice (such as Messenger, Slack etc.) by integrating it’s API with that platform.


### Installation
### Using docker-compose (Recommended) 
```sh
docker-compose up -d
docker-compose exec iky_backend python manage.py init
```
#### backend

* Setup Virtualenv , MongoDB and install python requirements
```sh
install mongodb from https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-16-04 

pip3 install virtualenv

virtualenv venv

make setup

make run_dev

```
* Production
```sh
make run_prod
```

#### frontend
* Development
sudo npm install -g @angular/cli
```sh
cd frontend
npm install
ng serve
```
* Production
```sh
cd frontend
ng build --prod --environment=python
```
serve files in dist/ folder using nginx or any webserver

### DB

#### Restore
```
mongorestore --drop --db=iky-ai --dir=dump/iky-ai/
```
or you can import some default intents using follwing steps

- goto http://localhost:8080/agent/default/settings
- click 'choose file'
- choose 'examples/default_intents.json file'
- click import

### Heroku
[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)


* add your dev/production configurations in config.py

 ### Dependencies documentations
* [NLTK documentation](www.nltk.org/)
* [SKLearn documentation](http://scikit-learn.org/)
* [CRFsuite documentation](http://www.chokkan.org/software/crfsuite/)
* [python CRfSuite](https://python-crfsuite.readthedocs.io/en/latest/)
