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
from time import sleep

import qsharp
from qsharp import QSharpCallable

def delete_token():
    """Delete account."""
    pass


def transpile(circuit):
    comp: QSharpCallable = qsharp.compile(circuit)
    # In the case of multiple callables, only return the first one
    if hasattr(comp, '__len__'):
        comp = comp[-1]
    return comp


def _prepare_deplarization_noise(p_single, p_multiple, p_measure):
    """Prepares a depolarisation noise model for the noise simulator"""
    noise = qsharp.get_noise_model_by_name("ideal")
    p_single = 1-p_single
    p_multiple = 1-p_multiple
    p_measure = 1-p_measure
    noise.h.post = qsharp.depolarizing_process(p_single)
    noise.x.post = qsharp.depolarizing_process(p_single)
    noise.y.post = qsharp.depolarizing_process(p_single)
    noise.z.post = qsharp.depolarizing_process(p_single)
    noise.i.post = qsharp.depolarizing_process(p_single)
    noise.cnot.post = qsharp.depolarizing_process(p_multiple)
    noise.rx.post = qsharp.depolarizing_process(p_single)
    noise.ry.post = qsharp.depolarizing_process(p_single)
    noise.rz.post = qsharp.depolarizing_process(p_single)
    noise.s.post = qsharp.depolarizing_process(p_single)
    noise.s_adj.post = qsharp.depolarizing_process(p_single)
    noise.t.post = qsharp.depolarizing_process(p_single)
    noise.t_adj.post = qsharp.depolarizing_process(p_single)
    noise.z_meas = qsharp.depolarizing_process(p_measure)
    return noise


def execute_job(transpiled_circuit, shots, p_single, p_multiple, p_measure, params=None):
    """Simulate Job on simulator and return results"""
    counts = {}
    qsharp.set_noise_model(_prepare_deplarization_noise(p_single, p_multiple, p_measure))
    for i in range(shots):
        if not params:
            result = transpiled_circuit.simulate_noise()
        else:
            result = transpiled_circuit.simulate_noise(**params)
        key = "".join(map(str, result))
        counts[key] = counts.setdefault(key, 0) + 1
    return counts


if __name__ == '__main__':
    circuit = """
                open Microsoft.Quantum.Canon;
                open Microsoft.Quantum.Intrinsic;
                open Microsoft.Quantum.Measurement;

                operation Circuit(): Result[] {
                    mutable r = [Zero, Zero];
                    use q0 = Qubit[2] {
                        H(q0[0]);
                        CX(q0[0], q0[1]);
                        R1(1.5707963267948966, q0[1]);
                        T(q0[0]);
                        Controlled Rx([q0[0]], (5.16920185242945, q0[1]));
                        set r w/= 0 <- M(q0[0]);
                        set r w/= 1 <- M(q0[1]);
                        return r;
                    }
                }
            """
    comp = qsharp.compile(circuit)
    if hasattr(comp, '__len__'):
        comp = comp[-1]
    trace = comp.trace()
    print(trace)
    print(comp.estimate_resources(default_gate_time=1))
