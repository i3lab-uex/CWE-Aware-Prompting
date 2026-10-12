from __future__ import annotations

from typing import Dict, Iterable, Any

# --------------------------------------------------------------------------- #
# Global list of fields that are allowed to be updated.
# Add or remove field names here as the vehicle schema evolves.
# --------------------------------------------------------------------------- #
ALLOWED_FIELDS: list[str] = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "owner_id",
]

# --------------------------------------------------------------------------- #
# Exception raised when an attempt is made to modify a disallowed attribute.
# --------------------------------------------------------------------------- #
class DisallowedFieldError(KeyError):
    """Raised when a modification attempts to set a field that is not allowed."""


def modify_vehicle_data(
    vehicle_info: Dict[str, Any],
    modifications: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Return a new dictionary containing the vehicle data updated with
    *modifications*, but only for attributes listed in :data:`ALLOWED_FIELDS`.

    Parameters
    ----------
    vehicle_info:
        Dictionary representing the current state of a vehicle.
    modifications:
        Dictionary mapping attribute names to new values.

    Returns
    -------
    dict[str, Any]
        A shallow copy of *vehicle_info* with the allowed modifications applied.

    Raises
    ------
    DisallowedFieldError
        If *modifications* contains any key not in :data:`ALLOWED_FIELDS`.
    TypeError
        If either argument is not a dictionary.
    """
    if not isinstance(vehicle_info, dict):
        raise TypeError(f"vehicle_info must be a dict, got {type(vehicle_info).__name__}")
    if not isinstance(modifications, dict):
        raise TypeError(f"modifications must be a dict, got {type(modifications).__name__}")

    # Create a shallow copy so the caller's data is not mutated unexpectedly.
    updated_vehicle = vehicle_info.copy()

    for field, value in modifications.items():
        if field not in ALLOWED_FIELDS:
            raise DisallowedFieldError(
                f"Attempted to modify disallowed field '{field}'. "
                f"Allowed fields are: {sorted(ALLOWED_FIELDS)}"
            )
        updated_vehicle[field] = value

    return updated_vehicle