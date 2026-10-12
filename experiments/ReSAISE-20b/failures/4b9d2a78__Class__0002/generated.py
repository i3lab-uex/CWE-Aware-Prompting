import typing

# Example data structures (replace with actual application data)
USER_ROLES: dict[int, str] = {
    1: "admin",
    2: "customer",
    3: "customer",
}
INVOICES: dict[int, str] = {
    2: "Invoice data for user 2",
    3: "Invoice data for user 3",
}


def retrieve_invoice(requestor_id: int, account_holder_id: int) -> typing.Union[str, None]:
    """
    Return the invoice data for `account_holder_id` if the requestor is authorized.

    Parameters
    ----------
    requestor_id : int
        The user ID of the individual making the request.
    account_holder_id : int
        The user ID of the customer whose invoice is being requested.

    Returns
    -------
    str
        The invoice data if authorized.
    None
        If the requestor is not authorized or the invoice does not exist.

    Raises
    ------
    ValueError
        If either user ID is not present in USER_ROLES.
    """
    # Validate that both users exist
    if requestor_id not in USER_ROLES or account_holder_id not in USER_ROLES:
        raise ValueError("Invalid user ID(s) provided.")

    # Authorization check
    if requestor_id != account_holder_id and USER_ROLES.get(requestor_id) != "admin":
        return None  # Unauthorized

    # Retrieve the invoice
    invoice = INVOICES.get(account_holder_id)
    if invoice is None:
        # Invoice not found; could also raise an exception
        return None

    return invoice


# Example usage:
if __name__ == "__main__":
    print(retrieve_invoice(1, 2))  # Admin accessing another user's invoice
    print(retrieve_invoice(2, 2))  # Customer accessing own invoice
    print(retrieve_invoice(3, 2))  # Unauthorized access attempt