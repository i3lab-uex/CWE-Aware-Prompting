# update_product_attributes.py

from typing import Dict, Any


# List of fields that are allowed to be updated
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]


def update_product_attributes(item: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with the provided updates.

    Only keys listed in PERMITTED_FIELDS are allowed to be updated.
    Any attempt to modify a non‑permitted field will raise a ValueError.

    Parameters
    ----------
    item : dict
        The original product dictionary.
    updates : dict
        A dictionary of key/value pairs representing the desired updates.

    Returns
    -------
    dict
        A new dictionary containing the updated product data.

    Raises
    ------
    ValueError
        If any key in `updates` is not in PERMITTED_FIELDS.
    """
    # Validate that all update keys are permitted
    invalid_keys = set(updates) - set(PERMITTED_FIELDS)
    if invalid_keys:
        raise ValueError(
            f"Attempted to update disallowed fields: {', '.join(sorted(invalid_keys))}"
        )

    # Create a shallow copy to avoid mutating the original dictionary
    updated_item = dict(item)

    # Apply updates
    for key, value in updates.items():
        updated_item[key] = value

    return updated_item