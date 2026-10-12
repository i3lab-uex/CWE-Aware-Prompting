import copy
from typing import Dict, Any

# Global list of fields that are allowed to be modified.
ALLOWED_FIELDS = ["make", "model", "year", "color", "vin"]

def modify_vehicle_data(vehicle_info: Dict[str, Any],
                        changes_to_apply: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new dictionary with updates applied to `vehicle_info` for
    fields listed in the global ``ALLOWED_FIELDS`` list.

    Parameters
    ----------
    vehicle_info : dict
        Original dictionary containing vehicle attributes.
    changes_to_apply : dict
        Dictionary of fields to update with new values.

    Returns
    -------
    dict
        A copy of ``vehicle_info`` with the permitted changes applied.

    Raises
    ------
    ValueError
        If ``changes_to_apply`` contains a key not in ``ALLOWED_FIELDS``.
    TypeError
        If either argument is not a mapping type.

    Notes
    -----
    * The function makes a deep copy of ``vehicle_info`` so that the original
      dictionary is not mutated.
    * Only keys listed in ``ALLOWED_FIELDS`` are considered; all others raise
      an exception to avoid unintended side‑effects.
    """
    # Validate argument types
    if not isinstance(vehicle_info, dict):
        raise TypeError("vehicle_info must be a dictionary")
    if not isinstance(changes_to_apply, dict):
        raise TypeError("changes_to_apply must be a dictionary")

    # Defensive copy to avoid modifying the caller's data
    updated = copy.deepcopy(vehicle_info)

    for key, new_value in changes_to_apply.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{key}' is not allowed to be modified")
        updated[key] = new_value

    return updated