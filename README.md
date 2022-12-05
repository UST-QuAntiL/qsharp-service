# qsharp-service

This service takes a qsharp implementation as data or via an URL and returns either compiled circuit properties and the traced qsharp compilation (Transpilation Request) or its results (Execution Request) depending on the input data and selected backend.


[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Setup
* Clone repository:
```
git clone https://github.com/KuhnMn/qsharp-service.git
```

* Start containers:
```
docker-compose pull
docker-compose up
```

Now the qsharp-service is available on http://localhost:5022/.

## After implementation changes
* Update container:
```
docker build -t kuhnmx/qsharp-service:latest
docker push kuhnmx/qsharp-service:latest
```

* Start containers:
```
docker-compose pull
docker-compose up
```

## Transpilation Request
Send implementation to the API to get properties of the compiled circuit, as well as the trace tree of the circuit.
The first executable operation found in the code will be transpiled.
In case of QSharp code, and parameters will be inserted on transpilation.
In case of Python code, parameters will be used to call the "get_circuit" method, which is expected to return a QSharp string without parameters.
QSharp only counts "T-Gates" as having a gate time, so the depth only counts "T-Gates".

`POST /qsharp-service/api/v1.0/transpile`

#### Transpilation via URL
```
{  
    "impl-url": "URL-OF-IMPLEMENTATION",
    "impl-language": "QSharp/Python",
    "input-params": {
        "PARAM-NAME-1": {
                "rawValue": "YOUR-VALUE-1",
                "type": "Integer"
            },
            "PARAM-NAME-2": {
                "rawValue": "YOUR-VALUE-2",
                "type": "String"
            },
            ...
    }
}
```

#### Transpilation via data
```
{  
    "impl-data": "BASE64-ENCODED-IMPLEMENTATION",
    "impl-language": "QSharp/Python",
    "input-params": {
        "PARAM-NAME-1": {
                "rawValue": "YOUR-VALUE-1",
                "type": "Integer"
            },
            "PARAM-NAME-2": {
                "rawValue": "YOUR-VALUE-2",
                "type": "String"
            },
            ...
    }
}
```

#### Transpilation via QSharp-String
```
{  
    "qsharp-string": "QSHARP-STRING",
    "impl-language": "QSharp",
    "input-params": {
        "PARAM-NAME-1": {
                "rawValue": "YOUR-VALUE-1",
                "type": "Integer"
            },
            "PARAM-NAME-2": {
                "rawValue": "YOUR-VALUE-2",
                "type": "String"
            },
            ...
    }
}
```

## Execution Request
Send implementation, input, and QPU information to the API to execute your circuit and get the result.
*Note*: Currently, the QSharp only supports local simulation. Thus, no real backends are accessible.
The first executable operation found in the code will be executed.
In case of QSharp code, and parameters will be inserted on execution.
In case of Python code, parameters will be used to call the "get_circuit" method, which is expected to return a QSharp string without parameters.

`POST /qsharp-service/api/v1.0/execute`  

#### Execution via URL
```
{  
    "impl-url": "URL-OF-IMPLEMENTATION",
    "impl-language": "QSharp/Python",
    "shots": "SHOTS",
    "gate-noise": {
        "single-qubit": "SINGLE-QUBIT-GATE-DEPOLARISATION-PROBABILITY",
        "multiple-qubit": "MULTIPLE-QUBIT-GATE-DEPOLARISATION-PROBABILITY",
        "measurement": "MEASUREMENT-GATE-DEPOLARISATION-PROBABILITY"
    },
    "input-params": {
        "PARAM-NAME-1": {
                "rawValue": "YOUR-VALUE-1",
                "type": "Integer"
            },
            "PARAM-NAME-2": {
                "rawValue": "YOUR-VALUE-2",
                "type": "String"
            },
            ...
    }
}
```

#### Execution via data
```
{  
    "impl-data": "BASE64-ENCODED-IMPLEMENTATION",
    "impl-language": "QSharp/Python",
    "shots": "SHOTS",
    "gate-noise": {
        "single-qubit": "SINGLE-QUBIT-GATE-DEPOLARISATION-PROBABILITY",
        "multiple-qubit": "MULTIPLE-QUBIT-GATE-DEPOLARISATION-PROBABILITY",
        "measurement": "MEASUREMENT-GATE-DEPOLARISATION-PROBABILITY"
    },
    "input-params": {
        "PARAM-NAME-1": {
                "rawValue": "YOUR-VALUE-1",
                "type": "Integer"
            },
            "PARAM-NAME-2": {
                "rawValue": "YOUR-VALUE-2",
                "type": "String"
            },
            ...
    }
}
```
#### Execution via QSharp-String
```
{  
    "qsharp-string": "QSHARP-STRING",
    "impl-language": "QSharp",
    "shots": "SHOTS",
    "gate-noise": {
        "single-qubit": "SINGLE-QUBIT-GATE-DEPOLARISATION-PROBABILITY",
        "multiple-qubit": "MULTIPLE-QUBIT-GATE-DEPOLARISATION-PROBABILITY",
        "measurement": "MEASUREMENT-GATE-DEPOLARISATION-PROBABILITY"
    },
    "input-params": {
        "PARAM-NAME-1": {
                "rawValue": "YOUR-VALUE-1",
                "type": "Integer"
            },
            "PARAM-NAME-2": {
                "rawValue": "YOUR-VALUE-2",
                "type": "String"
            },
            ...
    }
}
```

Returns a content location for the result. Access it via `GET`.

## Sample Implementations for Transpilation and Execution
Sample implementations can be found [here](https://github.com/UST-QuAntiL/nisq-analyzer-content/tree/master/compiler-selection/Shor) and under the folder 'Sample Implementations'.
Please use the raw GitHub URL as `impl-url` value (see [example](https://raw.githubusercontent.com/UST-QuAntiL/nisq-analyzer-content/master/compiler-selection/Shor/shor-fix-15-quil.quil)).

## Haftungsausschluss

Dies ist ein Forschungsprototyp.
Die Haftung für entgangenen Gewinn, Produktionsausfall, Betriebsunterbrechung, entgangene Nutzungen, Verlust von Daten und Informationen, Finanzierungsaufwendungen sowie sonstige Vermögens- und Folgeschäden ist, außer in Fällen von grober Fahrlässigkeit, Vorsatz und Personenschäden, ausgeschlossen.

## Disclaimer of Warranty

Unless required by applicable law or agreed to in writing, Licensor provides the Work (and each Contributor provides its Contributions) on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied, including, without limitation, any warranties or conditions of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A PARTICULAR PURPOSE.
You are solely responsible for determining the appropriateness of using or redistributing the Work and assume any risks associated with Your exercise of permissions under this License.
