"""Keyed locking: hide every single-qubit angle before the circuit leaves your machine.

The circuit is rewritten as CX gates plus exactly one keyed block per wire segment,
block = rz(k) sx rz(k') sx rz(k''), every angle a Parameter whose value is the key.
The compiler therefore sees only the CX skeleton, and that skeleton is flattened too:
decoy CX pairs pad every qubit pair to the same CX count, each decoy lands at a uniform
boundary between two-qubit instructions (never inside a real interaction), commuting rzz
runs are shuffled out of the author's order, and every CX gets a random direction (the H
gates that flip it are absorbed into the keyed blocks for free). Unlocking = binding the
key after compilation.

Known limit: decoys are adjacent CX-block-CX pairs, so they hide the graph only when every
real interaction is also such a pair (QAOA's rzz). For lone-CX circuits an attacker can
peel the decoys off; none of the demo secrets live in that skeleton.
"""
import itertools
from collections import Counter
from dataclasses import dataclass

import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.circuit import Parameter
from qiskit.quantum_info import Operator
from qiskit.synthesis import OneQubitEulerDecomposer

_ZSX = OneQubitEulerDecomposer("ZSX")
_H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)


@dataclass
class Locked:
    circuit: QuantumCircuit  # what the untrusted compiler sees
    key: dict                # Parameter -> float; never leaves the user
    decoys: int              # decoy CX pairs inserted


def _flatten(qc, rng):
    """One list of (name, qubits, op) per original instruction, in cx + 1q gates."""
    insts = [i for i in qc.data if i.operation.name not in ("barrier", "measure")]
    k = 0
    while k < len(insts):  # rzz gates commute: shuffle each run so their order isn't the author's
        j = k
        while j < len(insts) and insts[j].operation.name == "rzz":
            j += 1
        insts[k:j] = [insts[k + x] for x in rng.permutation(j - k)]
        k = j + 1
    groups = []
    for inst in insts:
        qs = [qc.find_bit(q).index for q in inst.qubits]
        if len(qs) == 1:
            groups.append([(inst.operation.name, qs, inst.operation)])
            continue
        sub = QuantumCircuit(qc.num_qubits)
        sub.append(inst.operation, qs)
        f = transpile(sub, basis_gates=["u", "cx"], optimization_level=1, seed_transpiler=0)
        groups.append([(i.operation.name, [f.find_bit(q).index for q in i.qubits], i.operation) for i in f.data])
    return groups


def lock(qc, decoys=0, seed=None):
    """decoys = extra padding rounds on top of equalising every pair.

    Leave seed=None in real use: decoy placement must come from OS entropy, never from a
    value the compiler can guess (a public seed lets it replay and subtract the decoys).
    """
    rng = np.random.default_rng(seed)
    groups = _flatten(qc, rng)
    n = qc.num_qubits
    out = qc.copy_empty_like(name="locked")  # no name/metadata: those can carry the secret
    out.metadata = {}
    out.global_phase = 0  # unobservable, and the real value leaks a bit of the secret
    key, pending = {}, [np.eye(2, dtype=complex) for _ in range(n)]

    def rz(angle, q):
        p = Parameter(f"k{len(key):03d}")
        key[p] = float(angle)
        out.rz(p, q)

    def flush(qs):
        for q in qs:
            for inst in _ZSX(pending[q], simplify=False).data:  # always the full rz-sx-rz-sx-rz form
                rz(inst.operation.params[0], q) if inst.operation.name == "rz" else out.sx(q)
            pending[q] = np.eye(2, dtype=complex)

    count = Counter(frozenset(qs) for g in groups for name, qs, _ in g if name == "cx")
    pairs = [frozenset(p) for p in itertools.combinations(range(n), 2)]
    top = max([count[p] for p in pairs] + [0]) + 2 * decoys
    # ponytail: 2-CX decoys can't fix an odd gap; a 3-CX identity gadget could. Refuse rather than leak.
    if any((top - count[p]) % 2 for p in pairs):
        raise ValueError("lock: a qubit pair has an odd CX gap; padding would leave the interaction graph visible")
    inserted = 0
    for p in pairs:
        for _ in range((top - count[p]) // 2):
            two = [i for i, g in enumerate(groups) if any(name == "cx" for name, _, _ in g)]
            s = int(rng.integers(len(two) + 1))  # uniform boundary between two-qubit instructions
            at = 0 if s == 0 else two[s - 1] + 1
            groups[at:at] = [[("cx", sorted(p), None)] * 2]  # CX.CX = I, but locked like any real gate
            inserted += 1

    for name, qs, op in (o for g in groups for o in g):
        if name == "cx":
            a, b = qs
            flip = rng.random() < 0.5  # CX(a,b) = (H x H) CX(b,a) (H x H)
            if flip:
                pending[a], pending[b] = _H @ pending[a], _H @ pending[b]
            flush(qs)
            out.cx(b, a) if flip else out.cx(a, b)
            if flip:
                pending[a], pending[b] = _H.copy(), _H.copy()
        elif len(qs) == 1:
            pending[qs[0]] = Operator(op).data @ pending[qs[0]]
        else:
            raise ValueError(f"lock: unsupported operation {name!r}")
    flush(range(n))

    if any(inst.operation.name == "measure" for inst in qc.data):
        out.barrier()
        for inst in qc.data:
            if inst.operation.name == "measure":
                out.append(inst)
    return Locked(out, key, inserted)


def unlock(compiled, key):
    """Bind the secret key into the compiled circuit."""
    bound = compiled.assign_parameters({p: v for p, v in key.items() if p in compiled.parameters})
    if bound.parameters:
        raise ValueError(f"unlock: unbound parameters left: {list(bound.parameters)[:5]}")
    return bound


def random_key(locked, seed=None):
    """A wrong key: what an attacker without the key has to guess."""
    rng = np.random.default_rng(seed)
    return {p: float(rng.uniform(-np.pi, np.pi)) for p in locked.key}
