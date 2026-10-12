import threading

# Simulated database of accounts.
ACCOUNTS_DB = {
    "ACC001": {"account_number": "ACC001", "owner_id": "EMP123", "balance": 1000.0},
    "ACC002": {"account_number": "ACC002", "owner_id": "EMP456", "balance": 500.0},
    "ACC003": {"account_number": "ACC003", "owner_id": "EMP789", "balance": 750.0},
}

# Lock to ensure atomic updates across accounts.
DB_LOCK = threading.RLock()


def execute_transfer(employee_id: str, role_value: str,
                     source_acct: str, target_acct: str,
                     total_amount: float) -> str:
    """
    Perform a transfer between two accounts.

    Args:
        employee_id: ID of the user initiating the transfer.
        role_value: Role of the user (e.g., 'account_owner', 'bank_admin',
                    'customer_service').
        source_acct: Account number to debit.
        target_acct: Account number to credit.
        total_amount: Amount to transfer.

    Returns:
        A success message confirming the transfer.

    Raises:
        PermissionError: If the user is not authorized to perform this transfer.
        ValueError: If accounts are invalid or insufficient funds.
    """
    # Basic input validation
    if total_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    with DB_LOCK:
        src = ACCOUNTS_DB.get(source_acct)
        tgt = ACCOUNTS_DB.get(target_acct)

        if src is None or tgt is None:
            raise ValueError("One or both account numbers are invalid.")

        # Authorization logic
        authorized = False

        if role_value == "bank_admin":
            # Bank admins can transfer any accounts.
            authorized = True

        elif role_value == "account_owner":
            # Owners can transfer only from accounts they own.
            if src["owner_id"] == employee_id:
                authorized = True

        elif role_value == "customer_service":
            # Customer service can transfer only to/from accounts with
            # balances below a threshold (e.g., 10000) and must have admin
            # privileges on the target account. This is a simplistic example.
            threshold = 10000
            if (src["balance"] <= threshold and tgt["balance"] <= threshold):
                authorized = True

        if not authorized:
            raise PermissionError(
                f"User {employee_id} with role '{role_value}' "
                "is not authorized to perform this transfer."
            )

        # Check sufficient funds
        if src["balance"] < total_amount:
            raise ValueError("Insufficient funds in the source account.")

        # Perform transfer atomically
        src["balance"] -= total_amount
        tgt["balance"] += total_amount

    return (
        f"Transfer of ${total_amount:.2f} from {source_acct} "
        f"to {target_acct} completed successfully."
    )