from __future__ import annotations

# Example role and invoice dictionaries (replace with real data sources)
USER_ROLES = {
    1: "admin",
    2: "customer",
    3: "customer",
    # ...
}

INVOICES = {
    2: {"invoice_id": 101, "amount": 250.0, "status": "paid"},
    3: {"invoice_id": 102, "amount": 175.5, "status": "unpaid"},
    # ...
}

def access_invoice(user_id: int, client_id: int) -> dict | str:
    """
    Retrieve an invoice for a given client if the requesting user is authorized.

    Parameters
    ----------
    user_id : int
        The ID of the user attempting to access an invoice.
    client_id : int
        The ID of the customer whose invoice is being requested.

    Returns
    -------
    dict or str
        The invoice data if access is granted, otherwise the string "Unauthorized".

    Raises
    ------
    KeyError
        If either the user_id or client_id is not present in their respective dictionaries.
    """
    # Validate existence of the user and invoice
    if user_id not in USER_ROLES:
        raise KeyError(f"Unknown user_id: {user_id}")
    if client_id not in INVOICES:
        raise KeyError(f"Unknown client_id: {client_id}")

    role = USER_ROLES[user_id]

    # Authorization logic
    if role == "admin" or user_id == client_id:
        return INVOICES[client_id]

    return "Unauthorized"