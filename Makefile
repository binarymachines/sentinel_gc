HOST=127.0.0.1
TEST_PATH=./tests
RECIPEPREFIX= # prefix char is a space, on purpose; do not delete
PHONY=clean


clean: 
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

install-deps:
	pipenv install
	pipenv install -e .

regen: clean
	PYTHONPATH=`pwd` pipenv run routegen -e s_config.yaml > sentinel.py

spinup: 
	export SENTINEL_HOME=`pwd`; pipenv run python sentinel.py --configfile s_config.yaml

run-wsgi:
	export SENTINEL_HOME=`pwd`; pipenv run gunicorn -b :8080 sentinel:app

deploy:
	gcloud app deploy

test:	clean
	export SENTINEL_HOME=`pwd`; pipenv run python -m unittest discover -s snap ./tests -v

