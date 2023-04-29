DOCKER_REPO := sahil7776

wake-up:
	docker-compose up -d

pip:
	pip install -r requirements.txt

localdev:
	docker exec -it backend bash

build-image:
	@docker build -t ${DOCKER_REPO}/api -f Dockerfile .

push-image:
	@docker push  -t ${DOCKER_REPO}/api

run-test:
	python manage.py test services.chatbot.tests services.pdfparser.tests

local-api: pip
	python manage.py migrate --settings=BookGpt.settings.local
	python manage.py runserver --settings=BookGpt.settings.local 0.0.0.0:8000

