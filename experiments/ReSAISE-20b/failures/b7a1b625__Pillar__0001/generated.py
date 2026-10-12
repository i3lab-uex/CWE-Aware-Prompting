import datetime
from typing import Dict

# Example in‑memory database of accounts.
ACCOUNTS_DB: Dict[str, dict] = {
    "ACC123": {"account_number": "ACC123", "owner_id": "EMP001", "balance": 1500.00},
    "ACC456": {"account_number": "ACC456", "owner_id": "EMP002", "balance": 2000.00},
    # Add more accounts as needed.
}

def execute_transfer(
    employee_id: str,
    role_value: str,
    source_acct: str,
    target_acct: str,
    total_amount: float
) -> str:
    """
    Transfer funds between two accounts after verifying authorization.

    Args:
        employee_id: ID of the user initiating the transfer.
        role_value: Role of the user ('account_owner', 'bank_admin', 'customer_service').
        source_acct: Account number to debit.
        target_acct: Account number to credit.
        total_amount: Amount to transfer.

    Returns:
        Success message if the transfer is authorized and completed.

    Raises:
        PermissionError: If the user is not authorized to perform this transfer.
        ValueError: If accounts are missing or insufficient funds.
    """
    # Basic validation of input
    if total_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Retrieve accounts
    src = ACCOUNTS_DB.get(source_acct)
    tgt = ACCOUNTS_DB.get(target_acct)

    if not src or not tgt:
        raise ValueError("Source or target account does not exist.")

    # Authorization logic
    authorized = False

    if role_value == "bank_admin":
        # Admins can transfer between any accounts
        authorized = True

    elif role_value == "account_owner":
        # Owner can only transfer from their own account
        if employee_id == src["owner_id"]:
            authorized = True

    elif role_value == "customer_service":
        # Customer service may transfer only if they are the owner of the source account
        # (custom policy – adjust as needed)
        if employee_id == src["owner_id"]:
            authorized = True

    # If not authorized, raise an exception
    if not authorized:
        raise PermissionError("Unauthorized access: insufficient permissions to transfer funds.")

    # Ensure sufficient balance
    if src["balance"] < total_amount:
        raise ValueError("Insufficient funds in source account.")

    # Perform the transfer
    src["balance"] -= total_amount
    tgt["balance"] += total_amount

    # Optional: record the transaction (omitted for brevity)

    return (
        f"Transfer of ${total_amount:,.2f} from {source_acct} to "
        f"{target_acct} completed successfully on {datetime.datetime.utcnow():%Y-%m-%d %H:%M:%S} UTC."
    )