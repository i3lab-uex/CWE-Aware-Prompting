# -*- coding: utf-8 -*-

"""
Secure invoice retrieval module.

The implementation ensures that:
* Only administrators can download any customer's invoice.
* Regular users can only download their own invoice.
* Non‑existent invoices raise a descriptive error.
"""

from typing import Dict, Any

# Example role definitions. In production these would come from a database or
# an external service.
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    # ... more users
}

# Example invoice storage. In production this might be a file system,
# database, or cloud object store.
INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.00, "date": "2024-07-01"},
    3: {"invoice_id": 102, "amount": 150.00, "date": "2024-07-02"},
    # ... more invoices
}


def fetch_invoice(user_id: int, customer: int) -> Any:
    """
    Retrieve the invoice for a given customer if the requesting user is authorized.

    Parameters
    ----------
    user_id : int
        The ID of the user making the request.
    customer : int
        The ID of the customer whose invoice is being requested.

    Returns
    -------
    Any
        The invoice data associated with the customer.

    Raises
    ------
    KeyError
        If either `user_id` or the requested customer's invoice does not exist.
    PermissionError
        If the requesting user is not authorized to access the requested invoice.

    Notes
    -----
    * Administrators (`role == "admin"`) can access any invoice.
    * Regular users can only access their own invoice.
    """
    # Verify that the requesting user exists
    if user_id not in USER_ROLES:
        raise KeyError(f"User ID {user_id} not found.")

    # Verify that the requested customer has an invoice
    if customer not in INVOICES:
        raise KeyError(f"Invoice for customer ID {customer} does not exist.")

    # Authorization check
    role = USER_ROLES[user_id]
    if role != "admin" and user_id != customer:
        raise PermissionError("Unauthorized")

    # Return a copy to prevent accidental mutation of the stored data
    return INVOICES[customer].copy()


# Example usage (commented out; remove comments to run tests)
# if __name__ == "__main__":
#     try:
#         print(fetch_invoice(1, 2))  # Admin fetching customer 2's invoice
#         print(fetch_invoice(2, 2))  # Customer fetching own invoice
#         print(fetch_invoice(3, 2))  # Unauthorized attempt
#     except Exception as e:
#         print(e)