import copy

# Global list of fields that are allowed to be modified.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]

def modify_item_details(item: dict, details: dict) -> dict:
    """
    Return a new product dictionary with updated values for the keys present in
    `details`, but only if those keys are listed in PERMITTED_FIELDS.

    Parameters
    ----------
    item : dict
        The original product dictionary. Must contain at least the keys that
        are permitted to be updated.
    details : dict
        A mapping of key/value pairs that should override the corresponding
        entries in `item`.

    Returns
    -------
    dict
        A new dictionary that reflects the updated product state.

    Raises
    ------
    ValueError
        If any key in `details` is not listed in PERMITTED_FIELDS.
    TypeError
        If either argument is not a dictionary.

    Notes
    -----
    * The original `item` dictionary is never mutated; a shallow copy is
      returned.
    * This function protects against accidental modification of disallowed
      fields, which is a common source of CWE-664 violations when a resource
      (the product dictionary) is not correctly controlled over its lifetime.
    """
    if not isinstance(item, dict):
        raise TypeError("`item` must be a dictionary")
    if not isinstance(details, dict):
        raise TypeError("`details` must be a dictionary")

    # Validate that all keys in details are permitted.
    for key in details:
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Field '{key}' is not permitted for update")

    # Create a shallow copy to avoid side‑effects on the original item.
    updated_item = copy.copy(item)

    # Apply updates.
    for key, value in details.items():
        updated_item[key] = value

    return updated_item