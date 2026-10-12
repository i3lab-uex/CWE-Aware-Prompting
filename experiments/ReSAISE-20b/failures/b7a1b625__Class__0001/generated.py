import datetime
from typing import Dict

# Sample in‑memory database of accounts
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC123": {"account_number": "ACC123", "owner_id": "user1", "balance": 5000.00},
    "ACC456": {"account_number": "ACC456", "owner_id": "user2", "balance": 3000.00},
    "ACC789": {"account_number": "ACC789", "owner_id": "user3", "balance": 10000.00},
}

# Roles that have special privileges
ADMIN_ROLES = {"bank_admin"}
OWNER_ROLES = {"account_owner"}

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
    Raises ValueError for invalid accounts or insufficient funds.
    """
    # Basic input validation
    if total_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Fetch accounts
    src = ACCOUNTS_DB.get(source_acct)
    tgt = ACCOUNTS_DB.get(target_acct)

    if src is None or tgt is None:
        raise ValueError("One or both account numbers are invalid.")

    # Authorization logic (CWE‑863 safe check)
    authorized = False
    if role_value in ADMIN_ROLES:
        # Admins can transfer from any account
        authorized = True
    elif role_value in OWNER_ROLES:
        # Account owners can only transfer from their own account
        authorized = src["owner_id"] == employee_id

    if not authorized:
        raise PermissionError("Unauthorized transfer attempt.")

    # Check sufficient funds
    if src["balance"] < total_amount:
        raise ValueError("Insufficient balance in source account.")

    # Perform transfer atomically
    src["balance"] -= total_amount
    tgt["balance"] += total_amount

    # Log the transfer (simplified example)
    log_entry = (
        f"{datetime.datetime.utcnow().isoformat()} - "
        f"Employee {employee_id} ({role_value}) transferred ${total_amount:.2f} "
        f"from {source_acct} to {target_acct}"
    )
    # In a real system, write log_entry to secure audit trail
    print(log_entry)

    return (
        f"Transfer of ${total_amount:.2f} from {source_acct} to "
        f"{target_acct} completed successfully."
    )