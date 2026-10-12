from typing import Any, Dict

# Example role mapping (user_id -> list of roles)
USER_ROLES: Dict[int, list[str]] = {
    1: ["admin"],
    2: ["customer"],
    3: ["customer"],
}

# Example invoice storage (user_id -> invoice data)
INVOICES: Dict[int, Any] = {
    2: {"invoice_id": "INV-1001", "amount": 150.0, "items": ["Widget A"]},
    3: {"invoice_id": "INV-1002", "amount": 200.0, "items": ["Widget B"]},
}


def download_invoice(current_user_id: int, customer_id: int) -> Any:
    """
    Return the invoice data for a given customer if the requesting user is authorized.
    
    Authorization rules:
      - A user can download their own invoice (current_user_id == customer_id).
      - An administrator (role 'admin') can download any customer's invoice.
    
    Parameters
    ----------
    current_user_id : int
        The user ID of the actor requesting the download.
    customer_id : int
        The user ID whose invoice is requested.
    
    Returns
    -------
    Any
        The invoice data if authorized, otherwise the string 'Unauthorized'.
    
    Notes
    -----
    - If either user ID does not exist in USER_ROLES or INVOICES, the function
      treats it as an unauthorized request to avoid leaking existence information.
    """
    # Quick existence check: if either ID is unknown, deny access
    if current_user_id not in USER_ROLES or customer_id not in INVOICES:
        return "Unauthorized"

    # Self‑access
    if current_user_id == customer_id:
        return INVOICES[customer_id]

    # Admin access
    if "admin" in USER_ROLES[current_user_id]:
        return INVOICES[customer_id]

    # Default deny
    return "Unauthorized"