open Microsoft.Quantum.Canon;
open Microsoft.Quantum.Intrinsic;
open Microsoft.Quantum.Measurement;

operation Circuit(a : Double): Result[] {
    mutable r = [Zero, Zero];
    use q0 = Qubit[2] {
        H(q0[0]);
        CX(q0[0], q0[1]);
        R1(a, q0[1]);
        T(q0[0]);
        Controlled Rx([q0[0]], (5.16920185242945, q0[1]));
        set r w/= 0 <- M(q0[0]);
        set r w/= 1 <- M(q0[1]);
        return r;
    }
}
