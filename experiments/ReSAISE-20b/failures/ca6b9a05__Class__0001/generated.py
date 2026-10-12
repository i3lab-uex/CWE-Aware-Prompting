import threading

# Example accounts database (in-memory for demonstration purposes)
ACCOUNTS_DB = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user123", "balance": 1500.00},
    "ACC002": {"account_number": "ACC002", "owner_id": "user456", "balance": 300.00},
    # Add more accounts as needed
}

# A simple lock to avoid race conditions when updating balances
_db_lock = threading.Lock()


def move_funds(u_id: str, u_role: str, source_account: str,
               destination_account: str, money: float) -> str:
    """
    Transfer funds between two accounts.

    Parameters
    ----------
    u_id : str
        Identifier of the individual requesting the transfer.
    u_role : str
        Role of the individual ('account_owner', 'bank_admin',
        'customer_service').
    source_account : str
        Account number to debit.
    destination_account : str
        Account number to credit.
    money : float
        Amount to transfer.

    Returns
    -------
    str
        Success message indicating the transfer was completed.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    ValueError
        If accounts do not exist, balances are insufficient,
        or money is non‑positive.
    """

    # Basic validation
    if money <= 0:
        raise ValueError("Transfer amount must be positive")

    # Retrieve accounts safely
    src = ACCOUNTS_DB.get(source_account)
    dst = ACCOUNTS_DB.get(destination_account)

    if src is None or dst is None:
        raise ValueError("One or both accounts do not exist")

    # Authorization logic
    if u_role == "bank_admin":
        # Admin can transfer from any account to any account
        authorized = True
    elif u_role == "account_owner":
        # Owner can transfer only from accounts they own
        authorized = src["owner_id"] == u_id and dst["owner_id"] == u_id
    elif u_role == "customer_service":
        # Customer service can transfer between any accounts, but only if the
        # source account belongs to the requesting user or is a public account.
        authorized = src["owner_id"] == u_id
    else:
        authorized = False

    if not authorized:
        raise PermissionError("Unauthorized transfer attempt")

    # Perform the transfer atomically
    with _db_lock:
        if src["balance"] < money:
            raise ValueError("Insufficient funds in source account")

        # Update balances
        src["balance"] -= money
        dst["balance"] += money

    return (
        f"Transfer of ${money:,.2f} from {source_account} "
        f"to {destination_account} completed successfully."
    )