"""Victim circuits: each one carries a secret that is somebody's IP."""
import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import efficient_su2


def _phase_flip(qc, bits):
    """Flip the phase of basis state |bits> (Qiskit order: bits[-1] is qubit 0)."""
    n = qc.num_qubits
    zeros = [q for q in range(n) if bits[n - 1 - q] == "0"]
    if zeros:
        qc.x(zeros)
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    if zeros:
        qc.x(zeros)


def grover(marked="101"):
    """Grover search. Secret = the marked bitstring."""
    n = len(marked)
    qc = QuantumCircuit(n, name=f"grover-{n}")
    qc.h(range(n))
    for _ in range(int(np.pi / 4 * np.sqrt(2**n))):
        _phase_flip(qc, marked)
        qc.h(range(n))
        _phase_flip(qc, "0" * n)
        qc.h(range(n))
    qc.measure_all()
    qc.metadata = {"secret": marked, "kind": "marked item"}
    return qc


def qaoa_maxcut(edges=((0, 1), (1, 2), (2, 3), (3, 0), (0, 2)), n=4, gamma=2.85, beta=0.30):
    """One-layer QAOA for MaxCut. Secret = the graph and the trained angles.

    Default angles maximise the expected cut on the default graph (3.24 of 4), so the
    output is peaked on the optimal cuts 0101/1010 instead of near-uniform.
    """
    qc = QuantumCircuit(n, name=f"qaoa-{n}")
    qc.h(range(n))
    for a, b in edges:
        qc.rzz(2 * gamma, a, b)
    qc.rx(2 * beta, range(n))
    qc.measure_all()
    qc.metadata = {"secret": {"edges": [list(e) for e in edges], "gamma": gamma, "beta": beta},
                   "kind": "graph + trained angles"}
    return qc


def vqe_ansatz(n=4, reps=2, seed=11):
    """Hardware-efficient ansatz with 'trained' weights. Secret = the weights."""
    ansatz = efficient_su2(n, reps=reps)
    weights = np.random.default_rng(seed).uniform(-np.pi, np.pi, ansatz.num_parameters)
    qc = ansatz.assign_parameters(weights)
    qc.name = f"vqe-{n}"
    qc.measure_all()
    qc.metadata = {"secret": [round(float(w), 4) for w in weights], "kind": "trained weights"}
    return qc


DEMOS = {"Grover search (marked item)": grover,
         "QAOA MaxCut (graph + angles)": qaoa_maxcut,
         "VQE ansatz (trained weights)": vqe_ansatz}

# The same circuits with other secrets: score.secret_blind checks the locked view never changes.
# (QAOA: angles only. Its graph is structure, hidden statistically by padding, not exactly.)
VARIANTS = {"Grover search (marked item)": lambda: [grover(format(i, "03b")) for i in range(8)],
            "QAOA MaxCut (graph + angles)": lambda: [qaoa_maxcut(gamma=g, beta=b)
                                                     for g, b in ((2.85, 0.30), (0.8, 0.4), (1.9, 1.1))],
            "VQE ansatz (trained weights)": lambda: [vqe_ansatz(seed=s) for s in range(8)]}
