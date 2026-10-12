from typing import Any, Dict

# Example role mapping: user_id -> list of roles
USER_ROLES: Dict[int, list[str]] = {
    1: ["admin"],
    2: ["customer"],
    3: ["customer"],
}

# Example invoice storage: user_id -> invoice data
INVOICES: Dict[int, Any] = {
    2: {"invoice_id": "INV-002", "amount": 120.0},
    3: {"invoice_id": "INV-003", "amount": 75.5},
}

def download_invoice(current_user_id: int, customer_id: int) -> Any:
    """
    Return the invoice data for `customer_id` if the requesting user
    (current_user_id) is authorized.

    Authorization rules:
        - The customer can download their own invoice.
        - An admin user can download any customer's invoice.

    Parameters
    ----------
    current_user_id : int
        ID of the user making the request.
    customer_id : int
        ID of the customer whose invoice is requested.

    Returns
    -------
    Any
        The invoice data if authorized, otherwise the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If either user ID is not present in the role mapping or invoice data.
    """
    # Verify that both users exist
    if current_user_id not in USER_ROLES or customer_id not in INVOICES:
        raise KeyError("User ID(s) not found.")

    # Check if the current user is an admin
    is_admin = "admin" in USER_ROLES.get(current_user_id, [])

    # Allow download if user is admin or downloading own invoice
    if is_admin or current_user_id == customer_id:
        return INVOICES[customer_id]

    # Otherwise deny access
    return "Unauthorized"