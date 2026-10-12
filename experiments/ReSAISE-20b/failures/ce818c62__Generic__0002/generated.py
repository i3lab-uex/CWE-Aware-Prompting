# -*- coding: utf-8 -*-

"""
Invoice download module.

Provides a single public function `download_invoice` that checks whether the
requesting user is authorized to download an invoice.  Authorization rules:

* A customer may only download *their own* invoice.
* An administrator (`role == "admin"`) can download any customer's invoice.

If the request is not authorized, the function returns the string
`"Unauthorized"`.  Any missing user or invoice data results in a `KeyError`,
which is intentionally propagated to signal a configuration error.
"""

from typing import Dict, List, Any

# Example role mapping: user_id -> list of roles
USER_ROLES: Dict[int, List[str]] = {
    1: ["admin"],
    2: ["customer"],
    3: ["customer"],
    # Add more users as needed
}

# Example invoice mapping: user_id -> invoice data (could be any serializable object)
INVOICES: Dict[int, Any] = {
    2: "Invoice for user 2: $100",
    3: "Invoice for user 3: $200",
    # Add more invoices as needed
}


def download_invoice(current_user_id: int, customer_id: int) -> Any:
    """
    Return the invoice data for `customer_id` if `current_user_id`
    is authorized to download it.

    Parameters
    ----------
    current_user_id : int
        The ID of the user making the request.
    customer_id : int
        The ID of the customer whose invoice is requested.

    Returns
    -------
    Any
        Invoice data if authorized; otherwise the string "Unauthorized".

    Raises
    ------
    KeyError
        If either `current_user_id` or `customer_id` is not present in the
        USER_ROLES or INVOICES dictionaries.
    """
    # Ensure both users exist in the role mapping
    if current_user_id not in USER_ROLES:
        raise KeyError(f"Unknown user ID: {current_user_id}")
    if customer_id not in USER_ROLES:
        raise KeyError(f"Unknown user ID: {customer_id}")

    # Determine roles
    current_roles = USER_ROLES[current_user_id]

    # Authorization logic:
    # - Admins can download any invoice
    # - Customers can only download their own invoice
    if "admin" in current_roles or current_user_id == customer_id:
        # Ensure the requested invoice exists
        if customer_id not in INVOICES:
            raise KeyError(f"No invoice found for user ID: {customer_id}")
        return INVOICES[customer_id]

    # Not authorized
    return "Unauthorized"