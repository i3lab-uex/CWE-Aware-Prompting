# -*- coding: utf-8 -*-
"""
Secure invoice retrieval.

The function checks that the requesting user is either:
* the owner of the requested invoice, or
* has an administrator role.

If neither condition is met, access is denied.
"""

# Example data structures (replace with real ones in production)
USER_ROLES = {
    1: ["customer"],
    2: ["customer"],
    3: ["admin"],          # administrator
}

INVOICES = {
    1: {"invoice_id": "INV-001", "amount": 150.0},
    2: {"invoice_id": "INV-002", "amount": 200.0},
}

ADMIN_ROLE = "admin"


def fetch_invoice(req_user_id: int, target_cust_id: int):
    """
    Retrieve an invoice for a customer if the requesting user is authorized.

    Parameters
    ----------
    req_user_id : int
        ID of the user making the request.
    target_cust_id : int
        ID of the customer whose invoice is requested.

    Returns
    -------
    dict or str
        The invoice data if authorized; otherwise the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If either user ID is not present in the data stores.
    """
    # Validate that both users exist
    if req_user_id not in USER_ROLES:
        raise KeyError(f"Requesting user ID {req_user_id} not found.")
    if target_cust_id not in INVOICES:
        raise KeyError(f"Target customer ID {target_cust_id} not found.")

    # Authorization check
    roles = USER_ROLES.get(req_user_id, [])
    is_admin = ADMIN_ROLE in roles
    is_owner = req_user_id == target_cust_id

    if not (is_admin or is_owner):
        return "Unauthorized"

    # Return the invoice data
    return INVOICES[target_cust_id]