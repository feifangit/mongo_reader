import logging
import traceback
import argparse
from flask import Flask, request, jsonify, json
from pymongo import MongoClient, MongoReplicaSetClient
from mongoreader import MongoHandler
from bson import json_util

app = Flask(__name__)
logger = logging.getLogger('mongo_reader')

parser = argparse.ArgumentParser()
parser.add_argument("--mongoconn", help="MongoDB connection string", default='mongodb://127.0.0.1:27017/1')


@app.route("/")
def hello():
    info = {"client_clz": str(type(mongoReader))}
    return jsonify(info)


@app.route("/<db>/<col>/<cmd>")
def rest_call(db, col, cmd):
    logger.debug("rest call %s %s %s", db, col, cmd)
    r = {"error": "no command found", "ok": 0}
    if hasattr(mongoReader, "cmd%s" % cmd):
        try:
            r = getattr(mongoReader, "cmd%s" % cmd)(db, col, request.args)
            r["ok"] = 1
            
        except Exception as e:
            traceback.print_exc()
            r = {"ok": 0, "error": str(e)}
    resp = json.dumps(r, indent=2 if APP_DEBUG else None, default=json_util.default)
    return app.response_class(resp, mimetype='application/json')


def _make_mongo_client(connstr):
    _conn = MongoClient(connstr)
    if _conn._MongoClient__repl:
        _conn = MongoReplicaSetClient(connstr)
    return _conn


def build_app(cmdargs=""):
    args = parser.parse_args(cmdargs.split())
    global mongoReader 
    mongoReader = MongoHandler(_make_mongo_client(args.mongoconn))
    return app


if __name__ == "__main__":
    # for debug only
    # -p -i -d only available for start up from command line
    parser.add_argument("-p", "--port", help="port number", type=int, default=5000)
    parser.add_argument("-i", "--ip", help="listening IP", default='0.0.0.0')
    parser.add_argument("-d", "--debug", help="debug", action="store_true")
    args = parser.parse_args()

    APP_DEBUG = args.debug

    mongoReader = MongoHandler(_make_mongo_client(args.mongoconn))
    app.run(debug=APP_DEBUG)
