#!/usr/bin/python
import cmath
from math import inf, log10, pi, sqrt

LIGHTSPEED = 299792458
VACUUM_PERMEABILITY = 4 * pi * 1e-7
VACUUM_PERMITIVITY = 1 / (VACUUM_PERMEABILITY * LIGHTSPEED ** 2)


def _qdrt(x: float) -> float:
    return sqrt(sqrt(x))


def radar_max_range(
    transmitting_power: float,
    gain: float,
    cross_section: float,
    freq: float,
    sensitivity: float,
) -> float:

    wavelength = LIGHTSPEED / freq
    return _qdrt(
        (transmitting_power * gain ** 2 * cross_section * wavelength ** 2)
        / ((4 * pi) ** 3 * sensitivity)
    )


def reflection(
    source: [float, complex] = None,
    load: [float, complex] = None,
    vswr: float = None,
) -> complex:
    if source or load and not vswr:
        if load == inf:
            return 1.0
        return abs((load - source) / (load + source))
    if vswr and not (source or load):
        return (vswr - 1) / (vswr + 1)
    raise Exception


def return_loss(reflection: float) -> float:
    if reflection == 0:
        return inf
    return -20 * log10(reflection)


def vswr(
    source: [float, complex] = None,
    load: [float, complex] = None,
    reflection: float = None,
) -> complex:
    if (source or load) and not reflection:
        if load == 0:
            return inf
        return (abs(load + source) + abs(load - source)) / (
            abs(load + source) - abs(load - source)
        )
    if vswr and not (source or load):
        return (1 + reflection) / (1 - reflection)
    raise Exception


def phase_constant_from_wavelength(wavelength: float) -> float:
    return 2 * pi / wavelength


def wavelength(freq: float = None, phase_constant: float = None) -> float:
    if freq and not phase_constant:
        return LIGHTSPEED / freq
    if phase_constant and not freq:
        return 2 * pi / phase_constant


def propagation_coefficient(
    freq: float, R: float, L: float, G: float, C: float
) -> float:
    circ_freq = 2 * pi * freq
    return cmath.sqrt((R + 1j * circ_freq * L) * (G + 1j * circ_freq * C))


def phase_velocity(
    circ_freq: float = None,
    phase_constant: float = None,
    inductance: float = None,
    capacitance: float = None,
) -> float:
    if not (circ_freq is None or phase_constant is None):
        return circ_freq / phase_constant
    if not (inductance is None or capacitance is None):
        return 1 / sqrt(inductance * capacitance)
    raise Exception


if __name__ == "__main__":
    max_range = radar_max_range(10e3, 14e3, 1, 10e9, 1e-13)
    print(f"{max_range:.0f}")
