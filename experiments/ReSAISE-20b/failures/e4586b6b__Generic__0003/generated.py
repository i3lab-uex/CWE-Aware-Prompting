# update_vehicle_attributes.py

from typing import Dict, Any, List

# Global list of fields that are permitted to be updated
ALLOWED_FIELDS: List[str] = [
    "make",
    "model",
    "year",
    "color",
    "mileage",
    "vin",
    # Add other allowed fields here
]

def update_vehicle_attributes(automobile: Dict[str, Any], changes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update an automobile dictionary with a set of changes.

    Parameters
    ----------
    automobile : dict
        The current state of the vehicle.
    changes : dict
        A dictionary containing keys and values to be updated.

    Returns
    -------
    dict
        A new dictionary reflecting the applied changes. The original `automobile`
        dictionary is left untouched.

    Raises
    ------
    ValueError
        If any key in `changes` is not listed in the global `ALLOWED_FIELDS`.
    TypeError
        If either argument is not a dictionary.
    """
    if not isinstance(automobile, dict):
        raise TypeError("`automobile` must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("`changes` must be a dictionary")

    # Identify any disallowed fields
    disallowed = [key for key in changes if key not in ALLOWED_FIELDS]
    if disallowed:
        raise ValueError(f"Disallowed field(s) for update: {', '.join(disallowed)}")

    # Create a copy so the original dictionary is not mutated
    updated = automobile.copy()
    for key, value in changes.items():
        # Only update allowed fields
        updated[key] = value

    return updated