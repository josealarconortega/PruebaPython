import math
import random
import uuid
from typing import List, Optional

from application.api.database import db
from application.api.database.extended_model import ExtendedModel 

from flask import current_app 
class Earthquake(ExtendedModel):
    __tablename__ = 'Earthquake'
    create_at = db.Column(db.DateTime, primary_key=True)
    fecha_inicio = db.Column(db.DateTime, nullable=False)
    fecha_fin = db.Column(db.DateTime, nullable=False)
    magnitud_min = db.Column(db.Float, nullable=False)
    magnitud_max = db.Column(db.Float, nullable=False) 
    salida = db.Column(db.Text())
    def __init__(self, fecha_inicio, fecha_fin, magnitud_min, magnitud_max, salida):
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.magnitud_min = magnitud_min
        self.magnitud_max = magnitud_max
        self.salida = salida