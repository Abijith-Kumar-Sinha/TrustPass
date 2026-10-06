"""One scorecard for every run: confidentiality, integrity, quality and cost side by side.

Rahman, Haghparast & Mikkonen (2026) point out that obfuscation papers each invent
their own metric (TVD, DFC, ...) so results can't be compared. We report one fixed set,
and test wrong keys on random input states, not only |0...0> (the gap CLOAQ, 2026, flags).

The wrong-key numbers only show that the key controls the function: every qubit ends in a
fully keyed block, so a random key looks random for ANY lock and cannot reveal a leak. The
checks that can fail are structural: nothing but key symbols leaves, every qubit pair
carries the same CX count, and (secret_blind) the view is identical for every secret.
"""
import itertools
from collections import Counter

import numpy as np
from qiskit import transpile
from qiskit.quantum_info import Statevector, random_statevector

from lock import lock, random_key, unlock


def _probs(circ, init=None):
    body = circ.remove_final_measurements(inplace=False)
    sv = init if init is not None else Statevector.from_int(0, 2**body.num_qubits)
    return sv.evolve(body).probabilities()


def _tvd(p, q):
    return float(0.5 * np.abs(p - q).sum())


def view(circ):
    """Everything the compiler sees besides key symbols: gate names and unordered qubit sets."""
    return tuple((i.operation.name, frozenset(circ.find_bit(q).index for q in i.qubits)) for i in circ.data)


def secret_blind(variants, seed=0):
    """Lock the same circuit with every possible secret: is the compiler's view always identical?

    The lock's randomness is held fixed (a test-only seed) so that only the secret varies:
    if the view still never changes, the secret has no influence on what the compiler sees.
    """
    return len({view(lock(v, seed=seed).circuit) for v in variants}) == 1


def confidentiality(original, locked, guesses=30, inputs=5, seed=0):
    """Key sanity (wrong keys give unrelated outputs) plus the structural leak guards."""
    rng = np.random.default_rng(seed)
    n = original.num_qubits
    true0 = _probs(original)
    states = [random_statevector(2**n, seed=int(s)) for s in rng.integers(2**31, size=inputs)]
    true_r = [_probs(original, s) for s in states]
    zero_in, rand_in = [], []
    for _ in range(guesses):
        guess = unlock(locked.circuit, random_key(locked, seed=int(rng.integers(2**31))))
        p0 = _probs(guess)
        zero_in.append(_tvd(p0, true0))
        rand_in.append(np.mean([_tvd(_probs(guess, s), t) for s, t in zip(states, true_r)]))
    # Reference: how far off is a guess that knows *nothing* (a random output state)?
    know_nothing = np.mean([_tvd(random_statevector(2**n, seed=int(s)).probabilities(), t)
                            for t in true_r for s in rng.integers(2**31, size=4)])
    all_zero = unlock(locked.circuit, {p: 0.0 for p in locked.key})
    lc = locked.circuit
    per_pair = Counter(frozenset(lc.find_bit(q).index for q in i.qubits) for i in lc.data if i.operation.name == "cx")
    pairs = [frozenset(p) for p in itertools.combinations(range(n), 2)]
    two_q = sum(per_pair.values())
    return {
        "key_angles": len(locked.key),
        "know_nothing_tvd": round(float(know_nothing), 3),
        "indistinguishability": round(float(min(1.0, np.mean(rand_in) / know_nothing)), 3),
        # Structural regression guards (necessary, not sufficient, for hiding):
        "metadata_clean": not lc.metadata and lc.name == "locked",
        "pair_count_spread": max(per_pair[p] for p in pairs) - min(per_pair[p] for p in pairs) if pairs else 0,
        "visible_2q_gates": two_q,
        "decoy_share_of_2q": round(2 * locked.decoys / two_q, 3) if two_q else 0.0,
        "wrong_key_tvd_zero_input": round(float(np.mean(zero_in)), 3),
        "wrong_key_tvd_random_inputs": round(float(np.mean(rand_in)), 3),
        "zero_key_tvd": round(_tvd(_probs(all_zero), true0), 3),
        "luckiest_guess_similarity": round(1 - min(zero_in), 3),
    }


def overhead(original, locked, backend, seed=7):
    """What locking costs after compilation, versus compiling the plain circuit."""
    plain = transpile(original, backend, optimization_level=3, seed_transpiler=seed)
    lockd = transpile(locked.circuit, backend, optimization_level=3, seed_transpiler=seed)
    two = lambda c: sum(v for k, v in c.count_ops().items() if k in ("cx", "cz", "ecr"))
    return {"2q_plain": two(plain), "2q_locked": two(lockd),
            "depth_plain": plain.depth(), "depth_locked": lockd.depth()}


def trust(functional, fidelity, conf):
    """Pillars on 0-100 plus a single accept/reject verdict."""
    # 100 = wrong-key guesses are no closer than a random circuit AND the structural guards hold;
    # a leaky skeleton or metadata caps it. I/O-observing attackers are out of scope.
    cap = 0 if not conf["metadata_clean"] else 50 if conf["pair_count_spread"] else 100
    return {
        "confidentiality": min(cap, round(100 * conf["indistinguishability"])),
        "integrity": 100 if functional["passed"] else 0,
        "quality": round(100 * min(1.0, fidelity["ratio"])),
        "verdict": "ACCEPT" if functional["passed"] and fidelity["passed"] else "REJECT",
    }
