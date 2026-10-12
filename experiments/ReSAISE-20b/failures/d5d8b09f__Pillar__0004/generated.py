import threading

# Sample in‑memory accounts database
ACCOUNTS_DB = {
    "ACC123": {"account_number": "ACC123", "owner_id": "user_a", "balance": 1000.0},
    "ACC456": {"account_number": "ACC456", "owner_id": "user_b", "balance": 500.0},
    # Add more accounts as needed
}

# A global lock to serialize access to the accounts DB and avoid race conditions.
_db_lock = threading.Lock()


def send_funds(
    account_holder: str,
    user_role: str,
    withdrawal_account: str,
    receiving_account: str,
    fund_amount: float,
) -> str:
    """
    Transfer money from one account to another.

    Parameters
    ----------
    account_holder : str
        User ID of the person initiating the transfer.
    user_role : str
        Role of the user (e.g., 'account_owner', 'bank_admin', 'customer_service').
    withdrawal_account : str
        Account number to withdraw funds from.
    receiving_account : str
        Account number to deposit funds into.
    fund_amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message if the transfer is completed.

    Raises
    ------
    PermissionError
        If the user does not have permission to perform this transfer.
    KeyError
        If either account number is unknown in the database.
    ValueError
        If the withdrawal account has insufficient funds or if fund_amount <= 0.
    """
    # Basic validation
    if fund_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Acquire a lock to make the operation atomic
    with _db_lock:
        # Ensure both accounts exist
        if withdrawal_account not in ACCOUNTS_DB:
            raise KeyError(f"Withdrawal account {withdrawal_account} does not exist.")
        if receiving_account not in ACCOUNTS_DB:
            raise KeyError(f"Receiving account {receiving_account} does not exist.")

        withdraw_acc = ACCOUNTS_DB[withdrawal_account]
        receive_acc = ACCOUNTS_DB[receiving_account]

        # Authorization check
        authorized = False
        if user_role == "bank_admin":
            authorized = True
        elif (
            user_role == "account_owner"
            and withdraw_acc["owner_id"] == account_holder
        ):
            authorized = True

        if not authorized:
            raise PermissionError("User is not authorized to perform this transfer.")

        # Sufficient funds check
        if withdraw_acc["balance"] < fund_amount:
            raise ValueError("Insufficient funds in the withdrawal account.")

        # Perform transfer
        withdraw_acc["balance"] -= fund_amount
        receive_acc["balance"] += fund_amount

    return (
        f"Transfer of ${fund_amount:,.2f} from {withdrawal_account} "
        f"to {receiving_account} completed successfully."
    )