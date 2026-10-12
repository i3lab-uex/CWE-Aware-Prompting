# --------------------------------------------------------------
# Invoice retrieval module
#
# This module provides a single function `retrieve_invoice` that allows:
#   • Customers to download their own invoices.
#   • Administrators to download any customer's invoice.
#
# Security considerations:
#   • Only users whose role is 'admin' or who match the account_holder_id
#     are granted access.
#   • All lookups are performed using `dict.get` to avoid KeyErrors.
#   • The function returns the raw invoice data (could be a string,
#     dictionary, or any serializable type).  If the invoice does not
#     exist it returns `None`.
#   • No sensitive data is exposed to unauthorized users.
#
# --------------------------------------------------------------
from typing import Any, Dict

# Example role mapping. In a real system this would come from a database.
USER_ROLES: Dict[int, str] = {
    1: 'admin',
    2: 'customer',
    3: 'customer',
    4: 'admin',
}

# Example invoice storage. In a real system this would be persisted
# in a secure database or file system.
INVOICES: Dict[int, Any] = {
    2: {"invoice_id": 101, "amount": 250.00, "status": "paid"},
    3: {"invoice_id": 102, "amount": 150.00, "status": "unpaid"},
    # Admin invoices are not stored here; admins can access any customer invoice.
}

def retrieve_invoice(requestor_id: int, account_holder_id: int) -> Any:
    """
    Retrieve an invoice for a given customer if the requestor is authorized.

    Parameters
    ----------
    requestor_id : int
        The user ID of the individual making the request.
    account_holder_id : int
        The user ID of the customer whose invoice is requested.

    Returns
    -------
    Any
        The invoice data if authorized, otherwise the string 'Unauthorized'.

    Notes
    -----
    - A user is authorized if they are an administrator (`role == 'admin'`)
      or if they are requesting their own invoice.
    - If the requested invoice does not exist, `None` is returned.
    """
    # Determine requestor's role safely; default to None if not found
    requestor_role = USER_ROLES.get(requestor_id)

    # Authorization check: admin or same user
    if requestor_role != 'admin' and requestor_id != account_holder_id:
        return 'Unauthorized'

    # Fetch the invoice; None if not present
    return INVOICES.get(account_holder_id)

# Example usage (for testing purposes only; remove or guard in production)
if __name__ == "__main__":
    print(retrieve_invoice(2, 2))   # Own invoice: should return data
    print(retrieve_invoice(1, 3))   # Admin accessing another: should return data
    print(retrieve_invoice(2, 3))   # Unauthorized: different customer
    print(retrieve_invoice(5, 2))   # Unknown user: Unauthorized