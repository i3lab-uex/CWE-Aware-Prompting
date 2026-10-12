import copy
from typing import Dict, List

# Globally defined list of fields that are allowed to be updated
PERMITTED_FIELDS: List[str] = ["price", "description", "stock", "category"]


def adjust_product_data(prod_info: Dict[str, any], change_vals: Dict[str, any]) -> Dict[str, any]:
    """
    Update only the fields listed in PERMITTED_FIELDS for a product.

    Parameters
    ----------
    prod_info : dict
        Dictionary representing the existing product data.
    change_vals : dict
        Dictionary containing field-value pairs to be updated.

    Returns
    -------
    dict
        A new dictionary that reflects the applied changes. The original
        ``prod_info`` remains unchanged.

    Raises
    ------
    ValueError
        If ``change_vals`` contains keys that are not in PERMITTED_FIELDS.
    """
    # Validate incoming changes
    for key in change_vals:
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Attempt to modify non‑permitted field: {key}")

    # Create a shallow copy so the original product dict is not mutated
    updated_product = copy.deepcopy(prod_info)

    # Apply permitted updates
    for key, value in change_vals.items():
        updated_product[key] = value

    return updated_product