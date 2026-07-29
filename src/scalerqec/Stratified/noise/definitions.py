"""Definitions used in this module."""

from __future__ import annotations

STIM_SQGS = {
    "H",
    "X",
    "Y",
    "Z",
    "S",
    "S_DAG",
    "SQRT_X",
    "C_XYZ",
    "C_ZYX",
    "H_XY",
    "H_XZ",
    "H_YZ",
    "SQRT_X_DAG",
    "SQRT_Y",
    "SQRT_Y_DAG",
    "SQRT_Z",
    "SQRT_Z_DAG",
}
STIM_TQGS = {
    "CNOT",
    "CX",
    "CXSWAP",
    "CY",
    "CZ",
    "CZSWAP",
    "ISWAP",
    "ISWAP_DAG",
    "SQRT_XX",
    "SQRT_XX_DAG",
    "SQRT_YY",
    "SQRT_YY_DAG",
    "SQRT_ZZ",
    "SQRT_ZZ_DAG",
    "SWAP",
    "SWAPCX",
    "SWAPCZ",
    "XCX",
    "XCY",
    "XCZ",
    "YCX",
    "YCY",
    "YCZ",
    "ZCX",
    "ZCY",
    "ZCZ",
}
STIM_MEASUREMENT_RESETS = {"MR", "MRX", "MRY", "MRZ"}
STIM_MEASUREMENTS = {"M", "MX", "MY", "MZ"}
STIM_RESETS = {"R", "RX", "RY", "RZ"}
