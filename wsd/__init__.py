# -*- coding: utf-8 -*-
from flask import Flask
from config import STATIC_DIR, TEMPLATES_DIR
from utils import jinjaFilters

app = Flask(__name__, static_folder=STATIC_DIR, template_folder=TEMPLATES_DIR)
app.config.from_object('config.Config')

app.jinja_env.filters['day'] = jinjaFilters.day
app.jinja_env.filters['month'] = jinjaFilters.month
app.jinja_env.filters['year'] = jinjaFilters.year
app.jinja_env.filters['filesize'] = jinjaFilters.filesize

from .views import *
from .context_processors import *
