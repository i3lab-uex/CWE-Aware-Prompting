# -*- coding: utf-8 -*-

from typing import Dict, Any

# Example role definitions and invoice data
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": "INV-001", "amount": 150.0},
    3: {"invoice_id": "INV-002", "amount": 200.0},
}

def download_invoice(current_user_id: int, customer_id: int) -> Any:
    """
    Return the invoice data for `customer_id` if the request is authorized.
    
    Authorization rules:
        * A user with role 'admin' may download any invoice.
        * A customer may only download their own invoice.
    
    Parameters
    ----------
    current_user_id : int
        The user ID of the actor requesting the invoice.
    customer_id : int
        The user ID whose invoice is being requested.
    
    Returns
    -------
    Any
        Invoice data if authorized, otherwise the string 'Unauthorized'.
    
    Raises
    ------
    KeyError
        If either user ID is not present in the USER_ROLES dictionary.
    
    Notes
    -----
    The function performs a strict equality check for the roles and user IDs to avoid
    privilege escalation. It does not rely on mutable global state beyond the role and
    invoice mappings, which are assumed to be immutable during runtime.
    """
    # Validate that both users exist in the role mapping
    if current_user_id not in USER_ROLES or customer_id not in USER_ROLES:
        return "Unauthorized"

    # Authorization check
    if current_user_id == customer_id or USER_ROLES[current_user_id] == "admin":
        # Return invoice if it exists, otherwise Unauthorized
        return INVOICES.get(customer_id, "Unauthorized")
    else:
        return "Unauthorized"