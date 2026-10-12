import datetime
from typing import Dict

# Sample database of accounts
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "USR001", "balance": 1500.00},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "USR002", "balance": 3000.00},
    # add more accounts as needed
}

# Roles that are allowed to perform transfers
ALLOWED_ROLES = {"account_owner", "bank_admin"}


def _log_transaction(source: str, destination: str, amount: float) -> None:
    """
    Internal helper to log the transaction. In a real system this would write
    to a persistent audit trail.
    """
    timestamp = datetime.datetime.utcnow().isoformat()
    print(f"[{timestamp}] TRANSFER: {amount:.2f} from {source} to {destination}")


def execute_transfer(
    identifier: str,
    role: str,
    source_acc: str,
    destination_acc: str,
    value: float,
) -> str:
    """
    Transfer money from source account to destination account.

    Parameters
    ----------
    identifier : str
        The user ID requesting the transfer.
    role : str
        Role of the requester. Must be 'account_owner' or 'bank_admin'.
    source_acc : str
        Account number to debit.
    destination_acc : str
        Account number to credit.
    value : float
        Amount to transfer.

    Returns
    -------
    str
        Success message on successful transfer.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    ValueError
        For invalid accounts, insufficient funds or negative amounts.
    """
    # Basic validation
    if value <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Check accounts exist
    src = ACCOUNTS_DB.get(source_acc)
    dst = ACCOUNTS_DB.get(destination_acc)

    if src is None or dst is None:
        raise ValueError("Source or destination account does not exist.")

    # Authorization check – CWE‑863 prevention
    authorized = False
    if role == "bank_admin":
        authorized = True  # Admin can transfer any account
    elif role == "account_owner" and src["owner_id"] == identifier:
        authorized = True  # Owner can transfer from their own account

    if not authorized:
        raise PermissionError("Unauthorized transfer attempt.")

    # Ensure sufficient funds
    if src["balance"] < value:
        raise ValueError("Insufficient balance in source account.")

    # Perform the transfer atomically
    src["balance"] -= value
    dst["balance"] += value

    # Log the transaction (in real system, write to audit log)
    _log_transaction(source_acc, destination_acc, value)

    return (
        f"Transfer of {value:.2f} from {source_acc} to "
        f"{destination_acc} completed successfully."
    )


# Example usage (uncomment for testing)
# try:
#     msg = execute_transfer("USR001", "account_owner", "ACC1001", "ACC1002", 200.0)
#     print(msg)
# except Exception as e:
#     print(f"Error: {e}")