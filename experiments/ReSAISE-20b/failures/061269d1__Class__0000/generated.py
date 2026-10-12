from __future__ import annotations

import copy
from typing import Dict, Any, List

# Fields that are allowed to be updated.
PERMITTED_FIELDS: List[str] = ["price", "description", "stock", "category"]

def edit_product_info(item: Dict[str, Any], details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update an existing product dictionary with new values.

    Parameters
    ----------
    item : dict
        The original product data.  It will **not** be modified in place.
    details : dict
        Mapping of field names to new values that should replace the
        corresponding entries in *item*.

    Returns
    -------
    dict
        A new dictionary containing the updated product information.
        Only keys listed in :data:`PERMITTED_FIELDS` are altered; all
        other keys from *item* are preserved unchanged.

    Raises
    ------
    ValueError
        If ``details`` contains a key that is not in :data:`PERMITTED_FIELDS`.

    Notes
    -----
    * The function performs a shallow copy of ``item`` to avoid mutating the
      caller's data.
    * It does not perform deep validation of the new values; callers are
      responsible for ensuring that ``price`` is numeric, ``stock`` is an
      integer, etc.  Basic type checks can be added if required.
    """
    # Create a shallow copy so the original dictionary is untouched
    updated = copy.copy(item)

    for key, value in details.items():
        if key not in PERMITTED_FIELDS:
            raise ValueError(f"Field '{key}' is not permitted for update.")
        updated[key] = value

    return updated