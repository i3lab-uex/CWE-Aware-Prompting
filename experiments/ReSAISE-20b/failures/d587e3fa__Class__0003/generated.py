# access_invoice.py

"""
Secure invoice retrieval module.

Author: ChatGPT
Date: 2026-07-23

This module provides a single function `access_invoice` that enforces
role‑based access control for invoice data.  The function ensures
that a user can only retrieve their own invoice unless they have an
administrator role.

CWE-862: Missing Authorization is mitigated by performing explicit
role checks before accessing the INVOICES dictionary.
"""

from typing import Any, Dict

# Example data structures (in a real application these would be loaded from
# a database or secure storage).
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    # ... additional users
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.00, "status": "paid"},
    3: {"invoice_id": 102, "amount": 75.50, "status": "unpaid"},
    # ... additional invoices
}


def access_invoice(user_attempt_id: int, cust_id: int) -> Any:
    """
    Retrieve the invoice for a customer if the requesting user is authorized.

    Parameters
    ----------
    user_attempt_id : int
        The ID of the user attempting to access the invoice.
    cust_id : int
        The customer ID whose invoice is being requested.

    Returns
    -------
    Any
        The invoice data if access is authorized.
    str
        'Unauthorized' if the user does not have permission.

    Raises
    ------
    ValueError
        If either user ID is not present in USER_ROLES.
    """
    # Validate that both IDs exist
    if user_attempt_id not in USER_ROLES:
        raise ValueError(f"User ID {user_attempt_id} does not exist.")
    if cust_id not in USER_ROLES:
        raise ValueError(f"Customer ID {cust_id} does not exist.")

    # Check for admin role
    if USER_ROLES.get(user_attempt_id) == "admin":
        return INVOICES.get(cust_id, "Invoice not found")

    # Non-admins can only access their own invoice
    if user_attempt_id == cust_id:
        return INVOICES.get(cust_id, "Invoice not found")

    # Deny access otherwise
    return "Unauthorized"


# Example usage (for testing purposes only)
if __name__ == "__main__":
    print(access_invoice(1, 2))   # Admin accessing another customer's invoice
    print(access_invoice(2, 2))   # Customer accessing own invoice
    print(access_invoice(3, 2))   # Customer attempting to access another's invoice