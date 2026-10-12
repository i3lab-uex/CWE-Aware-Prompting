# -*- coding: utf-8 -*-
"""
Utility module for updating product attributes.

The global list ``PERMITTED_FIELDS`` defines which fields may be updated.
"""

from typing import Dict, Any

# Fields that are allowed to be modified
PERMITTED_FIELDS = ["price", "description", "stock", "category"]


def _validate_price(value: Any) -> bool:
    """Return True if ``value`` is a valid price (int or float)."""
    return isinstance(value, (int, float))


def _validate_stock(value: Any) -> bool:
    """Return True if ``value`` is a valid stock quantity (int)."""
    return isinstance(value, int) and value >= 0


def _validate_description(value: Any) -> bool:
    """Return True if ``value`` is a valid description (string)."""
    return isinstance(value, str)


def _validate_category(value: Any) -> bool:
    """Return True if ``value`` is a valid category (string)."""
    return isinstance(value, str)


# Mapping of field names to their validation functions
_VALIDATORS = {
    "price": _validate_price,
    "stock": _validate_stock,
    "description": _validate_description,
    "category": _validate_category,
}


def update_product_attributes(item: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update product attributes in ``item`` with values from ``updates``.

    Only keys listed in :data:`PERMITTED_FIELDS` are considered.
    Validation is performed on each value according to its field type.
    The original ``item`` dictionary is **not** modified; a new dict
    containing the updated values is returned.

    Parameters
    ----------
    item : dict
        Dictionary representing a product.  Must contain at least the keys
        defined in ``PERMITTED_FIELDS`` (although missing keys are simply
        added if they appear in ``updates``).
    updates : dict
        Dictionary of key/value pairs to apply to the product.

    Returns
    -------
    dict
        A new dictionary containing the updated product state.

    Raises
    ------
    TypeError
        If ``item`` or ``updates`` are not dictionaries.
    ValueError
        If a value in ``updates`` fails its field-specific validation.
    """
    if not isinstance(item, dict):
        raise TypeError("`item` must be a dictionary")
    if not isinstance(updates, dict):
        raise TypeError("`updates` must be a dictionary")

    # Work on a shallow copy to avoid mutating the caller's data
    updated_item = item.copy()

    for key, value in updates.items():
        if key not in PERMITTED_FIELDS:
            # Ignore any fields that are not permitted
            continue

        validator = _VALIDATORS.get(key)
        if validator and not validator(value):
            raise ValueError(
                f"Invalid value for field '{key}': {value!r}"
            )

        updated_item[key] = value

    return updated_item