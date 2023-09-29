from MISW_EXP_2_DETECTOR_INTRUSOS import create_app
from flask_restful import Resource, Api
from .common.utils import get_request_mapping, generate_random_request
from flask import Flask, request
from random import random, randint
import pandas as pd
import requests
from celery import Celery
import joblib

celery_app = Celery('tasks', broker='redis://127.0.0.1:6379/0')
model = joblib.load('./model_training/trained_model.joblib') # load the ML model

app = create_app('default')
app_context = app.app_context()
app_context.push()

api = Api(app)


@celery_app.task(name='log.alertas')
def enviar_alerta(datos_log):
    pass


class VistaDetector(Resource):
    def post(self):
        request_mapped = get_request_mapping(request.json["req"])
        # request_mapped = get_request_mapping(generate_random_request())
        df = pd.DataFrame(request_mapped, index=[0])
        intrusion = model.predict(df)
        if intrusion[0] == -1:
            args = {'request': request.json, 'intrusion': request.json["info"]}
            enviar_alerta.apply_async(args)

api.add_resource(VistaDetector, '/api/detector-intrusos')