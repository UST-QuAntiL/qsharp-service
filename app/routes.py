# ******************************************************************************
#  Copyright (c) 2021 University of Stuttgart
#
#  See the NOTICE file(s) distributed with this work for additional
#  information regarding copyright ownership.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ******************************************************************************
from qsharp import QSharpCallable

from app import app, qsharp_handler, implementation_handler, db, parameters
from app.request_schemas import TranspilationRequestSchema, TranspilationRequest, ExecutionRequestSchema, \
    ExecutionRequest
from app.response_schemas import TranspilationResponseSchema, TranspilationResponse, ExecutionResponseSchema, \
    ExecutionResponse, ResultResponseSchema, ResultResponse
from app.result_model import Result
from flask import jsonify, abort, request, Response
from flask_smorest import Blueprint
import logging
import json
import base64
import traceback

blp = Blueprint(
    "routes",
    __name__,
    url_prefix="/qsharp-service/api/v1.0/",
    description="All QSharp-Service endpoints",
)

@blp.route("/transpile", methods=["POST"])
@blp.arguments(
    TranspilationRequestSchema,
    example={
        "impl-url": "https://raw.githubusercontent.com/UST-QuAntiL/qsharp-service/main/Sample%20Implementations/circuit_qsharp_params.qs",
        "impl-language": "QSharp",
        "input-params": {
                "a": {
                        "rawValue": 2.0,
                        "type": "Float"
                }
        }
    }
)
@blp.response(200, TranspilationResponseSchema)
def transpile_circuit(request: TranspilationRequest):
    """Get implementation from URL. Pass input into implementation. Generate and transpile circuit
    and return depth and width."""
    if not request:
        abort(400)
    impl_language = request.get('impl_language', '')
    input_params = request.get('input_params', "")
    impl_url = request.get('impl_url', "")
    qsharp_string = request.get('qsharp_string', "")
    impl_data = request.get('impl_data', "")
    bearer_token = request.get("bearer_token", "")
    if input_params != "":
        input_params = parameters.ParameterDictionary(input_params)
    # adapt if real backends are available
    token = ''
    # if 'token' in input_params:
    #     token = input_params['token']
    # elif 'token' in request.json:
    #     token = request.json.get('token')
    # else:
    #     abort(400)
    logging.info("Input is " + str(request))

    if impl_url is not None and impl_url != "":
        impl_url = request.get('impl_url')
        if impl_language.lower() == 'qsharp':
            short_impl_name = 'no name'
            circuit = implementation_handler.prepare_code_from_qsharp_url(impl_url, bearer_token)
        else:
            short_impl_name = "untitled"
            try:
                circuit = implementation_handler.prepare_code_from_url(impl_url, input_params, bearer_token)
            except ValueError:
                abort(400)

    elif impl_data:
        impl_data = base64.b64decode(impl_data.encode()).decode()

        short_impl_name = 'no short name'
        if impl_language.lower() == 'qsharp':
            circuit = implementation_handler.prepare_code_from_qsharp(impl_data)
        else:
            try:
                circuit = implementation_handler.prepare_code_from_data(impl_data, input_params)
            except ValueError:
                abort(400)
    elif qsharp_string:
        short_impl_name = 'no short name'
        app.logger.info(qsharp_string)
        circuit = qsharp_string
    else:
        abort(400)

    try:
        transpiled_circuit: QSharpCallable = qsharp_handler.transpile(circuit)
        if impl_language.lower() == 'qsharp':
            estimated_resources = transpiled_circuit.estimate_resources(**input_params)
        else:
            estimated_resources = transpiled_circuit.estimate_resources()
        # count number of gates, multi qubit gates and measurements operation, by iterating over all operations
        number_of_cnot_gates = estimated_resources["CNOT"]
        number_of_measurement_operations = estimated_resources["Measure"]

        # width: the amount of qubits
        width = estimated_resources["Width"]

        # In Q#, only T-gates impact depth
        t_depth = estimated_resources["Depth"]

        if impl_language.lower() == 'qsharp':
            traced = transpiled_circuit.trace(**input_params)
        else:
            traced = transpiled_circuit.trace()
    except Exception:
        app.logger.info(f"Transpile {short_impl_name}.")
        app.logger.info(traceback.format_exc())
        abort(Response("Transpilation failed", 500))

    app.logger.info(f"Transpile {short_impl_name}: "
                    f"w={width}, "
                    f"t_d={t_depth}, "
                    f"number of measurement operations={number_of_measurement_operations}")
    return TranspilationResponse(t_depth, number_of_cnot_gates, width, number_of_measurement_operations, circuit, traced)


