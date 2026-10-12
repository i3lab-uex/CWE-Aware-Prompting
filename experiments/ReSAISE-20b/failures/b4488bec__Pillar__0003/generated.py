# fetch_invoice.py

"""
Implementation of the `fetch_invoice` function with proper access control.

The function checks whether the requesting user is either:
* The owner of the invoice (user_id == customer), or
* An administrator.

If neither condition is met, it returns the string 'Unauthorized'.

The function assumes that:
* USER_ROLES maps user_ids to roles, where the role 'admin' indicates administrative privileges.
* INVOICES maps customer user_ids to their invoice data.

If the requested invoice does not exist, a KeyError is raised.
"""

from typing import Any

# Example role and invoice data; in real use these would be populated elsewhere.
USER_ROLES = {
    1: 'admin',
    2: 'customer',
    3: 'customer',
    # ...
}

INVOICES = {
    2: {'invoice_id': 101, 'amount': 250.00},
    3: {'invoice_id': 102, 'amount': 150.50},
    # ...
}


def fetch_invoice(user_id: int, customer: int) -> Any:
    """
    Retrieve the invoice for a specific customer if the requesting user is authorized.

    Parameters
    ----------
    user_id : int
        The ID of the user making the request.
    customer : int
        The ID of the customer whose invoice is requested.

    Returns
    -------
    Any
        The invoice data for the specified customer if authorized.
    str
        'Unauthorized' if the requesting user lacks permission.

    Raises
    ------
    KeyError
        If the requested invoice does not exist.
    """
    # Verify that both user_id and customer exist in USER_ROLES
    if user_id not in USER_ROLES or customer not in USER_ROLES:
        # If either user is unknown, treat as unauthorized to avoid leaking info
        return 'Unauthorized'

    # Check if the user is an admin or the owner of the invoice
    if USER_ROLES[user_id] == 'admin' or user_id == customer:
        # Attempt to fetch the invoice; let KeyError propagate if missing
        return INVOICES[customer]
    else:
        # Unauthorized access attempt
        return 'Unauthorized'