import copy
from typing import Dict, Any

# Global list of fields that are allowed to be modified.
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
    # Add other permissible fields here
]

def modify_product_details(product: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with new values provided in `data`.

    Parameters
    ----------
    product : dict
        The original product dictionary. It will **not** be modified in place.
    data : dict
        A mapping of field names to new values that should be applied to the product.

    Returns
    -------
    dict
        A new dictionary containing the updated product data.

    Raises
    ------
    ValueError
        If `product` or `data` is not a dictionary.
    KeyError
        If an attempt is made to update a field that is not in `PERMITTED_FIELDS`.

    Notes
    -----
    - The function performs a shallow copy of the product dictionary before applying updates.
      This ensures that callers are not surprised by in‑place modifications.
    - Only fields listed in `PERMITTED_FIELDS` may be altered. All other keys are preserved
      unchanged.
    - The function is intentionally simple and does not perform type validation on the values,
      but callers should ensure that data types are appropriate for each field.
    """
    if not isinstance(product, dict):
        raise ValueError("`product` must be a dictionary")
    if not isinstance(data, dict):
        raise ValueError("`data` must be a dictionary")

    # Create a copy to avoid mutating the original product
    updated_product = copy.deepcopy(product)

    for key, value in data.items():
        if key not in PERMITTED_FIELDS:
            raise KeyError(f"Field '{key}' is not permitted for update")
        updated_product[key] = value

    return updated_product