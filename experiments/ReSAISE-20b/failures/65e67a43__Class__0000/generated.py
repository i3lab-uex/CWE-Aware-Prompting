# -*- coding: utf-8 -*-

"""
Utility for retrieving invoices with proper authorization checks.

Author: ChatGPT
Date: 2026-07-23
"""

from typing import Any, Dict

# Example role mapping and invoice storage. In a real application these would
# come from a database or external service.
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    4: "guest",          # role with no special privileges
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": "INV-001", "amount": 150.0, "status": "paid"},
    3: {"invoice_id": "INV-002", "amount": 200.0, "status": "unpaid"},
}

def fetch_invoice(requester_id: int, owner_id: int) -> Any:
    """
    Retrieve the invoice for a given customer if the requester is authorized.

    Parameters
    ----------
    requester_id : int
        The ID of the user attempting to access the invoice.
    owner_id : int
        The ID of the customer whose invoice is being requested.

    Returns
    -------
    dict | str
        The invoice details if access is granted, otherwise the string 'Unauthorized'.

    Notes
    -----
    * A user can access their own invoice.
    * An administrator (role == 'admin') can access any customer's invoice.
    * If the requester or owner does not exist in the system, 'Unauthorized' is returned.

    Security
    --------
    * The function performs a strict authorization check to prevent CWE‑862 (Missing Authorization).
    * It does not expose internal data structures or error messages that could aid an attacker.
    """
    # Verify that both users exist in the system
    if requester_id not in USER_ROLES or owner_id not in INVOICES:
        return "Unauthorized"

    # Admin role is privileged
    requester_role = USER_ROLES.get(requester_id)

    # Allow if the requester is an admin or requesting their own invoice
    authorized = (
        requester_role == "admin" or
        requester_id == owner_id
    )

    if not authorized:
        return "Unauthorized"

    # Return a copy to avoid accidental modifications
    invoice = INVOICES.get(owner_id)
    if invoice is None:
        return "Unauthorized"

    # Return a shallow copy; deep copy could be used if nested structures exist
    return dict(invoice)

# Example usage (for testing only)
if __name__ == "__main__":
    print(fetch_invoice(1, 2))   # Admin accessing customer 2's invoice
    print(fetch_invoice(2, 2))   # Customer accessing own invoice
    print(fetch_invoice(3, 2))   # Unauthorized access attempt