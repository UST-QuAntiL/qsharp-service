import marshmallow as ma
from flask import Response


class TranspilationResponse:
    def __init__(self, t_depth, number_of_cnots, width, number_of_measurement_operations, qsharp_string, traced_qsharp):
        self.t_depth = t_depth
        self.number_of_cnots = number_of_cnots
        self.width = width
        self.number_of_measurement_operations = number_of_measurement_operations
        self.qsharp_string = qsharp_string
        self.traced_qsharp = traced_qsharp

    def to_json(self):
        json_response = {'t-depth': self.t_depth,
                         'number-of-cnots': self.number_of_cnots,
                         'width': self.width,
                         'number-of-measurement-operations': self.number_of_measurement_operations,
                         'qsharp-string': self.qsharp_string,
                         'traced-qsharp': self.traced_qsharp
                         }
        return json_response


class ExecutionResponse(Response):
    def __init__(self, location):
        super().__init__()
        self.location = location

    def to_json(self):
        json_response = {'Location': self.location}
        return json_response


class ResultResponse:
    def __init__(self, id, complete, result=None, backend=None, shots=None):
        self.id = id
        self.complete = complete
        self.result = result
        self.backend = backend
        self.shots = shots

    def to_json(self):
        if self.result and self.backend and self.shots:
            return {'id': self.id, 'complete': self.complete, 'result': self.result,
                    'backend': self.backend, 'shots': self.shots}
        else:
            return {'id': self.id, 'complete': self.complete}


class TranspilationResponseSchema(ma.Schema):
    t_depth = ma.fields.Integer()
    number_of_cnots = ma.fields.Integer()
    width = ma.fields.Integer()
    number_of_measurement_operations = ma.fields.Integer()
    qsharp_string = ma.fields.String()
    traced_qsharp = ma.fields.Mapping()


class ExecutionResponseSchema(ma.Schema):
    location = ma.fields.String()


class ResultResponseSchema(ma.Schema):
    id = ma.fields.UUID()
    complete = ma.fields.Boolean()
    result = ma.fields.Mapping()
    backend = ma.fields.String()
    shots = ma.fields.Integer()
