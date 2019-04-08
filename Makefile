PACKAGE = $(python setup.py --name)

run:
	python example-slackapp/run.py

clean:
	@ python setup.py clean
	@ rm -rf *.egg-info .pytest_cache
	@ find . -name '*.pyc' | xargs rm
