from stim import Circuit
from .definitions import STIM_MEASUREMENTS, STIM_RESETS, STIM_SQGS, STIM_TQGS, STIM_MEASUREMENT_RESETS

class NoiseModel:
    """Class representing a noise model for a quantum circuit."""

    def __init__(self, ideal_qubits: set[int] | None = None) -> None:
        """Initialize the noise model.

        Args:
           ideal_qubits: Set of qubit indices that are ideal (not subject to noise).
        """
        self.ideal_qubits = ideal_qubits or set()

    def _apply_noise(self, circ: Circuit, op: str, targets: list[int], p: float) -> None:
        """Apply noise to the circuit only if the targets are not ideal qubits.

        If any of the targets are in the set of ideal qubits, the noise operation is not applied to those targets.

        Args:
           circ: The circuit to which the noise is applied.
           op: The noise operation (e.g., "DEPOLARIZE1").
           targets: List of qubit indices to apply the noise to.
           p: Probability of the noise operation.
        """
        assert targets, "Targets cannot be empty."

        any_ideal = any(t in self.ideal_qubits for t in targets)
        if not any_ideal:
            circ.append_operation(op, targets, p)
            
class CircuitLevelNoise(NoiseModel):
    """Class representing circuit-level noise.

    The following noise model is applied to the circuit:
        - Qubit initialization flips with probability p_init (depolaring noise after initialization).
        - Measurements flip with probability p_meas (depolarizing noise before measuring).
        - Single-qubit gates are subject to depolarizing noise of strength p_sqg.
        - Two-qubit gates are subject to depolarizing noise of strength p_tqg.
    """

    def __init__(
        self, p_tqg: float, p_sqg: float, p_meas: float, p_init: float, ideal_qubits: set[int] | None = None
    ) -> None:
        """Initialize the circuit-level noise model.

        Args:
            p_tqg: Probability of depolarizing noise for two-qubit gates.
            p_sqg: Probability of depolarizing noise for single-qubit gates.
            p_meas: Probability of depolarizing noise for measurements.
            p_init: Probability of depolarizing noise after initialization.
            ideal_qubits: Set of qubit indices that are ideal (not subject to noise).
        """
        super().__init__(ideal_qubits)
        self.p_tqg = p_tqg
        self.p_sqg = p_sqg
        self.p_meas = p_meas
        self.p_init = p_init

    def apply(self, circ: Circuit) -> Circuit:
        """Apply the noise model to a stim circuit."""
        noisy_circ = Circuit()

        for op in circ:
            name = op.name
            if name in STIM_SQGS:
                for targets in op.target_groups():
                    noisy_circ.append_operation(op.name, targets)
                    self._apply_noise(noisy_circ, "DEPOLARIZE1", [trgt.qubit_value for trgt in targets], self.p_sqg)

            elif name in STIM_RESETS:
                for targets in op.target_groups():
                    noisy_circ.append_operation(op.name, targets)
                    noisy_circ.append("Z_ERROR" if op.name.endswith("X") else "X_ERROR", targets, self.p_meas)

            elif name in STIM_TQGS:
                for targets in (
                    op.target_groups()
                ):  # errors might propagate so we have to apply noise to every target group individually
                    noisy_circ.append_operation(op.name, targets)
                    self._apply_noise(noisy_circ, "DEPOLARIZE2", [trgt.qubit_value for trgt in targets], self.p_tqg)

            elif name in STIM_MEASUREMENTS:
                for targets in op.target_groups():
                    if not any(t in self.ideal_qubits for t in [trgt.qubit_value for trgt in targets]):
                        noisy_circ.append("Z_ERROR" if op.name.endswith("X") else "X_ERROR", targets, self.p_meas)
                        noisy_circ.append_operation(op.name, targets)
                    else:
                        noisy_circ.append_operation(op.name, targets)
            elif name in STIM_MEASUREMENT_RESETS:
                for targets in op.target_groups():
                    if not any(t in self.ideal_qubits for t in [trgt.qubit_value for trgt in targets]):
                        noisy_circ.append("Z_ERROR" if op.name.endswith("X") else "X_ERROR", targets, self.p_meas)
                        noisy_circ.append_operation(op.name, targets)
                        noisy_circ.append("Z_ERROR" if op.name.endswith("X") else "X_ERROR", targets, self.p_meas)
                    else:
                        noisy_circ.append_operation(op.name, targets)
            else:
                noisy_circ.append_operation(op)
        return noisy_circ
