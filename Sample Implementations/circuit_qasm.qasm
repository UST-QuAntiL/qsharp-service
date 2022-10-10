// Generated from Cirq v0.11.1

OPENQASM 2.0;
include "qelib1.inc";


// Qubits: [(4, 1), (5, 1)]
qreg q[2];
creg m_m0[1];
creg m_m[1];
creg m_m2[1];


h q[0];
measure q[1] -> m_m0[0];
rx(pi*0.5) q[1];
cx q[0],q[1];
measure q[1] -> m_m[0];
measure q[0] -> m_m2[0];