import json
from typing import Any, Dict

# Example data structures (replace with real data in production)
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
}
INVOICES: Dict[int, Any] = {
    2: {"invoice_id": "INV-1001", "amount": 250.00, "status": "paid"},
    3: {"invoice_id": "INV-1002", "amount": 125.50, "status": "unpaid"},
}


def fetch_invoice(requester_id: int, owner_id: int) -> Any:
    """
    Retrieve an invoice if the requester is authorized.

    Parameters
    ----------
    requester_id : int
        The ID of the user attempting to fetch an invoice.
    owner_id : int
        The ID of the customer whose invoice is requested.

    Returns
    -------
    dict or str
        The invoice details if authorized, otherwise the string 'Unauthorized'.

    Raises
    ------
    ValueError
        If either requester_id or owner_id is not present in USER_ROLES.
    KeyError
        If the requested invoice does not exist for owner_id.
    """
    # Validate presence of requester and owner in the role mapping
    if requester_id not in USER_ROLES:
        raise ValueError(f"Requester ID {requester_id} is unknown.")
    if owner_id not in USER_ROLES:
        raise ValueError(f"Owner ID {owner_id} is unknown.")

    # Check permissions
    requester_role = USER_ROLES[requester_id]
    if requester_id != owner_id and requester_role.lower() != "admin":
        return "Unauthorized"

    # Retrieve the invoice
    if owner_id not in INVOICES:
        raise KeyError(f"No invoice found for owner ID {owner_id}")

    return INVOICES[owner_id]


# Example usage (for testing purposes only)
if __name__ == "__main__":
    try:
        print(fetch_invoice(1, 2))   # Admin accessing customer 2's invoice
        print(fetch_invoice(2, 2))   # Customer accessing own invoice
        print(fetch_invoice(3, 2))   # Unauthorized access attempt
    except Exception as e:
        print(f"Error: {e}")