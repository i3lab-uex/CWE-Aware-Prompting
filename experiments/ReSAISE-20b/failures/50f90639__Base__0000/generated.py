from typing import Dict, Any

# Fields that are allowed to be updated.
PERMITTED_FIELDS = {
    "price",
    "description",
    "stock",
    "category",
}

def modify_product_details(product: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a product dictionary with values from *data* only for fields
    that are explicitly permitted. The function returns the modified product.
    
    Parameters
    ----------
    product : dict
        Original product dictionary. It is modified in place.
    data : dict
        Dictionary containing potential updates.

    Returns
    -------
    dict
        The updated product dictionary.
    
    Raises
    ------
    TypeError
        If *product* or *data* are not dictionaries.
    """
    if not isinstance(product, dict):
        raise TypeError("product must be a dictionary")
    if not isinstance(data, dict):
        raise TypeError("data must be a dictionary")

    for key, value in data.items():
        # Ensure the key is a string and permitted
        if isinstance(key, str) and key in PERMITTED_FIELDS:
            product[key] = value
    return product