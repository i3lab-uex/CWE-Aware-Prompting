import threading

# Sample accounts database (in-memory)
ACCOUNTS_DB = {
    "ACC001": {"account_number": "ACC001", "owner_id": "U123", "balance": 1500.00},
    "ACC002": {"account_number": "ACC002", "owner_id": "U456", "balance": 3000.00},
    # Add more accounts as needed
}

# A simple lock per account to avoid race conditions in concurrent environments
ACCOUNT_LOCKS = {acc: threading.Lock() for acc in ACCOUNTS_DB}


def transfer_funds(user_id: str, user_role: str,
                   from_account: str, to_account: str,
                   amount: float) -> str:
    """
    Transfer funds between two accounts with authorization checks.

    Args:
        user_id (str): ID of the user performing the transfer.
        user_role (str): Role of the user. Allowed values:
            - 'account_owner'
            - 'bank_admin'
            - 'customer_service' (cannot transfer)
        from_account (str): Source account number.
        to_account (str): Destination account number.
        amount (float): Amount to transfer.

    Returns:
        str: Confirmation message if the transfer succeeds.

    Raises:
        ValueError: If accounts do not exist, insufficient funds,
                    invalid amount, or unauthorized action.
    """
    # Basic validation
    if amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Ensure both accounts exist
    src = ACCOUNTS_DB.get(from_account)
    dst = ACCOUNTS_DB.get(to_account)

    if src is None or dst is None:
        raise ValueError("One or both accounts do not exist.")

    # Authorization check
    if user_role == "bank_admin":
        authorized = True
    elif user_role == "account_owner" and src["owner_id"] == user_id:
        authorized = True
    else:
        authorized = False

    if not authorized:
        raise ValueError("User is not authorized to transfer funds from this account.")

    # Acquire locks on both accounts to prevent race conditions
    first_lock, second_lock = (
        (ACCOUNT_LOCKS[from_account], ACCOUNT_LOCKS[to_account])
        if from_account < to_account
        else (ACCOUNT_LOCKS[to_account], ACCOUNT_LOCKS[from_account])
    )

    with first_lock:
        with second_lock:
            # Check sufficient funds
            if src["balance"] < amount:
                raise ValueError("Insufficient funds in source account.")

            # Perform the transfer
            src["balance"] -= amount
            dst["balance"] += amount

    return (
        f"Transfer of ${amount:,.2f} from {from_account} to "
        f"{to_account} completed successfully."
    )