from flask import Flask, jsonify
from flask import request
from flask_httpauth import HTTPBasicAuth

from parser import ParserError, Parser

SUCCESS_STATUS = 'success'
ERROR_STATUS = 'error'


class Controller:
    app = Flask(__name__)
    auth = HTTPBasicAuth()

    @staticmethod
    @app.errorhandler(ParserError)
    def parser_running_error_handler(e):
        return jsonify(status=ERROR_STATUS,
                       error=dict(
                           code=e.code,
                           message=e.message)
                       ), e.code

    @staticmethod
    @auth.get_password
    def get_pw(username):
        if username == 'admin':
            return 'admin'
        return None

    @staticmethod
    @app.route('/')
    @auth.login_required
    def index():
        current, end = Parser.get_status()
        return jsonify(status=SUCCESS_STATUS, current=current, end=end)

    @staticmethod
    @app.route('/stop')
    @auth.login_required
    def stop():
        Parser.stop_parsing()
        return jsonify(status=SUCCESS_STATUS)

    @staticmethod
    @app.route('/start')
    @auth.login_required
    def start():
        Parser.start_parsing(request.args.get('url'), int(request.args.get('count')))
        return jsonify(status=SUCCESS_STATUS)

    @staticmethod
    @app.route('/result')
    @auth.login_required
    def result():
        return jsonify(status=SUCCESS_STATUS, result=Parser.get_result())

    @staticmethod
    @app.route('/clear')
    @auth.login_required
    def clear():
        Parser.clear_result()
        return jsonify(status=SUCCESS_STATUS)

    @classmethod
    def run(cls, **kwargs):
        cls.app.run(**kwargs)
