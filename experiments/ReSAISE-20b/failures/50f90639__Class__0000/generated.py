import copy
from typing import Dict, Any

# Global list of fields that are allowed to be updated.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
    # Add other permitted fields here.
]


def modify_product_details(product: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with values from ``data`` only for keys listed in
    :data:`PERMITTED_FIELDS`.

    Parameters
    ----------
    product:
        Original product dictionary. It will not be modified in place.
    data:
        Dictionary containing potential updates.

    Returns
    -------
    dict
        A new dictionary representing the updated product.

    Raises
    ------
    KeyError
        If ``data`` contains a key that is not in :data:`PERMITTED_FIELDS`.
    """
    # Create a shallow copy to avoid mutating the original product.
    updated_product = copy.deepcopy(product)

    for key, value in data.items():
        if key not in PERMITTED_FIELDS:
            raise KeyError(f"Field '{key}' is not permitted for update.")
        updated_product[key] = value

    return updated_product