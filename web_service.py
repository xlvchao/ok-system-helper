from gevent import monkey
monkey.patch_all()
from flask import Flask, request, jsonify
from core.system_helper import SysInfosCollector
from gevent import pywsgi

import os
import configparser
from utils.log_helper import LoggerFactory

logger = LoggerFactory().getLogger()


# Flask初始化参数尽量使用你的包名，这个初始化方式是官方推荐的，官方解释：http://flask.pocoo.org/docs/0.12/api/#flask.Flask
app = Flask(__name__)

sys_infos_collector = SysInfosCollector()

# 获取配置
base_dir = os.path.dirname(os.path.abspath(__file__))
conf = configparser.ConfigParser()
conf.read(os.path.join(base_dir, 'config.conf'))

# application
application_name = conf.get("application", "name")
application_host = conf.get("application", "host")
application_port = conf.getint("application", "port")


@app.route('/cpu', methods=['GET'])
def cpu():
    try:
        return jsonify({'code': 0, 'message': 'success', 'data': sys_infos_collector.cpu()})
    except Exception as e:
        logger.error(e.with_traceback())
        return jsonify({'code': 1, 'message': 'failed'})

@app.route('/memory', methods=['GET'])
def memory():
    try:
        return jsonify({'code': 0, 'message': 'success', 'data': sys_infos_collector.memory()})
    except Exception as e:
        logger.error(e.with_traceback())
        return jsonify({'code': 1, 'message': 'failed'})


@app.route('/swap', methods=['GET'])
def swap():
    try:
        return jsonify({'code': 0, 'message': 'success', 'data': sys_infos_collector.swap()})
    except Exception as e:
        logger.error(e.with_traceback())
        return jsonify({'code': 1, 'message': 'failed'})

@app.route('/disk', methods=['GET'])
def disk():
    try:
        return jsonify({'code': 0, 'message': 'success', 'data': sys_infos_collector.disk()})
    except Exception as e:
        logger.error(e.with_traceback())
        return jsonify({'code': 1, 'message': 'failed'})


if __name__ == "__main__":
    logger.info('ok-system-helper web_service starting...')
    # 这种是不太推荐的启动方式，我这只是做演示用，官方启动方式参见：http://flask.pocoo.org/docs/0.12/quickstart/#a-minimal-application
    # app.run(host="0.0.0.0", port=application_port, debug=False)

    # 使用WSGI启动服务
    server = pywsgi.WSGIServer(('0.0.0.0', application_port), app)
    server.serve_forever()