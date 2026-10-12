import threading

# Example in‑memory database of accounts.
ACCOUNTS_DB = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user123", "balance": 1500.00},
    "ACC002": {"account_number": "ACC002", "owner_id": "user456", "balance": 3000.00},
    # Add more accounts as needed
}

# A lock to serialize access to the account balances.
_ACCOUNTS_LOCK = threading.Lock()


def transfer_funds(
    user_id: str,
    user_role: str,
    from_account: str,
    to_account: str,
    amount: float
) -> str:
    """
    Transfer money between two accounts with proper authorization checks.

    Parameters
    ----------
    user_id : str
        The ID of the user attempting to transfer funds.
    user_role : str
        Role of the user: 'account_owner', 'bank_admin', or 'customer_service'.
    from_account : str
        The account number to transfer funds from.
    to_account : str
        The account number to transfer funds to.
    amount : float
        The amount of money to transfer.

    Returns
    -------
    str
        Confirmation message if the transfer succeeded.

    Raises
    ------
    ValueError
        If an account does not exist, if the amount is non‑positive,
        or if there are insufficient funds.
    PermissionError
        If the user is not authorized to perform the transfer.
    """
    if amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Retrieve accounts atomically to avoid race conditions.
    with _ACCOUNTS_LOCK:
        src = ACCOUNTS_DB.get(from_account)
        dst = ACCOUNTS_DB.get(to_account)

    if src is None or dst is None:
        raise ValueError("One or both accounts do not exist.")

    # Authorization check – CWE‑863 protection
    authorized = False
    if user_role == "bank_admin":
        # Admin can transfer between any accounts.
        authorized = True
    elif user_role == "account_owner":
        # Owner can only transfer from their own account.
        authorized = (src["owner_id"] == user_id)
    # 'customer_service' role is explicitly denied transfer rights.

    if not authorized:
        raise PermissionError("User is not authorized to perform this transfer.")

    # Perform the transfer atomically.
    with _ACCOUNTS_LOCK:
        if src["balance"] < amount:
            raise ValueError("Insufficient funds in the source account.")
        src["balance"] -= amount
        dst["balance"] += amount

    return (
        f"Transfer of ${amount:,.2f} from {from_account} "
        f"to {to_account} completed successfully."
    )