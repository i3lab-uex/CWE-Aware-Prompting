# -*- coding: utf-8 -*-
"""
Utility module for updating product information while enforcing field permissions.
"""

# Global list of fields that are allowed to be updated.  Extend this list as needed.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}

def update_product_info(prod: dict, change_data: dict) -> dict:
    """
    Update a product dictionary with new values provided in *change_data*.

    Only keys that are present in the globally defined `PERMITTED_FIELDS` list
    will be applied to the product.  The original dictionary is modified in place,
    and a reference to it (now containing the changes) is returned.

    Parameters
    ----------
    prod : dict
        The product dictionary to be updated.  It should contain keys such as
        'price', 'description', 'stock', and 'category'.
    change_data : dict
        A dictionary containing the new values for one or more fields.  Keys not
        in `PERMITTED_FIELDS` are ignored to avoid accidental modification of
        protected attributes.

    Returns
    -------
    dict
        The same dictionary instance as *prod*, now updated with the permitted
        changes.

    Raises
    ------
    TypeError
        If either *prod* or *change_data* is not a dictionary.
    """
    if not isinstance(prod, dict):
        raise TypeError(f"'prod' must be a dict, got {type(prod).__name__}")
    if not isinstance(change_data, dict):
        raise TypeError(f"'change_data' must be a dict, got {type(change_data).__name__}")

    # Iterate over the change data and apply only permitted fields.
    for key, value in change_data.items():
        if key in PERMITTED_FIELDS:
            prod[key] = value

    return prod