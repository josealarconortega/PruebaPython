from . import *
import aiohttp
from flask import jsonify, request
from os import getenv
from application.api.services.CallService import CallService
import json
from datetime import datetime
import time
from sqlalchemy import exc
from datetime import datetime

@mod.route('/getEarthquakesByDates', methods=["GET"])
def getEarthquakesByDates():
    response = {
        'status': 400,
        'data': []
    }
    errors = []
    
    fechaInicio = request.json['fechaInicio'] if 'fechaInicio' in request.json  else None
    fechaFin = request.json['fechaFin'] if 'fechaFin' in request.json  else None

    try:
        datetime.strptime(fechaInicio, '%d/%m/%Y')
        datetime.strptime(fechaFin, '%d/%m/%Y')
    except:
        response['status'] = 400
        errors.append('Error, la informacion enviada no es correcta')

    magnitudeMinima = float(request.json['magnitudeMinima']) if float(request.json['magnitudeMinima']) else None
    
    if fechaInicio is None or fechaFin is None or str(fechaInicio) >  str(fechaFin) or magnitudeMinima is None or magnitudeMinima == 0 or magnitudeMinima < 0 :
        response['status'] = 400
        errors.append('Error, la informacion enviada no es correcta')

    
    if len(errors) == 0:
        try:
            uri_service = getenv('url_api')
            uri = '&starttime='+fechaInicio+'&endtime='+fechaFin+'&minmagnitude=' + str(magnitudeMinima)
            service = CallService()
            data = service.call([uri_service + uri], ['get']) 
            result = json.loads(data[0])
            
            eart = Earthquake(fecha_inicio = fechaInicio, fecha_fin = fechaFin, magnitud_min = magnitudeMinima, magnitud_max = 0, salida = result)
            db.session.add(eart)
            response['status'] = 200
            response_data = []
            for data in result['features']:
                data = {
                    "mag": data['properties']['mag'],
                    "place": data['properties']['place'],
                    "time": time.strftime("%A, %b %d %Y %H:%M:%S.%f", time.localtime(data['properties']['time'])),
                    "updated": time.strftime("%A, %b %d %Y %H:%M:%S.%f", time.localtime(data['properties']['updated'])),
                    "alert": data['properties']['alert'],
                    "status": data['properties']['status'],
                    "tsunami": data['properties']['tsunami'],
                    "magType": data['properties']['magType'],
                    "type": data['properties']['type'],
                    "title": data['properties']['title']
                }
                response_data.append(data)
            response['data'] = response_data
        except:
            response['status'] = 400
    else:
        response['data'] = errors
    return jsonify(response['data']),  response['status']


@mod.route('/getEarthquakesByMagnitudes', methods=["GET"])
def getEarthquakesByMagnitudes():
    errors = []
    
    response = {
        'status': 400,
        'data': []
    } 
    magnitudeMinima = None
    magnitudeMaxima = None
    try:
        magnitudeMinima = float(request.json['magnitudeMinima']) if float(request.json['magnitudeMinima']) else None
        magnitudeMaxima = float(request.json['magnitudeMaxima']) if float(request.json['magnitudeMaxima']) else None
    except:
        response['status'] = 400
        errors.append('Error, la informacion enviada no es correcta')
    if magnitudeMinima is None or magnitudeMinima == 0 or magnitudeMinima < 0 or magnitudeMaxima is None or magnitudeMaxima == 0 or magnitudeMaxima < 0 or  magnitudeMinima > magnitudeMaxima:
        response['status'] = 400
        errors.append('Error, la informacion enviada no es correcta')
    if len(errors) == 0:
        try:
            uri_service = getenv('url_api')
            uri = '&minmagnitude=' + str(magnitudeMinima) + '&maxmagnitude' + str(magnitudeMaxima)
            service = CallService()
            data = service.call([uri_service + uri], ['get']) 
            result = json.loads(data[0])
            eart = Earthquake(fecha_inicio = None, fecha_fin = None, magnitud_min = magnitudeMinima, magnitud_max = magnitudeMaxima, salida = result)
            db.session.add(eart)
            response_data = []
            for data in result['features']:
                data = {
                    "mag": data['properties']['mag'],
                    "place": data['properties']['place'],
                    "time": time.strftime("%A, %b %d %Y %H:%M:%S.%f", time.localtime(data['properties']['time'])),
                    "updated": time.strftime("%A, %b %d %Y %H:%M:%S.%f", time.localtime(data['properties']['updated'])),
                    "alert": data['properties']['alert'],
                    "status": data['properties']['status'],
                    "tsunami": data['properties']['tsunami'],
                    "magType": data['properties']['magType'],
                    "type": data['properties']['type'],
                    "title": data['properties']['title']
                }
                response_data.append(data)
            response['data'] = response_data

        except:
            response['status'] = 500
            response['data'] = ['Error, Fallo la transaccion']
    else:
        response['data'] = errors 
    return jsonify(response['data']), response['status']