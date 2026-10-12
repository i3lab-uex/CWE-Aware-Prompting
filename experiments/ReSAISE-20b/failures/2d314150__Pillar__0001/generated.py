import threading

# Simulated accounts database
ACCOUNTS_DB = {
    "ACC123": {"account_number": "ACC123", "owner_id": "U1", "balance": 5000.0},
    "ACC456": {"account_number": "ACC456", "owner_id": "U2", "balance": 3000.0},
    # Add more accounts as needed
}

# Lock for thread‑safety when updating balances
db_lock = threading.Lock()


def transfer_funds(
    user_id: str,
    user_role: str,
    from_account: str,
    to_account: str,
    amount: float,
) -> str:
    """
    Transfer funds between two accounts with proper authorization checks.

    Parameters
    ----------
    user_id : str
        ID of the user attempting the transfer.
    user_role : str
        Role of the user ('account_owner', 'bank_admin', or 'customer_service').
    from_account : str
        Account number to transfer funds from.
    to_account : str
        Account number to transfer funds to.
    amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Confirmation message if the transfer is successful.

    Raises
    ------
    ValueError
        If either account does not exist, insufficient funds,
        or the amount is non‑positive.
    """
    if amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Retrieve accounts atomically
    with db_lock:
        src = ACCOUNTS_DB.get(from_account)
        dst = ACCOUNTS_DB.get(to_account)

    if src is None or dst is None:
        raise ValueError("One or both accounts do not exist.")

    # Authorization check
    if user_role == "account_owner":
        if src["owner_id"] != user_id or dst["owner_id"] != user_id:
            return "Authorization error: owners can only transfer between their own accounts."
    elif user_role not in ("bank_admin", "customer_service"):
        return "Authorization error: insufficient privileges."

    # Ensure sufficient funds
    with db_lock:
        if src["balance"] < amount:
            raise ValueError("Insufficient funds in the source account.")

        # Perform transfer
        src["balance"] -= amount
        dst["balance"] += amount

    return (
        f"Transfer of ${amount:.2f} from {from_account} to {to_account} "
        f"completed successfully."
    )