@blp.route("/execute", methods=["POST"])
@blp.arguments(
    ExecutionRequestSchema,
    example={
        "impl-url": "https://raw.githubusercontent.com/UST-QuAntiL/qsharp-service/main/Sample%20Implementations/circuit_qsharp_params.qs",
        "impl-language": "QSharp",
        "shots": 1024,
        "gate-noise": {
            "single-qubit": 0.1,
            "multiple-qubit": 0.2,
            "measurement": 0.1
        },
        "input-params": {
                "a": {
                        "rawValue": 2.0,
                        "type": "Float"
                }
        }
    }
)
@blp.response(202, ExecutionResponseSchema)
def execute_circuit(request: ExecutionRequest):
    """Put execution job in queue. Return location of the later result."""
    if not request:
        abort(400)
    impl_language = request.get('impl_language', '')
    impl_url = request.get('impl_url')
    bearer_token = request.get("bearer_token", "")
    impl_data = request.get('impl_data')
    qsharp_string = request.get('qsharp_string', "")
    noise = request.get('gate_noise', "")
    qpu = request.get('qpu_name', "")
    input_params = request.get('input_params', "")
    if input_params != "":
        input_params = parameters.ParameterDictionary(input_params)
    shots = request.get('shots', 1024)
    if 'token' in input_params:
        token = input_params['token']
    elif 'token' in request:
        token = request.get('token')
    else:
        token = ""

    # If noise is not a dictionary, see if different information is given, else turn it into a blank dictionary
    if not isinstance(noise, dict):
        if qpu == "noisy-simulator":
            noise = {"single_qubit": 0.1, "multiple_qubit": 0.2, "measurement": 0.1}
        else:
            noise = {}

    job = app.execute_queue.enqueue('app.tasks.execute', impl_url=impl_url, impl_data=impl_data,
                                    impl_language=impl_language, qsharp=qsharp_string,
                                    token=token, input_params=input_params, shots=shots, bearer_token=bearer_token,
                                    noise=noise)
    result = Result(id=job.get_id(), shots=shots)
    db.session.add(result)
    db.session.commit()

    logging.info('Returning HTTP response to client...')
    content_location = '/qsharp-service/api/v1.0/results/' + result.id
    response = ExecutionResponse(content_location)
    response.status_code = 202
    response.headers.set("Location", content_location)
    return response


@app.route('/qsharp-service/api/v1.0/calculate-calibration-matrix', methods=['POST'])
def calculate_calibration_matrix():
    """Put calibration matrix calculation job in queue. Return location of the later result."""
    abort(404)


@blp.route("/results/<string:result_id>", methods=["GET"])
@blp.response(200, ResultResponseSchema)
def get_result(result_id):
    """Return result when it is available."""
    result = Result.query.get(result_id.strip())
    if result.complete:
        result_histogram = json.loads(result.result)
        response = ResultResponse(result.id, result.complete, result_histogram, result.backend, result.shots)
    else:
        response = ResultResponse(result.id, result.complete)
    return response


@blp.route("/version", methods=["GET"])
@blp.response(200)
def version():
    return jsonify({'version': '1.0'})


