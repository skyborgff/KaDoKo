from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_cors import CORS, cross_origin
import os
import multiprocessing
from multiprocessing import Process, Manager
# from Core.API.TaskManager import Tasker
from Core.Tasker.TaskManager import Tasker, TaskImportance, TaskType


class FlaskAPI:
    def __init__(self, taskDict: dict):
        print('Flask Server Object Created')

        # configuration
        DEBUG = False

        # instantiate the app
        self.app = Flask(__name__, static_folder="FlaskFiles")
        self.app.config.from_object(__name__)

        # enable CORS
        CORS(self.app, resources={r'/*': {'origins': '*'}})

        self.tasker = Tasker(taskDict)

        # sanity check route
        @self.app.route('/ping', methods=['GET'])
        def ping_pong():
            return jsonify('pong!')

        @self.app.route('/library_list', methods=['GET'])
        def library_list():
            # info = self.kadoko.ui.library_list()
            info = self.tasker.addWaitReply('library_list', TaskImportance.UI, TaskType.SYNC)
            return jsonify(info)

        @self.app.route('/db_list', methods=['GET'])
        def db_list():
            # info = self.kadoko.ui.db_list()
            info = self.tasker.addWaitReply('db_list', TaskImportance.UI, TaskType.SYNC)
            return jsonify(info)

        @self.app.route('/plugin_info', methods=['GET'])
        def plugin_info():
            info = self.tasker.addWaitReply('plugin_info', TaskImportance.UI, TaskType.SYNC)
            return jsonify(info)

        @self.app.route('/setup_settings', methods=['POST'])
        def setup_settings():
            response_object = {'status': 'success'}
            post_data = request.get_json()
            # self.kadoko.ui.setup_settings(post_data)
            self.tasker.addWaitReply('setup_settings', TaskImportance.UI, TaskType.SYNC, [post_data])
            response_object['message'] = 'Settings Received'
            return jsonify(response_object)

        @self.app.route('/get_authentication_needed', methods=['GET'])
        def get_authentication_needed():
            # info = self.kadoko.ui.get_authentication_needed()
            info = self.tasker.addWaitReply('get_authentication_needed', TaskImportance.UI, TaskType.SYNC)
            return jsonify(info)

        @self.app.route('/set_authentication', methods=['POST'])
        def set_authentication():
            response_object = {'status': 'success'}
            post_data = request.get_json()
            # self.kadoko.ui.set_authentication(post_data)
            self.tasker.addTask('set_authentication', TaskImportance.UI, TaskType.SYNC, [post_data])
            response_object['message'] = 'Auth Received'
            return jsonify(response_object)

        @self.app.route('/force/<path:path>')
        def send_force(path):
            # self.taskDict['tasks'] += {'task': 'generate_graph', 'args': "Core/API/FlaskFiles/force/force.json"}
            # # self.kadoko.database.generate_graph("Core/API/FlaskFiles/force/force.json")
            # print('Flask')
            # print(self.taskDict)
            # print('Sending Graph')
            self.tasker.addWaitReply('generate_graph', TaskImportance.UI, TaskType.SYNC, ["Core/API/FlaskFiles/force/force.json"])
            return send_from_directory('FlaskFiles/force', path)

        self.app.run('localhost', 8283, False)
