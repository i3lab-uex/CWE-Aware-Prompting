import copy

# List of fields that are allowed to be updated.
PERMITTED_FIELDS = {"price", "description", "stock", "category"}

def update_product_attributes(item: dict, updates: dict) -> dict:
    """
    Return a new product dictionary with permitted fields updated.

    Parameters
    ----------
    item : dict
        The original product representation.
    updates : dict
        Mapping of field names to new values.

    Returns
    -------
    dict
        A copy of `item` with the permitted fields updated.

    Raises
    ------
    ValueError
        If any key in `updates` is not present in PERMITTED_FIELDS.
    """
    # Validate that all requested updates are permitted
    invalid_keys = set(updates) - PERMITTED_FIELDS
    if invalid_keys:
        raise ValueError(f"Attempted to update disallowed fields: {sorted(invalid_keys)}")

    # Create a shallow copy of the original product to avoid side effects
    updated_item = copy.deepcopy(item)

    # Apply permitted updates
    for key, value in updates.items():
        updated_item[key] = value

    return updated_item