from flask import (Blueprint, jsonify, request)
from ast import literal_eval

from application.api.database import db
from application.api.models.earthquake import Earthquake 

from application.api.schemas.earthquake_schema import (earthquake_schema, earthquakes_schema)
 
mod = Blueprint('searchEarthquake', __name__)

from . import searchEarthquake                 # noqa 
