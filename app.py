import os
from flask import Flask
from flask import jsonify
from flask import request
import json
from cerberus import Validator
from exceptions import payLoadIsMissing
from exceptions import malformedJson
from exceptions import payloadNotMatchingSchema
from scale import Scale



app = Flask(__name__)


@app.errorhandler(payLoadIsMissing)
@app.errorhandler(payloadNotMatchingSchema)
@app.errorhandler(malformedJson)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


payload_output_schema =  {
                        'success': {'type': 'boolean', 'required': True},
                        'payload': {'type': 'dict', 'required': True, 'schema': {'risk':{'type':'number'}}}
                        }

payload_input_schema = {
                    'risk': {'type': 'number', 'required': True},
                    'to_date': {'type': 'string', 'required': True},
                    'pair': {'type': 'string', 'required': True},
                    }



@app.route("/ping")
def ping():
    return "Pong!"

@app.route("/schema")
def schema():
    return json.dumps(dict(input=payload_input_schema, output=payload_output_schema))

@app.route("/", methods=['GET'])
def index():
    return 'Block-Scale_risk'

@app.route("/", methods=['POST'])
@app.route("/simulate", methods=['POST'])
def simulate():
    v = Validator()
    v.schema = payload_input_schema
    payload = request.form.get('payload', None)
    if not(payload):
        raise payLoadIsMissing('There is no payload', status_code=500)
    try:
        payload = json.loads(payload)
    except:
        raise malformedJson("Payload present but malformed")
    if v(payload):
        sc = Scale(payload=payload)
        data = sc.scaleToDate()
        res = dict(success=True,payload=data)
        return json.dumps(res)
    else:
        raise payloadNotMatchingSchema("Payload didn't match schema ({}\n{})".format(payload_input_schema, v.errors))
        

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7003))
    app.run(host='0.0.0.0', port=port)