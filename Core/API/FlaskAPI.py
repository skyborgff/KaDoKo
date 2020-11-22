from flask import Flask, jsonify, request
from flask_cors import CORS


class FlaskAPI:
    def __init__(self, kadoki):
        # configuration
        DEBUG = True

        # instantiate the app
        self.app = Flask(__name__)
        self.app.config.from_object(__name__)

        # enable CORS
        CORS(self.app, resources={r'/*': {'origins': '*'}})

        self.kadoki = kadoki

        # sanity check route
        @self.app.route('/ping', methods=['GET'])
        def ping_pong():
            return jsonify('pong!')

        @self.app.route('/library_list', methods=['GET'])
        def library_list():
            return jsonify(self.kadoki.ui.library_list())

        @self.app.route('/db_list', methods=['GET'])
        def db_list():
            return jsonify(self.kadoki.ui.db_list())

        @self.app.route('/setup_settings', methods=['POST'])
        def setup_settings():
            response_object = {'status': 'success'}
            post_data = request.get_json()
            self.kadoki.ui.setup_settings(post_data)
            response_object['message'] = 'Settings Received'
            return jsonify(response_object)

        @self.app.route('/get_authentication_needed', methods=['GET'])
        def get_authentication_needed():
            return jsonify(self.kadoki.ui.get_authentication_needed())

        @self.app.route('/set_authentication', methods=['POST'])
        def set_authentication():
            response_object = {'status': 'success'}
            post_data = request.get_json()
            self.kadoki.ui.set_authentication(post_data)
            response_object['message'] = 'Auth Received'
            return jsonify(response_object)
