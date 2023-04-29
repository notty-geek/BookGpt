# BookGpt

This is a Django project with Rest API that provides a chatbot service and a PDF parser service.


## Steps to Run the Project

1. Fill up the .env file present in your root directory 

```angular2html
##########################
## POSTGRES RELATED ENV
##########################

POSTGRES_USER=chatgpt_user
POSTGRES_PASSWORD=password
POSTGRES_DB=chatgpt_db
POSTGRES_HOST=BookGptDb

##########################
## REDIS RELATED ENV
##########################
REDIS_HOST=redis
REDIS_PORT=6379



##########################
## OPENAI RELATED ENV
##########################
OPENAI_API_KEY=

##########################
## PINECONE RELATED ENV
##########################
PINECONE_INDEX=
PINECONE_API_ENV=
PINECONE_API_KEY=


```

2. Run `make wake-up`

#### Your local server should spin up and Swagger Url should be up and running

```http://localhost:8000/v1/swagger-ui```

<br>

###Should look something like this
<br>


![](../../../../var/folders/x1/ztyf7cr13tscl59t7gkzgmjr0000gn/T/TemporaryItems/NSIRD_screencaptureui_oP48nv/Screenshot 2023-04-29 at 11.27.04 AM.png)


####Now, You can try all the APIS from above documentations


## Steps to Build

- `make build-image` to build a new docker image
- `make push-image` to push the Docker image to whatever path is set up in the Makefile.



## Steps to run test 
- ``make run-test``




## Django admin dashboard

- http://localhost:8000/admin

![](../../../../var/folders/x1/ztyf7cr13tscl59t7gkzgmjr0000gn/T/TemporaryItems/NSIRD_screencaptureui_ffAFfD/Screenshot 2023-04-29 at 3.39.41 AM.png)



## Django task queue dashboard 
- http://localhost:8000/django-rq

![](../../../../var/folders/x1/ztyf7cr13tscl59t7gkzgmjr0000gn/T/TemporaryItems/NSIRD_screencaptureui_9NF9Rn/Screenshot 2023-04-29 at 3.39.01 AM.png)


## Creating a Superuser
- To access the Django Admin Dashboard, you can create a superuser using the command `python manange.py createsuperuser`.


## Project Structure 
```angular2html

BookGpt
│
├── settings/
│   ├── __init__.py                # Configurations for Django settings
│   ├── asgi.py                    # ASGI application entry point
│   ├── urls.py                    # URL routing for the project
│   └── wsgi.py                    # WSGI application entry point
│
├── e2e/
│   └── ...                        # Integration tests
│
├── services/
│   ├── chatbot/
│   │   ├── migrations/
│   │   │   └── ...                # Database migrations for chatbot service
│   │   ├── __init__.py            # Initialization code for chatbot service
│   │   ├── admin.py               # Django admin for chatbot models
│   │   ├── apps.py                # Configuration for chatbot app
│   │   ├── helpers.py             # Helper functions for chatbot functionality
│   │   ├── models.py              # Django models for chatbot functionality
│   │   ├── serializers.py         # Serialization logic for chatbot models
│   │   ├── tests.py               # Test cases for chatbot functionality
│   │   └── views.py               # API views for chatbot functionality
│   │
│   └── parser/
│   │   ├── management/
│   │    │   ├── commands/
│   │    │   │   └── ...            # Custom management commands for PDF parser service
│   │    │   ├── __init__.py        # Initialization code for PDF parser service
│   │    │   ├── admin.py           # Django admin for parser models
│   │    │   ├── apps.py            # Configuration for parser app
│   │    │   ├── models.py          # Django models for PDF parser functionality
│   │    │   ├── serializer.py      # Serialization logic for parser models
│   │    │   ├── task.py            # Background task functionality for PDF parsing
│   │    │   ├── tests.py           # Test cases for PDF parser functionality
│   │    │   ├── urls.py            # URL routing for PDF parser service
│   │    │   └── views.py           # API views for PDF parser functionality
│   │    │
│   │    └── migrations/
│   │        └── ...                # Database migrations for parser service
│   │
│    ── swagger/
│       ├── __init__.py                # Initialization code for Swagger documentation
│       ├── spec.py                    # Swagger specification
│       ├── swagger.yaml               # Swagger YAML configuration
│       └── templates/
│           ├── __init__.py            # Initialization code for Swagger templates
│           └── swagger_ui_template.html # HTML template for Swagger UI
│
├── utils/
│   └── lang_chain.py              # Language processing utility functions
│
├── venv/                          # Virtual environment for Python dependencies
│
├── .env                           # Environment variable file for local development
├── .gitignore                     # Files and directories to ignore in Git
├── .local.env                     # Environment variable file for local deployment
├── .pre-commit-config.yaml        # Configuration for pre-commit hooks
├── docker-compose.yml             # Docker Compose configuration for deployment
├── Dockerfile                     # Dockerfile for building deployment image
├── Makefile                       # Makefile for building and deploying project




```

### More things Can be Done

1. More Error Retry implementations can be done
2. Cache implementaion can be done
3. Automated retry mechanism can be build for failed tasks
4. Error tracking Tools can be used like OpenCensus, Sentry
5. CirceCi can be implemented for auto deployments
6. Nginx implementation as a docker sidecar
7. PgBouncer Side car to allow multiple threads of connections for scale
8. Much more things
9. Add E2E testcases, I have added basic template what i mean by that 