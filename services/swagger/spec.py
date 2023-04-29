import json
import yaml
from django.shortcuts import render
import os


def generate_yaml_to_ui(request):
    swagger_yml = os.path.join(os.getcwd(), "services", "swagger", "swagger.yaml")
    swagger_template = "swagger_ui_template.html"
    with open(swagger_yml, 'r') as stream:
        try:
            spec_dict = yaml.safe_load(stream)
            return render(request, swagger_template, {
                'swagger_json': json.dumps(spec_dict)
            })
        except yaml.YAMLError as e:
            print(e)
            return request.Response(
                code=500
            )
