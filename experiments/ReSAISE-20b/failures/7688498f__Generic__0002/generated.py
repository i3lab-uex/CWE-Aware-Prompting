import threading

# Example in‑memory database of accounts.
ACCOUNTS_DB = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "USR001", "balance": 5000.00},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "USR002", "balance": 3000.00},
    # Add more accounts as needed.
}

# A global lock to ensure atomic updates in a multi‑threaded environment.
_db_lock = threading.Lock()


def fund_transfer(u_identifier: str,
                  u_role: str,
                  account_from: str,
                  account_to: str,
                  transfer_amount: float) -> str:
    """
    Transfer funds between two accounts after performing authorization checks.

    Parameters
    ----------
    u_identifier : str
        Identifier of the individual requesting the transfer.
    u_role : str
        Role held by the individual ('account_owner', 'bank_admin',
        or 'customer_service').
    account_from : str
        Account number to debit.
    account_to : str
        Account number to credit.
    transfer_amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message indicating the transfer was completed.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    ValueError
        If accounts are missing, balances insufficient or input is invalid.
    """

    # Basic validation of arguments
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Retrieve accounts
    with _db_lock:
        acct_from = ACCOUNTS_DB.get(account_from)
        acct_to = ACCOUNTS_DB.get(account_to)

    if not acct_from or not acct_to:
        raise ValueError("One or both account numbers are invalid.")

    # Authorization logic
    authorized = False

    if u_role == "bank_admin":
        authorized = True
    elif u_role == "account_owner" and acct_from["owner_id"] == u_identifier:
        authorized = True
    # customer_service is not allowed to initiate transfers in this simplified model

    if not authorized:
        raise PermissionError("User is not authorized to perform this transfer.")

    # Perform the transfer atomically
    with _db_lock:
        if acct_from["balance"] < transfer_amount:
            raise ValueError("Insufficient funds in the source account.")
        acct_from["balance"] -= transfer_amount
        acct_to["balance"] += transfer_amount

    return (f"Transfer of ${transfer_amount:,.2f} from "
            f"{account_from} to {account_to} completed successfully.")