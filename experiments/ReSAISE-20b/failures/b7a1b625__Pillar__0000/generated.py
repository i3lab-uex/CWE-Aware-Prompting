import threading

# Mock database of accounts
ACCOUNTS_DB = {
    "1001": {"account_number": "1001", "owner_id": "userA", "balance": 5000.0},
    "1002": {"account_number": "1002", "owner_id": "userB", "balance": 3000.0},
    # Add more accounts as needed
}

# Lock for thread‑safety when updating balances
db_lock = threading.Lock()


def execute_transfer(
    employee_id: str,
    role_value: str,
    source_acct: str,
    target_acct: str,
    total_amount: float,
) -> str:
    """
    Transfer money from source_acct to target_acct.

    Parameters
    ----------
    employee_id : str
        ID of the user initiating the transfer.
    role_value : str
        Role of the user (e.g., 'account_owner', 'bank_admin',
        'customer_service').
    source_acct : str
        Account number to withdraw from.
    target_acct : str
        Account number to deposit into.
    total_amount : float
        Amount to transfer.

    Returns
    -------
    str
        Success message if the transfer is completed.

    Raises
    ------
    PermissionError
        If the user does not have permission to transfer from the source
        account.
    ValueError
        If accounts are missing, amounts invalid, or insufficient funds.
    """

    # Basic validation of input
    if total_amount <= 0:
        raise ValueError("Transfer amount must be positive")

    # Retrieve accounts
    src = ACCOUNTS_DB.get(source_acct)
    tgt = ACCOUNTS_DB.get(target_acct)

    if src is None or tgt is None:
        raise ValueError("One or both accounts do not exist")

    # Authorization logic
    if role_value == "bank_admin":
        authorized = True
    elif role_value == "account_owner" and src["owner_id"] == employee_id:
        authorized = True
    else:
        authorized = False

    if not authorized:
        raise PermissionError(
            f"User '{employee_id}' with role '{role_value}' is not authorized to transfer from account {source_acct}"
        )

    # Perform the transfer atomically
    with db_lock:
        if src["balance"] < total_amount:
            raise ValueError(
                f"Insufficient funds in account {source_acct}. Available: {src['balance']}"
            )
        src["balance"] -= total_amount
        tgt["balance"] += total_amount

    return (
        f"Transfer of {total_amount:.2f} from account {source_acct} "
        f"to account {target_acct} completed successfully."
    )