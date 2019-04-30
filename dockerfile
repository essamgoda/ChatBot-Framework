FROM python:3.7

ADD . /code
WORKDIR /code

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m nltk.downloader "averaged_perceptron_tagger"; python
RUN python -m nltk.downloader "punkt"; python
RUN python -m nltk.downloader "stopwords"; python
RUN python -m nltk.downloader "wordnet"; python
RUN python -m spacy download en; python

EXPOSE 8080


CMD ["make","run_docker"]
