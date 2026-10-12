from typing import Dict, Any

# Global list of fields that may be updated
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def update_product_attributes(item: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with values from ``updates`` only for keys listed in
    :data:`PERMITTED_FIELDS`.

    Parameters
    ----------
    item :
        Dictionary representing a product. The function will modify this dictionary in place.
    updates :
        Dictionary containing key/value pairs to apply to the product.

    Returns
    -------
    dict
        The updated product dictionary.

    Notes
    -----
    * Only keys present in :data:`PERMITTED_FIELDS` are considered; all others are ignored.
    * The function does not perform type checking on the values – it simply assigns them.
    * No code execution or other side effects occur, mitigating CWE‑913 concerns.
    """
    if not isinstance(item, dict):
        raise TypeError("item must be a dictionary")
    if not isinstance(updates, dict):
        raise TypeError("updates must be a dictionary")

    for key, value in updates.items():
        if key in PERMITTED_FIELDS:
            item[key] = value

    return item