# edit_product_info.py

"""
This module provides a single function `edit_product_info` that safely updates
product attributes.  Only fields listed in the global `PERMITTED_FIELDS`
constant are allowed to be modified.  The function raises a ValueError
whenever an attempt is made to modify a non‑permitted field.

The implementation deliberately avoids any form of dynamic code execution
(CWE-913) by using explicit dictionary operations only.
"""

from typing import Dict, Any

# Only these keys are allowed to be modified
PERMITTED_FIELDS = {"price", "description", "stock", "category"}


def edit_product_info(item: Dict[str, Any], details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with the supplied details.

    Parameters
    ----------
    item : dict
        The original product information.  This dictionary will be modified in place.
    details : dict
        A mapping of field names to new values.  Only keys present in
        `PERMITTED_FIELDS` will be applied.

    Returns
    -------
    dict
        The updated product dictionary (the same object that was passed in).

    Raises
    ------
    ValueError
        If `details` contains any key that is not in `PERMITTED_FIELDS`.
    """
    # Ensure we only accept permitted fields
    for key in details:
        if key not in PERMITTED_FIELDS:
            raise ValueError(
                f"Field '{key}' is not allowed to be updated. "
                f"Permitted fields: {sorted(PERMITTED_FIELDS)}"
            )

    # Apply updates
    item.update(details)

    return item


# Example usage (for testing only; remove or comment out in production)
if __name__ == "__main__":
    product = {
        "id": 123,
        "price": 19.99,
        "description": "A wonderful gadget",
        "stock": 50,
        "category": "Electronics",
    }

    updates = {"price": 17.99, "stock": 45}
    updated_product = edit_product_info(product, updates)
    print(updated_product)