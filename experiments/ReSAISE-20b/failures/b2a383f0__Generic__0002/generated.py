# ────────────────────────────────────────
# Invoice retrieval module
# ────────────────────────────────────────

from typing import Any, Dict

# Example data – in a real system these would be loaded from a database or config
USER_ROLES: Dict[int, list[str]] = {
    1: ["admin"],
    2: ["customer"],
    3: ["customer"],
    # ... other users
}

INVOICES: Dict[int, dict[str, Any]] = {
    2: {"invoice_id": 101, "amount": 250.0, "status": "paid"},
    3: {"invoice_id": 102, "amount": 180.0, "status": "unpaid"},
    # ... other invoices
}


def retrieve_invoice(requester_id: int, customer_request_id: int) -> Any:
    """
    Retrieve the invoice for a given customer if the requester is authorized.

    Parameters
    ----------
    requester_id : int
        The user ID of the person attempting to access the invoice.
    customer_request_id : int
        The user ID of the customer whose invoice is being requested.

    Returns
    -------
    dict or str
        The invoice data if access is permitted, otherwise the string 'Unauthorized'.

    Notes
    -----
    - Administrators (role containing 'admin') may access any invoice.
    - Regular customers can only retrieve their own invoices.
    - If the invoice does not exist, access is treated as unauthorized.
    """
    # Determine if requester is an admin
    roles = USER_ROLES.get(requester_id, [])
    is_admin = "admin" in [role.lower() for role in roles]

    # Authorization logic
    if not (is_admin or requester_id == customer_request_id):
        return "Unauthorized"

    # Fetch the invoice
    invoice = INVOICES.get(customer_request_id)
    if invoice is None:
        return "Unauthorized"

    # Return a copy to avoid accidental mutation
    return invoice.copy()


# ────────────────────────────────────────
# Example usage (for testing purposes)
# ────────────────────────────────────────

if __name__ == "__main__":
    # Admin accessing customer 2's invoice
    print(retrieve_invoice(1, 2))  # Should return the invoice

    # Customer accessing their own invoice
    print(retrieve_invoice(2, 2))  # Should return the invoice

    # Customer attempting to access another customer's invoice
    print(retrieve_invoice(2, 3))  # Should return 'Unauthorized'

    # Non-existent invoice
    print(retrieve_invoice(1, 99))  # Should return 'Unauthorized'