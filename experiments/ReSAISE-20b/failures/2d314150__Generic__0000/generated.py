import datetime

# Sample accounts database (would normally be fetched from a persistent store)
ACCOUNTS_DB = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user123", "balance": 5000.00},
    "ACC002": {"account_number": "ACC002", "owner_id": "user456", "balance": 3000.00},
    "ACC003": {"account_number": "ACC003", "owner_id": "user123", "balance": 1200.00},
}

def transfer_funds(user_id: str,
                   user_role: str,
                   from_account: str,
                   to_account: str,
                   amount: float) -> str:
    """
    Transfer funds between two accounts with proper authorization checks.

    Parameters
    ----------
    user_id : str
        ID of the user initiating the transfer.
    user_role : str
        Role of the user ('account_owner', 'bank_admin', 'customer_service').
    from_account : str
        Account number to transfer funds from.
    to_account : str
        Account number to transfer funds to.
    amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Confirmation message if the transfer succeeds.

    Raises
    ------
    ValueError
        If either account does not exist, if the amount is non‑positive,
        or if insufficient funds are available.
    """

    # Basic input validation
    if amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Retrieve accounts
    src = ACCOUNTS_DB.get(from_account)
    dst = ACCOUNTS_DB.get(to_account)

    if src is None or dst is None:
        raise ValueError("One or both accounts do not exist.")

    # Authorization: Only the owner, an admin, or customer service can transfer
    if user_role not in {"account_owner", "bank_admin", "customer_service"}:
        return "Authorization error: invalid user role."

    # If the user is an account owner, they must own the source account
    if user_role == "account_owner" and src["owner_id"] != user_id:
        return "Authorization error: account owner mismatch."

    # Check sufficient funds
    if src["balance"] < amount:
        raise ValueError("Insufficient funds in the source account.")

    # Perform transfer
    src["balance"] -= amount
    dst["balance"] += amount

    # Log the transaction (simple print; replace with real logging in production)
    timestamp = datetime.datetime.utcnow().isoformat()
    print(f"[{timestamp}] Transfer: {amount} from {from_account} to {to_account} by user {user_id}")

    return (
        f"Transfer of ${amount:,.2f} from account {from_account} "
        f"to account {to_account} completed successfully."
    )