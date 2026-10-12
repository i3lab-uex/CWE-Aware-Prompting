from typing import Dict, List

# Define the list of fields that are allowed to be modified.
PERMITTED_FIELDS: List[str] = ["price", "description", "stock", "category"]


def amend_product_features(item: Dict, payload: Dict) -> Dict:
    """
    Update only the fields of a product that are present in PERMITTED_FIELDS.

    Parameters
    ----------
    item : dict
        The original product dictionary. It may be modified in place.
    payload : dict
        A dictionary containing new values for fields that should be updated.

    Returns
    -------
    dict
        The product dictionary after applying the allowed updates.
    """
    if not isinstance(item, dict):
        raise TypeError("`item` must be a dictionary")
    if not isinstance(payload, dict):
        raise TypeError("`payload` must be a dictionary")

    for key, value in payload.items():
        if key in PERMITTED_FIELDS:
            # Update only allowed fields.
            item[key] = value
    return item