# cirq-service

This service takes a Cirq implementation as data or via an URL and returns either compiled circuit properties and the transpiled Quil String (Transpilation Request) or its results (Execution Request) depending on the input data and selected backend.


[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## Setup
* Clone repository:
```
git clone https://github.com/KuhnMn/cirq-service.git
```

* Start containers:
```
docker-compose pull
docker-compose up
```

Now the cirq-service is available on http://localhost:5018/.

## After implementation changes
* Update container:
```
docker build -t kuhnmx/cirq-service:latest
docker push kuhnmx/cirq-service:latest
```

* Start containers:
```
docker-compose pull
docker-compose up
```

## Transpilation Request
Send implementation and QPU information to the API to get properties of the transpiled circuit and the transpiled Cirq-JSON circuit itself.
*Note*: Currently, the Cirq package is used for local simulation. Thus, no real backends are accessible.
Inputs are currently also not supported.

`POST /cirq-service/api/v1.0/transpile`

#### Transpilation via data
```
{  
    "impl-data": "BASE64-ENCODED-IMPLEMENTATION",
    "impl-language": "Cirq",
    "qpu-name": "NAME-OF-QPU",
    "input-params": {
    }
}
```

## Execution Request
Send implementation, input, and QPU information to the API to execute your circuit and get the result.
*Note*: Currently, the Cirq package is used for local simulation. Thus, no real backends are accessible.
Inputs are currently also not supported.

`POST /cirq-service/api/v1.0/execute`  


#### Execution via data
```
{  
    "impl-data": "BASE64-ENCODED-IMPLEMENTATION",
    "impl-language": "Cirq",
    "qpu-name": "NAME-OF-QPU",
    "input-params": {
    }
}
```
#### Execution via transpiled Cirq-JSON String
Note that the JSON has to be sent in form of a single string.
```
{  
    "transpiled-cirq": "TRANSPILED-CIRQ-JSON-STRING",
    "qpu-name": "NAME-OF-QPU"
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
