# ────────────────────────────────────────────────────────────────
#  Invoice retrieval with role‑based access control
# ────────────────────────────────────────────────────────────────

from typing import Any, Dict

# Example data structures (in real usage these would be loaded from a DB or config)
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    # ...
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.0, "items": ["widget", "gadget"]},
    3: {"invoice_id": 102, "amount": 175.5, "items": ["widget"]},
    # ...
}


def get_invoice(requester_id: int, client_id: int) -> Any:
    """
    Return the invoice data for `client_id` if the requester is authorized.

    Parameters
    ----------
    requester_id : int
        The user ID of the individual making the request.
    client_id : int
        The user ID whose invoice is being requested.

    Returns
    -------
    Any
        The invoice data if authorized; otherwise the string 'Unauthorized'.

    Notes
    -----
    - A user is authorized if they are requesting their own invoice.
    - An administrator (role == 'admin') can request any customer's invoice.
    - If the requested client has no invoice, a KeyError will be raised.
    """
    # Verify requester exists
    if requester_id not in USER_ROLES:
        return "Unauthorized"

    # Verify client exists
    if client_id not in INVOICES:
        raise KeyError(f"No invoice found for user ID {client_id}")

    # Check authorization
    if requester_id == client_id or USER_ROLES.get(requester_id) == "admin":
        return INVOICES[client_id]

    # Unauthorized access attempt
    return "Unauthorized"