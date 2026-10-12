# update_item_information.py

from typing import Dict, Any, List


# Define which fields may be updated.  Only these keys will be considered.
PERMITTED_FIELDS: List[str] = ["price", "description", "stock", "category"]


def update_item_information(
    product_info: Dict[str, Any], new_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update a product's attributes with values from ``new_data``.
    
    Only keys present in :data:`PERMITTED_FIELDS` are allowed to be updated.  
    Any attempt to modify a non‑permitted field will raise ``ValueError``.
    
    Parameters
    ----------
    product_info : dict
        The original product dictionary.  This dictionary is **not** modified in place;
        a new updated dictionary is returned.
    new_data : dict
        Dictionary containing the desired updates.  Keys that are not in
        :data:`PERMITTED_FIELDS` cause a ``ValueError``.
    
    Returns
    -------
    dict
        A new dictionary containing the updated product information.
    """
    # Validate that all keys in ``new_data`` are permitted
    invalid_keys = [k for k in new_data if k not in PERMITTED_FIELDS]
    if invalid_keys:
        raise ValueError(
            f"Attempted to update disallowed fields: {', '.join(invalid_keys)}"
        )

    # Create a copy to avoid mutating the original product_info
    updated_product = product_info.copy()

    # Apply permitted updates
    for key, value in new_data.items():
        updated_product[key] = value

    return updated_product