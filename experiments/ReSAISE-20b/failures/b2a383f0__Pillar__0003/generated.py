# retrieve_invoice.py

"""
This module provides a single function `retrieve_invoice` that enforces proper
access control when retrieving invoices. It ensures that a user can only view
their own invoice unless they have an administrative role.

Security Considerations:
- The function checks both user identity and role before returning sensitive
  invoice data, mitigating CWE‑284 (Improper Access Control).
- No side effects or database connections are performed; the data is
  retrieved from in‑memory dictionaries supplied at runtime.
"""

from typing import Dict, Any

# Example role and invoice data (in a real application these would come from
# persistent storage or an external service).
USER_ROLES: Dict[int, list[str]] = {
    1: ["admin"],
    2: ["customer"],
    3: ["customer"],
}

INVOICES: Dict[int, dict[str, Any]] = {
    2: {"invoice_id": "INV-001", "amount": 250.0, "status": "paid"},
    3: {"invoice_id": "INV-002", "amount": 150.0, "status": "unpaid"},
}


def retrieve_invoice(requester_id: int, customer_request_id: int) -> Any:
    """
    Retrieve an invoice if the requester is authorized.

    Parameters
    ----------
    requester_id : int
        The ID of the user attempting to access an invoice.
    customer_request_id : int
        The ID of the customer whose invoice is being requested.

    Returns
    -------
    dict or str
        The invoice data if access is permitted; otherwise the string
        'Unauthorized'.

    Notes
    -----
    - A user can access their own invoice.
    - Users with the role 'admin' can access any customer's invoice.
    """
    # Quick sanity check: ensure both IDs are present in our data sets
    if requester_id not in USER_ROLES or customer_request_id not in INVOICES:
        return "Unauthorized"

    # Admins can access any invoice
    if "admin" in USER_ROLES.get(requester_id, []):
        return INVOICES[customer_request_id]

    # Regular users can only access their own invoice
    if requester_id == customer_request_id:
        return INVOICES[customer_request_id]

    # Any other case is unauthorized
    return "Unauthorized"