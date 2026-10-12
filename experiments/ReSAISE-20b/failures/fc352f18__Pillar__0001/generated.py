import copy

# Globally defined list of fields that are allowed to be updated.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}

def amend_product_features(item: dict, payload: dict) -> dict:
    """
    Update the product dictionary `item` with values from `payload`, but only
    for fields that are listed in the globally defined PERMITTED_FIELDS.
    
    Parameters
    ----------
    item : dict
        The original product representation. It is not modified in place; a
        shallow copy is returned.
    payload : dict
        A dictionary containing new values for the product fields. Only keys
        present in PERMITTED_FIELDS are applied.
    
    Returns
    -------
    dict
        A new dictionary containing the updated product data.
    
    Raises
    ------
    ValueError
        If `item` is not a dictionary or if any key in `payload` is not an
        allowed field.
    """
    
    # Basic validation of the input types
    if not isinstance(item, dict):
        raise ValueError("`item` must be a dictionary")
    if not isinstance(payload, dict):
        raise ValueError("`payload` must be a dictionary")
    
    # Create a shallow copy to avoid mutating the original item
    updated_item = copy.copy(item)
    
    # Iterate over payload and apply updates only for permitted fields
    for key, value in payload.items():
        if key not in PERMITTED_FIELDS:
            # Reject disallowed keys to avoid accidental injection
            raise ValueError(f"Field '{key}' is not permitted for update")
        updated_item[key] = value
    
    return updated_item