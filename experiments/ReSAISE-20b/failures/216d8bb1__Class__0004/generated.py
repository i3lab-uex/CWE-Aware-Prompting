# -*- coding: utf-8 -*-
"""
Utility to fetch invoices with proper authorization checks.

The function raises no exceptions for invalid input; it simply returns
either the requested invoice or the string 'Unauthorized'.

Author: OpenAI ChatGPT
"""

# --------------------------------------------------------------------------- #
# Imports
# --------------------------------------------------------------------------- #
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Sample data (replace with real persistence layer in production)
# --------------------------------------------------------------------------- #
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.00, "status": "paid"},
    3: {"invoice_id": 102, "amount": 150.00, "status": "unpaid"},
}

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #
def access_invoice(user_id: int, client_id: int) -> Any:
    """
    Return the invoice data for ``client_id`` if the requesting user
    has sufficient privileges.

    Parameters
    ----------
    user_id : int
        The ID of the user making the request.
    client_id : int
        The ID of the customer whose invoice is being requested.

    Returns
    -------
    dict | str
        The invoice dictionary if access is allowed, otherwise the string
        'Unauthorized'.

    Notes
    -----
    * Administrators (role == 'admin') may access any invoice.
    * Customers may only access their own invoices.
    * Missing user or client data is treated as unauthorized to avoid
      leaking information about valid IDs.
    """
    # 1. Validate that the user exists and has a known role
    role = USER_ROLES.get(user_id)
    if role is None:
        return "Unauthorized"

    # 2. Authorization logic
    if role != "admin" and user_id != client_id:
        return "Unauthorized"

    # 3. Retrieve the invoice (return Unauthorized if missing)
    invoice = INVOICES.get(client_id)
    return invoice or "Unauthorized"

# --------------------------------------------------------------------------- #
# Example usage (commented out – remove for production)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    print(access_invoice(1, 2))   # admin accessing customer 2's invoice
    print(access_invoice(2, 2))   # customer accessing own invoice
    print(access_invoice(2, 3))   # customer attempting to access another's invoice