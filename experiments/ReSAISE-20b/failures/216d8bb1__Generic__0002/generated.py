from typing import Any, Dict

# Example role mapping: user_id -> set of roles (e.g., {'admin', 'user'})
USER_ROLES: Dict[int, set] = {
    1: {"admin"},
    2: {"user"},
    3: {"user"},
}

# Example invoice storage: client_id -> invoice data
INVOICES: Dict[int, Any] = {
    2: {"amount": 150.0, "date": "2023-10-01", "items": ["product A"]},
    3: {"amount": 200.0, "date": "2023-10-05", "items": ["product B"]},
}


def access_invoice(user_id: int, client_id: int) -> Any:
    """
    Retrieve an invoice for a given client if the requesting user has
    sufficient privileges.

    Parameters:
        user_id (int): The ID of the user making the request.
        client_id (int): The ID of the customer whose invoice is requested.

    Returns:
        Any: The invoice data if access is granted.
        str: 'Unauthorized' if the user lacks permission or the
             invoice does not exist.

    Notes:
        - An 'admin' role grants access to all invoices.
        - A user can only view their own invoice (client_id == user_id).
    """
    # Check if the user exists in role mapping
    roles = USER_ROLES.get(user_id)
    if not roles:
        return "Unauthorized"

    # Permission check
    has_access = "admin" in roles or user_id == client_id
    if not has_access:
        return "Unauthorized"

    # Retrieve the invoice; return Unauthorized if missing
    invoice = INVOICES.get(client_id)
    if invoice is None:
        return "Unauthorized"

    return invoice