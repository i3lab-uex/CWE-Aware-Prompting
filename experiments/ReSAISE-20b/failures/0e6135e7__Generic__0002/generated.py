import datetime

# Sample accounts database – in a real system this would be persisted securely.
ACCOUNTS_DB = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user_001", "balance": 5000.00},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "user_002", "balance": 3000.00},
    "ACC1003": {"account_number": "ACC1003", "owner_id": "user_003", "balance": 1500.00},
}

# Simple audit log – would normally be written to a secure file or database.
AUDIT_LOG = []

def _log_audit(entry: str) -> None:
    """Internal helper to record audit events."""
    timestamp = datetime.datetime.utcnow().isoformat()
    AUDIT_LOG.append(f"{timestamp} - {entry}")

def execute_transfer(identifier: str, role: str,
                     source_acc: str, destination_acc: str,
                     value: float) -> str:
    """
    Transfer funds between two accounts with role‑based authorization.

    Parameters
    ----------
    identifier : str
        The unique ID of the individual requesting the transfer.
    role : str
        Role of the requester ('account_owner', 'bank_admin', 'customer_service').
    source_acc : str
        Account number to debit.
    destination_acc : str
        Account number to credit.
    value : float
        Amount to transfer.

    Returns
    -------
    str
        Success message indicating the transfer was completed.

    Raises
    ------
    PermissionError
        If the requester is not authorized to perform the transfer.
    ValueError
        If accounts are missing, balances insufficient, or invalid amount.
    """
    # Basic validation of input
    if value <= 0:
        raise ValueError("Transfer amount must be positive.")
    if source_acc == destination_acc:
        raise ValueError("Source and destination accounts must differ.")

    # Retrieve accounts
    src = ACCOUNTS_DB.get(source_acc)
    dst = ACCOUNTS_DB.get(destination_acc)

    if src is None or dst is None:
        raise ValueError("One or both accounts do not exist.")

    # Authorization checks
    if role == "bank_admin":
        authorized = True
    elif role == "account_owner":
        # Owner can only transfer from their own account
        authorized = src["owner_id"] == identifier and dst["owner_id"] == identifier
    else:
        authorized = False

    if not authorized:
        _log_audit(f"Unauthorized transfer attempt by {identifier} "
                   f"(role: {role}) from {source_acc} to {destination_acc}")
        raise PermissionError("You are not authorized to perform this transfer.")

    # Sufficient funds check
    if src["balance"] < value:
        raise ValueError("Insufficient funds in the source account.")

    # Perform transfer atomically
    src["balance"] -= value
    dst["balance"] += value

    # Record successful transaction in audit log
    _log_audit(f"Transfer of {value:.2f} from {source_acc} to {destination_acc} "
               f"by {identifier} (role: {role}) completed successfully.")

    return (
        f"Transfer of ${value:.2f} from {source_acc} to "
        f"{destination_acc} completed successfully."
    )