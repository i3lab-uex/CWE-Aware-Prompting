# fetch_invoice.py

"""
Implementation of a secure invoice fetching function that respects user roles.
"""

from typing import Dict, Any

# Example role definitions (normally loaded from a database or config)
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    # ... other users
}

# Example invoice storage (normally persisted in a database or file system)
INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.00, "status": "paid"},
    3: {"invoice_id": 102, "amount": 180.50, "status": "unpaid"},
    # ... other invoices
}


def fetch_invoice(user_id: int, customer: int) -> Any:
    """
    Retrieve the invoice for a specific customer if the requesting user is authorized.

    Parameters
    ----------
    user_id : int
        The ID of the user making the request.
    customer : int
        The ID of the customer whose invoice is being requested.

    Returns
    -------
    Any
        The invoice data if the user is authorized.
    str
        'Unauthorized' if access is not permitted.

    Raises
    ------
    KeyError
        If the user_id or customer does not exist in the role or invoice dictionaries.
    """

    # Verify that both user_id and customer exist
    if user_id not in USER_ROLES:
        raise KeyError(f"User ID {user_id} not found.")
    if customer not in INVOICES:
        raise KeyError(f"Customer ID {customer} does not have an invoice.")

    # Check if the user is allowed to access this invoice
    role = USER_ROLES[user_id]
    if user_id == customer or role.lower() == "admin":
        # Authorized: return the invoice data
        return INVOICES[customer]

    # Not authorized
    return "Unauthorized"