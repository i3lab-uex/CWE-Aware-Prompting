# -*- coding: utf-8 -*-

"""
Utility to allow users or administrators to download invoices.

The module expects two global dictionaries:
    USER_ROLES  : Mapping from user_id to an iterable of role names.
    INVOICES    : Mapping from client_id to invoice details (any serialisable object).

Example:

    USER_ROLES = {
        1: ['admin'],
        2: ['customer'],
        3: ['customer']
    }

    INVOICES = {
        2: {'id': 'INV-001', 'amount': 150.0},
        3: {'id': 'INV-002', 'amount': 200.0}
    }

Usage:

    invoice = access_invoice(user_id=2, client_id=2)   # returns the invoice
    invoice = access_invoice(user_id=1, client_id=3)   # admin can fetch any
    invoice = access_invoice(user_id=2, client_id=3)   # Unauthorized
"""

from typing import Any, Dict

# Example data (replace with real data in production)
USER_ROLES: Dict[int, Any] = {}
INVOICES: Dict[int, Any] = {}


def access_invoice(user_id: int, client_id: int) -> Any:
    """
    Return invoice data if the user is authorized.

    Parameters
    ----------
    user_id : int
        The ID of the user attempting to access an invoice.
    client_id : int
        The ID of the customer whose invoice is requested.

    Returns
    -------
    Any
        Invoice data if authorized, otherwise the string 'Unauthorized'.

    Notes
    -----
    * Administrators (role containing 'admin') can access any invoice.
    * Customers may only access their own invoices (user_id == client_id).
    * If the invoice does not exist, 'Unauthorized' is returned to avoid leaking
      information about non‑existent records.
    """
    # Quick exit if the user or invoice is missing
    roles = USER_ROLES.get(user_id)
    if roles is None:
        return "Unauthorized"

    # Normalize role representation
    if isinstance(roles, (list, set, tuple)):
        role_set = {role.lower() for role in roles}
    else:
        # Assume a single string role
        role_set = {str(roles).lower()}

    is_admin = "admin" in role_set
    is_owner = user_id == client_id

    if not (is_admin or is_owner):
        return "Unauthorized"

    # Retrieve the invoice; return 'Unauthorized' if missing
    invoice = INVOICES.get(client_id)
    return invoice or "Unauthorized"


# Example usage (for testing purposes only):
if __name__ == "__main__":
    # Populate example data
    USER_ROLES.update(
        {
            1: ["admin"],
            2: ["customer"],
            3: ["customer"],
        }
    )
    INVOICES.update(
        {
            2: {"id": "INV-001", "amount": 150.0},
            3: {"id": "INV-002", "amount": 200.0},
        }
    )

    print(access_invoice(2, 2))  # Own invoice
    print(access_invoice(1, 3))  # Admin access
    print(access_invoice(2, 3))  # Unauthorized