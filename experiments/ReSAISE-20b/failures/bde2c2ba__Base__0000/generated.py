# SPDX-License-Identifier: MIT

"""
Utility for safely updating product dictionaries.

The function `update_item_information` updates only those keys that are
explicitly listed in the global ``PERMITTED_FIELDS`` sequence. This
prevents accidental or malicious modification of sensitive attributes
(e.g., ``__class__``) that could lead to code injection or other
security issues (CWE‑915).
"""

from typing import Dict, Iterable

# List of keys that are allowed to be modified.
PERMITTED_FIELDS: Iterable[str] = (
    "price",
    "description",
    "stock",
    "category",
)

def update_item_information(
    product_info: Dict[str, object],
    new_data: Dict[str, object],
) -> Dict[str, object]:
    """
    Update a product dictionary with new values while restricting the
    modifications to a whitelist of permitted fields.

    Parameters
    ----------
    product_info : dict
        The original product dictionary. Must be a mutable mapping.
    new_data : dict
        Dictionary containing key/value pairs to update in ``product_info``.
        Only keys present in :data:`PERMITTED_FIELDS` will be applied.

    Returns
    -------
    dict
        The updated product dictionary.  ``product_info`` is modified in
        place and returned for convenience.

    Raises
    ------
    TypeError
        If either ``product_info`` or ``new_data`` is not a mapping.
    ValueError
        If any key in ``new_data`` is not an instance of :class:`str`.
    """
    # Validate input types
    if not isinstance(product_info, dict):
        raise TypeError("product_info must be a dictionary")
    if not isinstance(new_data, dict):
        raise TypeError("new_data must be a dictionary")

    # Ensure all keys are strings
    for key in new_data:
        if not isinstance(key, str):
            raise ValueError(f"Invalid key type: {key!r} (must be a string)")

    # Apply only permitted fields
    for key, value in new_data.items():
        if key in PERMITTED_FIELDS:
            product_info[key] = value

    return product_info