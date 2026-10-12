from __future__ import annotations

import copy
from typing import Dict, Any

# Global list of fields that are allowed to be updated.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def update_product_attributes(item: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new product dictionary with updates applied only to fields
    listed in PERMITTED_FIELDS. The original ``item`` is left untouched.

    Parameters
    ----------
    item : dict
        Dictionary representing the original product. It may contain any keys.
    updates : dict
        Dictionary containing key/value pairs that represent the desired changes.

    Returns
    -------
    dict
        A new dictionary with the permitted updates applied. Fields not in
        ``PERMITTED_FIELDS`` are ignored.

    Notes
    -----
    - The function performs a shallow copy of the original product to avoid
      accidental mutation.
    - It does not perform type or value validation; callers should ensure the
      updates are appropriate for the application domain.
    """
    # Make a shallow copy to avoid mutating the original product
    updated_item = copy.deepcopy(item)

    for key, value in updates.items():
        if key in PERMITTED_FIELDS:
            updated_item[key] = value
        else:
            # Optionally, log a warning or silently ignore the field.
            pass

    return updated_item