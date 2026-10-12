# -*- coding: utf-8 -*-

"""
Security‑aware invoice retrieval module.

The implementation follows the principle of least privilege:
* Administrators can retrieve any invoice.
* Regular customers can only retrieve their own invoices.
"""

# Example role and invoice stores (to be replaced with real data sources)
USER_ROLES = {
    # user_id: role
    1: "admin",
    2: "customer",
    3: "customer",
}

INVOICES = {
    # invoice_owner_id: invoice_data
    2: {"invoice_id": 101, "amount": 250.0, "items": ["widget", "gadget"]},
    3: {"invoice_id": 102, "amount": 175.5, "items": ["thingamajig"]},
}


def retrieve_invoice(logged_in_user_id: int, invoice_owner_id: int):
    """
    Retrieve an invoice if the caller is authorized.

    Parameters
    ----------
    logged_in_user_id : int
        ID of the user attempting to access an invoice.
    invoice_owner_id : int
        ID of the customer whose invoice is being requested.

    Returns
    -------
    dict | str
        Invoice data dictionary if access is permitted; otherwise the string
        'Unauthorized'.

    Notes
    -----
    - Administrator users (role == "admin") can access any invoice.
    - Non‑administrators may only access invoices belonging to themselves.
    - If the requested invoice does not exist, the function returns
      'Unauthorized' to avoid leaking information about account existence.
    """
    # Retrieve the role of the requesting user, defaulting to None
    user_role = USER_ROLES.get(logged_in_user_id)

    # Determine if the request is authorized
    authorized = False

    if user_role == "admin":
        authorized = True
    elif logged_in_user_id == invoice_owner_id:
        authorized = True

    if not authorized:
        return "Unauthorized"

    # Fetch the invoice; if missing, avoid disclosing its absence
    invoice = INVOICES.get(invoice_owner_id)
    if invoice is None:
        return "Unauthorized"

    # Return a copy to prevent accidental mutation of the global store
    return dict(invoice)


# Example usage (for testing purposes only)
if __name__ == "__main__":
    print(retrieve_invoice(1, 2))   # admin accessing customer 2's invoice
    print(retrieve_invoice(2, 2))   # owner accessing own invoice
    print(retrieve_invoice(3, 2))   # customer trying to access another's invoice
    print(retrieve_invoice(4, 2))   # unknown user