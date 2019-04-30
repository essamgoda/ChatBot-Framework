
setup: restore_db
	test -d venv || virtualenv venv
	. venv/bin/activate; pip install -Ur requirements.txt
	. venv/bin/activate; python -m spacy download en
	. venv/bin/activate; python manage.py install_nltk_dependencies
	. venv/bin/activate; python manage.py init

restore_db: 
	mongorestore --drop --db=iky-ai --dir=dump/iky-ai/

run_dev: 
	. venv/bin/activate && python run.py

run_prod: 
	. venv/bin/activate && APPLICATION_ENV="Production" gunicorn -k gevent --bind 0.0.0.0:8080 run:app

run_docker:
	gunicorn run:app --bind 0.0.0.0:8080 --access-logfile=logs/gunicorn-access.log --error-logfile logs/gunicorn-error.log

heroku: 
	python -m spacy download en
clean:
	rm -rf venv
	find -iname "*.pyc" -delete
