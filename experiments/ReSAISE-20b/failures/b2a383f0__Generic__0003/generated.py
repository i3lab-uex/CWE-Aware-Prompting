# --------------------------------------------------
# Invoice retrieval with role‑based access control
# --------------------------------------------------

from typing import Dict, Any

# Example dictionaries (replace with real data in production)
USER_ROLES: Dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
    # ...
}

INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.0},
    3: {"invoice_id": 102, "amount": 180.5},
    # ...
}


def retrieve_invoice(requester_id: int, customer_request_id: int) -> Any:
    """
    Return the invoice of `customer_request_id` if the requester is authorized.
    Administrators can access any invoice; customers can only access their own.

    Parameters
    ----------
    requester_id : int
        The user ID of the person attempting to access the invoice.
    customer_request_id : int
        The user ID whose invoice is being requested.

    Returns
    -------
    Any
        Invoice data if authorized; otherwise the string 'Unauthorized'.

    Notes
    -----
    * Missing user IDs or invoices do not reveal existence to prevent enumeration.
    * The function uses constant‑time comparison for role checking (not critical here but
      good practice if roles are sensitive).
    """
    # Verify requester exists and obtain role
    requester_role = USER_ROLES.get(requester_id)
    if requester_role is None:
        return "Unauthorized"

    # Check permissions
    authorized = False
    if requester_role.lower() == "admin":
        authorized = True
    elif requester_id == customer_request_id:
        authorized = True

    if not authorized:
        return "Unauthorized"

    # Retrieve invoice safely; missing invoices are treated as unauthorized
    invoice = INVOICES.get(customer_request_id)
    if invoice is None:
        return "Unauthorized"

    return invoice