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

from app import implementation_handler, qsharp_handler, db
from rq import get_current_job

from app.result_model import Result
import logging
import json
import base64


def execute(impl_url, impl_data, impl_language, qsharp, input_params, token, qpu_name, shots, bearer_token: str):
    """Create database entry for result. Get implementation code, prepare it, and execute it. Save result in db"""
    job = get_current_job()

    logging.info('Preparing implementation...')
    circuit = None
    if qsharp:
        circuit = qsharp
    else:
        if impl_url:
            if impl_language.lower() == 'qsharp':
                circuit = implementation_handler.prepare_code_from_qsharp_url(impl_url, bearer_token)
            else:
                circuit = implementation_handler.prepare_code_from_url(impl_url, input_params, bearer_token)
        elif impl_data:
            impl_data = base64.b64decode(impl_data.encode()).decode()
            if impl_language.lower() == 'qsharp':
                circuit = implementation_handler.prepare_code_from_qsharp(impl_data)
            else:
                circuit = implementation_handler.prepare_code_from_data(impl_data, input_params)
    if not circuit:
        result = Result.query.get(job.get_id())
        result.result = json.dumps({'error': 'URL not found'})
        result.complete = True
        db.session.commit()


    logging.info('Start transpiling...')
    try:
        transpiled_circuit = qsharp_handler.transpile(circuit)
    except Exception:
        result = Result.query.get(job.get_id())
        result.result = json.dumps({'error': 'Q# code could not be compiled'})
        result.complete = True
        db.session.commit()

    logging.info('Start executing...')
    if impl_language.lower() == "qsharp":
        job_result = qsharp_handler.execute_job(transpiled_circuit, shots, qpu_name, input_params)
    else:
        job_result = qsharp_handler.execute_job(transpiled_circuit, shots, qpu_name)
    if job_result:
        result = Result.query.get(job.get_id())
        result.result = json.dumps(job_result)
        result.complete = True
        db.session.commit()
    else:
        result = Result.query.get(job.get_id())
        result.result = json.dumps({'error': 'execution failed'})
        result.complete = True
        db.session.commit()
