from typing import Dict, Any

# Define which vehicle attributes can be updated
ALLOWED_FIELDS = {"make", "model", "year", "color", "vin"}

def update_vehicle_attributes(automobile: Dict[str, Any], changes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update the provided `automobile` dictionary with key/value pairs from
    `changes`, but only for keys that are present in the global
    ALLOWED_FIELDS set.

    Parameters
    ----------
    automobile : dict
        The original vehicle attributes.
    changes : dict
        Dictionary containing the fields to update.

    Returns
    -------
    dict
        The updated vehicle dictionary. The original dictionary is not modified.

    Raises
    ------
    ValueError
        If any key in `changes` is not allowed to be updated.
    """
    # Validate input types
    if not isinstance(automobile, dict):
        raise TypeError("`automobile` must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("`changes` must be a dictionary")

    # Ensure that all requested changes are allowed
    invalid_keys = set(changes) - ALLOWED_FIELDS
    if invalid_keys:
        raise ValueError(
            f"Attempted to update disallowed fields: {', '.join(sorted(invalid_keys))}"
        )

    # Create a shallow copy to avoid mutating the original
    updated = automobile.copy()
    for key, value in changes.items():
        updated[key] = value

    return updated