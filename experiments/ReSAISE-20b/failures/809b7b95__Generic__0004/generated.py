# -*- coding: utf-8 -*-

"""
Utility module for modifying product item details.

The global list `PERMITTED_FIELDS` defines which keys in a product
dictionary are allowed to be updated.  The function `modify_item_details`
applies updates from the supplied `details` dictionary to a product
dictionary, but only for keys that appear in `PERMITTED_FIELDS`.

The function mutates the original product dictionary and also returns it
for convenience.  Unpermitted keys are silently ignored to avoid accidental
corruption of the product data.

Example usage:

    product = {
        'price': 19.99,
        'description': 'A nice widget',
        'stock': 42,
        'category': 'Gadgets'
    }

    updates = {'price': 17.99, 'stock': 40, 'color': 'red'}
    modify_item_details(product, updates)

    # product now is:
    # {'price': 17.99, 'description': 'A nice widget', 'stock': 40,
    #  'category': 'Gadgets'}
"""

# Global list of fields that are allowed to be modified.
PERMITTED_FIELDS = [
    'price',
    'description',
    'stock',
    'category'
]


def modify_item_details(item: dict, details: dict) -> dict:
    """
    Update a product dictionary with new values for permitted fields.

    Parameters
    ----------
    item : dict
        The original product dictionary.  This dictionary is modified in
        place.
    details : dict
        A mapping of field names to new values that should be applied to
        the product.

    Returns
    -------
    dict
        The updated product dictionary (the same object that was passed in).

    Notes
    -----
    * Only keys present in :data:`PERMITTED_FIELDS` are updated.
    * Unpermitted keys are ignored; no exception is raised.
    """
    for key, value in details.items():
        if key in PERMITTED_FIELDS:
            item[key] = value
    return item