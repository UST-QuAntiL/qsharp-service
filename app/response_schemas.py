import json

import marshmallow as ma
from flask import Response


class TranspilationResponse:
    def __init__(self, t_depth, number_of_cnots, width, number_of_measurement_operations, qsharp_string, traced_qsharp):
        self.t_depth = t_depth
        self.number_of_cnots = number_of_cnots
        self.width = width
        self.number_of_measurement_operations = number_of_measurement_operations
        self.qsharp_string = qsharp_string
        self.traced_qsharp = str(traced_qsharp)


class ExecutionResponse(Response):
    def __init__(self, location):
        super().__init__()
        self.location = location



class ResultResponse:
    def __init__(self, id, complete, result=None, backend=None, shots=None):
        self.id = id
        self.complete = complete
        self.result = result
        self.backend = backend
        self.shots = shots


class TranspilationResponseSchema(ma.Schema):
    t_depth = ma.fields.Integer(data_key="t-depth")
    number_of_cnots = ma.fields.Integer(data_key="number-of-cnots")
    width = ma.fields.Integer()
    number_of_measurement_operations = ma.fields.Integer(data_key="number-of-measurement-operations")
    qsharp_string = ma.fields.String(data_key="qsharp-string")
    traced_qsharp = ma.fields.String(data_key="traced-qsharp")


class ExecutionResponseSchema(ma.Schema):
    location = ma.fields.String()


class ResultResponseSchema(ma.Schema):
    id = ma.fields.UUID()
    complete = ma.fields.Boolean()
    result = ma.fields.Mapping()
    backend = ma.fields.String()
    shots = ma.fields.Integer()
