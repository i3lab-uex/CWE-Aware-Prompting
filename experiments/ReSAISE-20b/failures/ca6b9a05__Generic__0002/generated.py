import threading

# Example accounts database (would normally be a persistent store)
ACCOUNTS_DB = {
    "ACC001": {"account_number": "ACC001", "owner_id": "U123", "balance": 1000.0},
    "ACC002": {"account_number": "ACC002", "owner_id": "U456", "balance": 500.0},
    "ACC003": {"account_number": "ACC003", "owner_id": "U789", "balance": 750.0},
}

# Lock for thread‑safe updates
_db_lock = threading.Lock()


def move_funds(u_id: str, u_role: str, source_account: str,
               destination_account: str, money: float) -> str:
    """
    Transfer funds between two accounts if the user is authorized.

    Parameters
    ----------
    u_id : str
        Identifier of the user requesting the transfer.
    u_role : str
        Role of the user ('account_owner', 'bank_admin', 'customer_service').
    source_account : str
        Account number from which money will be withdrawn.
    destination_account : str
        Account number to which money will be deposited.
    money : float
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
        If accounts are invalid, insufficient funds or negative amount.
    """
    if money <= 0:
        raise ValueError("Transfer amount must be positive")

    # Validate accounts
    src = ACCOUNTS_DB.get(source_account)
    dst = ACCOUNTS_DB.get(destination_account)

    if src is None:
        raise ValueError(f"Source account {source_account} does not exist")
    if dst is None:
        raise ValueError(f"Destination account {destination_account} does not exist")

    # Authorization check
    authorized = False
    if u_role == "bank_admin":
        authorized = True
    elif u_role == "account_owner" and src["owner_id"] == u_id:
        authorized = True
    # customer_service or others are not allowed to move funds directly

    if not authorized:
        raise PermissionError("User is not authorized to transfer funds")

    # Perform the transfer atomically
    with _db_lock:
        if src["balance"] < money:
            raise ValueError("Insufficient funds in source account")

        # Update balances
        src["balance"] -= money
        dst["balance"] += money

    return (f"Transfer of ${money:,.2f} from {source_account} "
            f"to {destination_account} completed successfully.")


# Example usage (commented out – remove comments to run)
# try:
#     msg = move_funds("U123", "account_owner", "ACC001", "ACC002", 200.0)
#     print(msg)
# except Exception as e:
#     print(f"Error: {e}")