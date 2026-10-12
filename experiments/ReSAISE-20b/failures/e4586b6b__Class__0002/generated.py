# SPDX-License-Identifier: MIT
"""
Vehicle attribute updater.

This module provides a single function, `update_vehicle_attributes`, which
updates an automobile dictionary with new values while strictly enforcing a
whitelist of modifiable fields defined in `ALLOWED_FIELDS`.  The function
creates and returns a new dictionary, leaving the original input unchanged,
to avoid unintended side effects.

Security Note
-------------
The implementation follows best practices to mitigate CWE‑913 (Improper
Control of Dynamically-Managed Code Resources):
* No dynamic code execution (`exec`/`eval`) is performed.
* Only keys present in `ALLOWED_FIELDS` are considered for update,
  preventing accidental or malicious modification of other fields.
* The function is pure: it does not mutate the input dictionaries.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",          # Vehicle Identification Number
    "engine_type",
    "transmission",
    "fuel_efficiency",
]

def update_vehicle_attributes(automobile: dict, changes: dict) -> dict:
    """
    Return a new dictionary with updates applied to the vehicle attributes.

    Parameters
    ----------
    automobile : dict
        Current state of the vehicle's attributes.
    changes : dict
        Proposed changes; keys are field names, values are new values.

    Returns
    -------
    dict
        A new dictionary containing the original vehicle data with any valid
        updates applied.

    Raises
    ------
    TypeError
        If either `automobile` or `changes` is not a dictionary.
    ValueError
        If `changes` contains keys that are not in `ALLOWED_FIELDS`.

    Notes
    -----
    * The function does **not** modify the input dictionaries.
    * Only keys listed in `ALLOWED_FIELDS` may be updated.  Attempting to
      update disallowed fields results in a ``ValueError``.
    """
    if not isinstance(automobile, dict):
        raise TypeError("`automobile` must be a dictionary.")
    if not isinstance(changes, dict):
        raise TypeError("`changes` must be a dictionary.")

    # Identify any disallowed keys
    invalid_keys = set(changes) - set(ALLOWED_FIELDS)
    if invalid_keys:
        raise ValueError(
            f"Attempted to modify disallowed fields: {sorted(invalid_keys)}"
        )

    # Create a shallow copy to avoid mutating the original
    updated = automobile.copy()

    # Apply allowed changes
    for key, value in changes.items():
        updated[key] = value

    return updated