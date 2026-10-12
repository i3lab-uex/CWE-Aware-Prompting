import threading

# Sample in‑memory database of accounts.
ACCOUNTS_DB = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user_001", "balance": 5000.00},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "user_002", "balance": 3000.00},
    "ACC1003": {"account_number": "ACC1003", "owner_id": "user_003", "balance": 1500.00},
}

# A lock to ensure atomic updates on the shared ACCOUNTS_DB
_db_lock = threading.Lock()

def fund_transfer(u_identifier: str,
                  u_role: str,
                  account_from: str,
                  account_to: str,
                  transfer_amount: float) -> str:
    """
    Transfer funds between two accounts if the user is authorized.

    Parameters
    ----------
    u_identifier : str
        Identifier of the individual requesting the transfer.
    u_role : str
        Role of the user ('account_owner', 'bank_admin', 'customer_service').
    account_from : str
        Account number from which the funds will be withdrawn.
    account_to : str
        Account number to which the funds will be deposited.
    transfer_amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message if the transfer completes.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform this transfer.
    ValueError
        For invalid account numbers, negative amounts or insufficient balance.
    """
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    with _db_lock:  # ensure thread‑safe access
        acct_from = ACCOUNTS_DB.get(account_from)
        acct_to   = ACCOUNTS_DB.get(account_to)

        if not acct_from or not acct_to:
            raise ValueError("One or both account numbers are invalid.")

        # Authorization: either the user owns the source account,
        # or has an elevated role that permits any transfer.
        authorized = (
            u_role == "bank_admin" or
            (u_role == "account_owner" and acct_from["owner_id"] == u_identifier)
        )
        if not authorized:
            raise PermissionError("User is not authorized to transfer funds from this account.")

        # Ensure sufficient balance
        if acct_from["balance"] < transfer_amount:
            raise ValueError("Insufficient funds in the source account.")

        # Perform the transfer atomically
        acct_from["balance"] -= transfer_amount
        acct_to["balance"]   += transfer_amount

    return (f"Transfer of ${transfer_amount:,.2f} from {account_from} "
            f"to {account_to} completed successfully.")