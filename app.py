from MISW_EXP_2_DETECTOR_INTRUSOS import create_app
from flask_restful import Resource, Api
from .common.utils import get_request_mapping
from flask import Flask, request
from random import random, randint
import requests
from celery import Celery

celery_app = Celery('tasks', broker='redis://127.0.0.1:6379/0')

app = create_app('default')
app_context = app.app_context()
app_context.push()

api = Api(app)


@celery_app.task(name='log.alertas')
def enviar_alerta(datos_log):
    pass


class VistaDetector(Resource):
    def post(self):
        test = get_request_mapping(request.json)
        print(test)
        # enviar_alerta.apply_async(args)


api.add_resource(VistaDetector, '/api/detector-intrusos')
        
