# update_product_attributes.py

from typing import Dict, Any

# Global list of fields that are allowed to be updated.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def update_product_attributes(item: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with the provided updates.

    Only keys that are present in PERMITTED_FIELDS will be applied.
    If an update contains a key that is not permitted, a ValueError
    will be raised.

    Args:
        item: The original product dictionary.
        updates: A dictionary of fields to update.

    Returns:
        A new dictionary with the applied updates.
    """
    # Validate that all update keys are permitted
    disallowed = set(updates) - set(PERMITTED_FIELDS)
    if disallowed:
        raise ValueError(f"Attempted to update non‑permitted fields: {', '.join(disallowed)}")

    # Create a shallow copy to avoid mutating the original
    updated_item = dict(item)

    # Apply updates
    for key, value in updates.items():
        updated_item[key] = value

    return updated_item