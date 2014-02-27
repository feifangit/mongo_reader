import logging
import traceback
import argparse
from flask import Flask, Response, request, jsonify
from flask import json
from pymongo import MongoClient, MongoReplicaSetClient
from mongoreader import MongoHandler
from bson import json_util

app = Flask(__name__)
logger = logging.getLogger('mongo_reader')

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument("--mongoip", help="MongoDB IP", default='127.0.0.1')
parser.add_argument("--mongoport", help="MongoDB Port", type=int, default='27017')
parser.add_argument("--mongors", help="MongoDB Replica set name")


@app.route("/")
def hello():
    return jsonify({"foo": "bar"})


@app.route("/<db>/<col>/<cmd>")
def rest_call(db, col, cmd):
    logger.debug("rest call %s %s %s", db, col, cmd)
    r = {"error":"no command found", "ok": 0}
    if hasattr(mongoReader, "cmd%s" % cmd):
        try:
            r = getattr(mongoReader, "cmd%s" % cmd)(db, col, request.args)
            r["ok"] = 1
            
        except Exception as e:
            traceback.print_exc()
            r = {"ok": 0, "error": str(e)}
    resp = json.dumps(r, indent=2, default=json_util.default)
    return app.response_class(resp, mimetype='application/json')

def build_app(cmdargs=""):
    args = parser.parse_args(cmdargs.split())
    mongoConn = (MongoReplicaSetClient if args.mongors else MongoClient)(args.mongoip, args.mongoport, args.mongors)
    global mongoReader 
    mongoReader = MongoHandler(mongoConn)
    return app


if __name__ == "__main__":
    # -p -i -d only available for start up from command line
    parser.add_argument("-p", "--port", help="port number", type=int, default=5000)
    parser.add_argument("-i", "--ip", help="listening IP", default='0.0.0.0')
    parser.add_argument("-d", "--debug", help="debug", action="store_true")
    args = parser.parse_args()

    mongoConn = (MongoReplicaSetClient if args.mongors else MongoClient)(args.mongoip, args.mongoport, args.mongors)
    mongoReader = MongoHandler(mongoConn)
    app.run(debug=args.debug)
