import threading

# Example account database
ACCOUNTS_DB = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user123", "balance": 1000.0},
    "ACC002": {"account_number": "ACC002", "owner_id": "user456", "balance": 500.0},
    # Add more accounts as needed
}

# Lock to ensure thread‑safe updates of balances
_db_lock = threading.Lock()


def fund_transfer(
    u_identifier: str,
    u_role: str,
    account_from: str,
    account_to: str,
    transfer_amount: float,
) -> str:
    """
    Transfer funds from one account to another.

    Parameters
    ----------
    u_identifier : str
        Identifier of the user requesting the transfer.
    u_role : str
        Role of the user (e.g., 'account_owner', 'bank_admin', 'customer_service').
    account_from : str
        Account number to debit.
    account_to : str
        Account number to credit.
    transfer_amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    ValueError
        If account numbers are invalid, amount is non‑positive,
        or insufficient funds.
    """

    # Basic validation
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Retrieve accounts
    src = ACCOUNTS_DB.get(account_from)
    dst = ACCOUNTS_DB.get(account_to)

    if src is None or dst is None:
        raise ValueError("One or both account numbers are invalid.")

    # Authorization logic
    authorized = False

    if u_role == "bank_admin":
        # Admins can transfer any funds
        authorized = True

    elif u_role == "customer_service":
        # Customer service can transfer only if the user is the owner of the source account
        authorized = (src["owner_id"] == u_identifier)

    elif u_role == "account_owner":
        # Owner can transfer only from their own account
        authorized = (src["owner_id"] == u_identifier)

    # Add more role rules here as needed

    if not authorized:
        raise PermissionError("User is not authorized to perform this transfer.")

    # Perform the transfer atomically
    with _db_lock:
        if src["balance"] < transfer_amount:
            raise ValueError("Insufficient funds in source account.")

        src["balance"] -= transfer_amount
        dst["balance"] += transfer_amount

    return (
        f"Transfer of ${transfer_amount:.2f} from {account_from} "
        f"to {account_to} completed successfully."
    )