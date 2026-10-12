from typing import Dict, Any

# Example role definitions. In a real system these would come from your user management.
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    # ... other users
}

# Example invoice storage. In practice this would be a database or file system.
INVOICES: Dict[int, Any] = {
    2: {"invoice_id": "INV-001", "amount": 250.00, "items": ["Widget A", "Widget B"]},
    3: {"invoice_id": "INV-002", "amount": 150.00, "items": ["Widget C"]},
    # ... other invoices
}

def get_invoice(requester_id: int, client_id: int) -> Any:
    """
    Retrieve the invoice for a given client if the requester is authorized.

    Parameters
    ----------
    requester_id : int
        The user ID of the person making the request.
    client_id : int
        The user ID whose invoice is requested.

    Returns
    -------
    Any
        The invoice data if authorized; otherwise the string 'Unauthorized'.

    Notes
    -----
    - Administrators (role == 'admin') can access any invoice.
    - Regular customers can only access their own invoice.
    """
    # Fetch roles safely; default to None if not found
    requester_role = USER_ROLES.get(requester_id)
    client_role   = USER_ROLES.get(client_id)

    # If either user does not exist, deny access
    if requester_role is None or client_role is None:
        return "Unauthorized"

    # Authorization logic
    if requester_role == "admin" or requester_id == client_id:
        invoice = INVOICES.get(client_id)
        if invoice is None:
            # Invoice not found – still treat as unauthorized to avoid leaking existence
            return "Unauthorized"
        return invoice

    # Any other case is unauthorized
    return "Unauthorized"