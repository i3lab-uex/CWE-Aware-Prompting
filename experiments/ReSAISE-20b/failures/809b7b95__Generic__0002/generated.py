from typing import Dict, Any

# Fields that are allowed to be updated.
PERMITTED_FIELDS = ["price", "description", "stock", "category"]

def modify_item_details(item: Dict[str, Any], details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update an item's attributes based on the provided details dictionary.
    
    Only keys present in PERMITTED_FIELDS are considered; all other keys are ignored.
    
    Parameters
    ----------
    item : dict
        The original product dictionary. It will be updated in place.
    details : dict
        A dictionary of desired updates. Only keys listed in PERMITTED_FIELDS are applied.
    
    Returns
    -------
    dict
        The updated product dictionary (same object as `item`).
    
    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    """
    if not isinstance(item, dict):
        raise TypeError("`item` must be a dictionary")
    if not isinstance(details, dict):
        raise TypeError("`details` must be a dictionary")
    
    for key, value in details.items():
        if key in PERMITTED_FIELDS:
            item[key] = value
    return item