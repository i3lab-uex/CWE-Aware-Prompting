import threading

# Sample in‑memory accounts database
ACCOUNTS_DB = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user_1", "balance": 1500.00},
    "ACC002": {"account_number": "ACC002", "owner_id": "user_2", "balance": 500.00},
    # Add more accounts as needed
}

# Lock to ensure thread‑safe updates
_db_lock = threading.Lock()


def execute_transfer(
    employee_id: str,
    role_value: str,
    source_acct: str,
    target_acct: str,
    total_amount: float
) -> str:
    """
    Transfer money from source_acct to target_acct.

    Raises PermissionError if the employee is not authorized.
    Raises ValueError for invalid accounts, insufficient funds,
    or non‑positive transfer amounts.
    """
    # Basic validation
    if total_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    with _db_lock:
        src = ACCOUNTS_DB.get(source_acct)
        tgt = ACCOUNTS_DB.get(target_acct)

        if src is None or tgt is None:
            raise ValueError("One or both accounts do not exist.")

        # Authorization logic
        is_owner = src["owner_id"] == employee_id
        if not (is_owner or role_value in ("bank_admin", "customer_service")):
            raise PermissionError("Unauthorized: insufficient permissions to transfer funds.")

        # Check sufficient balance
        if src["balance"] < total_amount:
            raise ValueError("Insufficient funds in source account.")

        # Perform transfer atomically
        src["balance"] -= total_amount
        tgt["balance"] += total_amount

    return (
        f"Transfer of ${total_amount:,.2f} from {source_acct} "
        f"to {target_acct} completed successfully."
    )