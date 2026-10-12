# -*- coding: utf-8 -*-
"""
Product editing utilities.

The module defines a single public function `edit_product_info` which
updates an existing product dictionary with values from another dictionary.
Only keys listed in the global `PERMITTED_FIELDS` are allowed to be changed.

The implementation is defensive:
* The original product dictionary is not modified in place – a shallow copy
  is returned instead.
* Unexpected keys in `details` are ignored silently; an explicit exception
  can be raised if stricter behaviour is desired.
* Type annotations and minimal validation make the function easy to use
  in larger applications.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import copy
from typing import Dict, Any, List

# --------------------------------------------------------------------------- #
# Global configuration
# --------------------------------------------------------------------------- #

PERMITTED_FIELDS: List[str] = ["price", "description", "stock", "category"]

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def edit_product_info(item: Dict[str, Any], details: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new product dictionary with updates applied from ``details``.
    
    Parameters
    ----------
    item : dict
        The original product dictionary. Must contain at least the keys
        listed in ``PERMITTED_FIELDS``; other keys are preserved unchanged.
    details : dict
        A dictionary containing the desired updates. Only keys present in
        ``PERMITTED_FIELDS`` are applied.
    
    Returns
    -------
    dict
        A new dictionary containing the updated product information. The input
        ``item`` remains unmodified.
    
    Raises
    ------
    TypeError
        If either ``item`` or ``details`` is not a mapping type.
    
    Notes
    -----
    * The function performs a shallow copy of ``item``. If any value inside
      the dictionary is itself a mutable object (e.g., a list or another dict),
      that object will not be deeply copied. Use ``copy.deepcopy`` if a full
      deep copy is required.
    * Keys in ``details`` that are not present in ``PERMITTED_FIELDS`` are
      silently ignored. This design choice avoids accidental modification of
      sensitive or immutable attributes.
    """
    # Basic type checks
    if not isinstance(item, dict):
        raise TypeError(f"Expected 'item' to be a dict, got {type(item).__name__}")
    if not isinstance(details, dict):
        raise TypeError(f"Expected 'details' to be a dict, got {type(details).__name__}")

    # Create a shallow copy so the original is not mutated
    updated_product = copy.deepcopy(item)

    # Apply only permitted updates
    for key, value in details.items():
        if key in PERMITTED_FIELDS:
            updated_product[key] = value

    return updated_product