from __future__ import annotations

# List of fields that are allowed to be updated.  This list is defined globally
# and must not contain any disallowed or sensitive attributes.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def update_product_info(prod: dict, change_data: dict) -> dict:
    """
    Update only permitted fields of a product dictionary.

    Parameters
    ----------
    prod : dict
        The original product representation.  It is modified in place.
    change_data : dict
        Mapping of field names to new values that should be applied.

    Returns
    -------
    dict
        The updated product dictionary (the same object that was passed in).

    Raises
    ------
    ValueError
        If any key in ``change_data`` is not present in :data:`PERMITTED_FIELDS`.

    Notes
    -----
    This function deliberately avoids any dynamic code execution.  It simply
    iterates over the provided ``change_data`` keys and assigns the new values
    to the product dictionary when the key is allowed.  No external resources
    are accessed, and no untrusted code can be executed through this path.
    """
    for key, value in change_data.items():
        if key not in PERMITTED_FIELDS:
            raise ValueError(
                f"Attempt to modify disallowed field '{key}'. "
                "Allowed fields: " + ", ".join(PERMITTED_FIELDS)
            )
        prod[key] = value
    return prod