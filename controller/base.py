
from flask import Response, jsonify, render_template, url_for, request, redirect
from flask.ext.restful import Resource
from flask.ext.classy import FlaskView, route
from lib.core import Code, Database, CodeNotFound
from lib.config import Config

class BaseController:
    
    def config(self):
        a = Config()
        a.parse()
        return a
