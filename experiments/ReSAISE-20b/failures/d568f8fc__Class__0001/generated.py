# -*- coding: utf-8 -*-

from typing import Dict, Any

# Global list of fields that are allowed to be updated
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def adjust_product_data(prod_info: Dict[str, Any], change_vals: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with new values while only allowing changes to
    fields specified in the global PERMITTED_FIELDS list.

    Parameters
    ----------
    prod_info : dict
        The original product data.  This dictionary will not be modified in place.
    change_vals : dict
        A mapping of field names to new values that should be applied.

    Returns
    -------
    dict
        A new dictionary containing the updated product data.

    Raises
    ------
    ValueError
        If any key in ``change_vals`` is not present in PERMITTED_FIELDS.
    """
    # Create a shallow copy to avoid side‑effects on the original dict
    updated_product = prod_info.copy()

    for field, new_value in change_vals.items():
        if field not in PERMITTED_FIELDS:
            raise ValueError(f"Field '{field}' is not permitted for update.")
        updated_product[field] = new_value

    return updated_product