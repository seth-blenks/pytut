
from flask import Blueprint

client = Blueprint('client',__name__)

from . import views
from . import admin
from . import mailing
