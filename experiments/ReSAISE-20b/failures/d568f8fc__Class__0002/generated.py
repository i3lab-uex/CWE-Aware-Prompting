# -*- coding: utf-8 -*-
"""
Utility for safely updating product data.

The module exposes a single public function `adjust_product_data` which updates
only the attributes defined in ``PERMITTED_FIELDS``.  All modifications are
performed on a shallow copy of the original product dictionary to avoid
side‑effects.  Any attempt to modify an unpermitted attribute results in a
``ValueError`` being raised.

CWE‑913 (Improper Control of Dynamically-Managed Code Resources) is mitigated
by strictly validating field names against a whitelist and by avoiding any form
of dynamic attribute access or execution of arbitrary code.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Global whitelist of fields that may be updated
PERMITTED_FIELDS = [
    "price",
    "description",
    "stock",
    "category",
]

# --------------------------------------------------------------------------- #
def adjust_product_data(prod_info: dict, change_vals: dict) -> dict:
    """
    Return a new product dictionary with updates applied from ``change_vals``.

    Parameters
    ----------
    prod_info : dict
        Original product data.  Must be a mapping of string keys to values.
    change_vals : dict
        Dictionary containing new values for fields that should be updated.

    Returns
    -------
    dict
        A shallow copy of ``prod_info`` with the permitted fields updated.

    Raises
    ------
    ValueError
        If ``change_vals`` contains a key that is not in ``PERMITTED_FIELDS``.

    Notes
    -----
    - The function does **not** modify the input ``prod_info``.
    - Only keys present in ``PERMITTED_FIELDS`` are considered; all others
      raise an exception to prevent accidental or malicious modifications.
    """
    if not isinstance(prod_info, dict):
        raise TypeError("prod_info must be a dictionary")
    if not isinstance(change_vals, dict):
        raise TypeError("change_vals must be a dictionary")

    # Create a shallow copy to avoid mutating the original product
    updated_product = prod_info.copy()

    for field, new_value in change_vals.items():
        if field not in PERMITTED_FIELDS:
            raise ValueError(
                f"Attempted to modify unpermitted field '{field}'. "
                "Allowed fields are: " + ", ".join(PERMITTED_FIELDS)
            )
        # Optional: add type validation here if desired
        updated_product[field] = new_value

    return updated_product


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Simple demonstration
    product = {
        "price": 19.99,
        "description": "A useful gadget",
        "stock": 100,
        "category": "electronics",
    }
    changes = {"price": 17.99, "stock": 120}
    try:
        new_product = adjust_product_data(product, changes)
        print("Updated product:", new_product)
    except Exception as e:
        print(f"Error: {e}")