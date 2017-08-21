from flask import render_template, redirect, url_for, request, Blueprint

from always import db


admin = Blueprint('admin', __name__)