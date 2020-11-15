setup:
	sudo apt install python3 python3-dev python3-venv
	python3 -m venv ~/.stock-info-flask-api

install:
	pip install --upgrade pip
	pip install -r requirements.txt

lint:
	pylint --disable=R,C main.py