# -*- coding: utf-8 -*-
"""
Access control for invoices.

The function `access_invoice` allows a user to retrieve an invoice only if
they are the owner of the invoice or have an administrative role.
"""

from typing import Dict, Any

# Example data structures (replace with real ones in production)
USER_ROLES: Dict[int, list[str]] = {
    1: ["customer"],
    2: ["admin"],
    3: ["customer", "vip"],
}

INVOICES: Dict[int, dict[str, Any]] = {
    1: {"invoice_id": 101, "amount": 250.0},
    3: {"invoice_id": 103, "amount": 470.5},
}

def access_invoice(user_attempt_id: int, cust_id: int) -> Any:
    """
    Retrieve an invoice if the requesting user is authorized.

    Parameters
    ----------
    user_attempt_id : int
        The ID of the user attempting to access the invoice.
    cust_id : int
        The customer ID whose invoice is being requested.

    Returns
    -------
    dict or str
        The invoice data if authorized; otherwise the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If either user_attempt_id or cust_id is not present in USER_ROLES
        or INVOICES, respectively.
    """
    # Validate existence of users and invoices
    if user_attempt_id not in USER_ROLES:
        raise KeyError(f"User ID {user_attempt_id} does not exist.")
    if cust_id not in INVOICES:
        raise KeyError(f"Invoice for customer ID {cust_id} does not exist.")

    # Authorization logic
    user_roles = USER_ROLES[user_attempt_id]
    is_admin = "admin" in (role.lower() for role in user_roles)
    if user_attempt_id == cust_id or is_admin:
        return INVOICES[cust_id]

    # Deny access
    return "Unauthorized"

# Example usage (for testing purposes only)
if __name__ == "__main__":
    print(access_invoice(1, 1))   # Should return the invoice for user 1
    print(access_invoice(2, 3))   # Admin accessing user 3's invoice
    print(access_invoice(1, 3))   # Unauthorized access attempt