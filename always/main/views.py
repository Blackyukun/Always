from flask import render_template, redirect, url_for, request, Blueprint

from always import db


main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html')