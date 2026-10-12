# -*- coding: utf-8 -*-

from typing import Any, Dict

# Example data structures (in a real application these would come from a database)
USER_ROLES: Dict[int, list[str]] = {
    1: ["admin"],
    2: ["customer"],
    3: ["customer"],
}

INVOICES: Dict[int, Dict[str, Any]] = {
    2: {"invoice_id": "INV-001", "amount": 250.0, "items": ["Widget A", "Widget B"]},
    3: {"invoice_id": "INV-002", "amount": 125.0, "items": ["Widget C"]},
}


def retrieve_invoice(logged_in_user_id: int, invoice_owner_id: int) -> Any:
    """
    Retrieve the invoice for a given customer.

    Parameters
    ----------
    logged_in_user_id : int
        The ID of the user attempting to access the invoice.
    invoice_owner_id : int
        The ID of the customer whose invoice is requested.

    Returns
    -------
    dict | str
        The invoice details if access is granted; otherwise the string 'Unauthorized'.

    Notes
    -----
    * A user can access their own invoice.
    * Users with the 'admin' role can access any customer's invoice.
    * The function is defensive: it treats missing user IDs or invoices as unauthorized access
      to avoid leaking information about the existence of users or invoices.
    """
    # Fetch roles for the logged-in user; default to empty list if not found
    roles = USER_ROLES.get(logged_in_user_id, [])

    # Allow if user is admin or accessing their own invoice
    if "admin" in roles or logged_in_user_id == invoice_owner_id:
        # Return a copy to prevent accidental mutation of the original data
        return INVOICES.get(invoice_owner_id, {}).copy()
    else:
        return "Unauthorized"