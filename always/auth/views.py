from flask import render_template, redirect, url_for, request, Blueprint

from always import db


auth = Blueprint('auth', __name__)
