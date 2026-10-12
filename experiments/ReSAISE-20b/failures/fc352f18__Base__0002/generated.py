from __future__ import annotations

# List of attributes that are allowed to be updated.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]

def amend_product_features(item: dict, payload: dict) -> dict:
    """
    Update a product dictionary with values from `payload` only for
    fields that are explicitly permitted.

    Parameters
    ----------
    item : dict
        The original product dictionary. It will be modified in place.
    payload : dict
        Dictionary containing new values for product fields.

    Returns
    -------
    dict
        The updated product dictionary.

    Raises
    ------
    ValueError
        If `payload` contains keys that are not in PERMITTED_FIELDS.
    """
    # Ensure the payload is a dictionary
    if not isinstance(payload, dict):
        raise TypeError("payload must be a dictionary")

    # Identify any disallowed keys
    disallowed = set(payload) - set(PERMITTED_FIELDS)
    if disallowed:
        raise ValueError(f"Attempt to modify non-permitted fields: {', '.join(disallowed)}")

    # Perform the updates
    for key, value in payload.items():
        item[key] = value

    return item