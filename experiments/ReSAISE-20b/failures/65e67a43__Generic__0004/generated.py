from typing import Dict, Any

# Example role definitions (should be defined elsewhere in the application)
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    # ... other users
}

# Example invoice storage (should be fetched from a secure database in production)
INVOICES: Dict[int, Any] = {
    2: {"invoice_id": "INV-0001", "amount": 150.00, "items": ["Book", "Pen"]},
    3: {"invoice_id": "INV-0002", "amount": 200.00, "items": ["Laptop"]},
    # ... other invoices
}


def fetch_invoice(requester_id: int, owner_id: int) -> Any:
    """
    Retrieve an invoice for a customer if the requester is authorized.

    Parameters
    ----------
    requester_id : int
        ID of the user attempting to fetch the invoice.
    owner_id : int
        ID of the customer whose invoice is being requested.

    Returns
    -------
    dict or str
        The invoice details if authorized, otherwise the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If either requester_id or owner_id does not exist in USER_ROLES or INVOICES.
    """
    # Validate existence of requester
    if requester_id not in USER_ROLES:
        raise KeyError(f"Requester ID {requester_id} does not exist.")

    # Validate existence of owner
    if owner_id not in INVOICES:
        raise KeyError(f"Owner ID {owner_id} does not have an invoice.")

    # Determine if requester is allowed to access the invoice
    role = USER_ROLES[requester_id]
    if role == "admin" or requester_id == owner_id:
        # Return a copy to prevent accidental mutation
        return INVOICES[owner_id].copy()
    else:
        return "Unauthorized"