import datetime

# Example in‑memory accounts database
ACCOUNTS_DB = {
    "ACC123": {"account_number": "ACC123", "owner_id": "user1", "balance": 1000.0},
    "ACC456": {"account_number": "ACC456", "owner_id": "user2", "balance": 500.0},
    # Add more accounts as needed
}

def execute_transfer(identifier: str, role: str,
                     source_acc: str, destination_acc: str,
                     value: float) -> str:
    """
    Transfer funds between accounts with role‑based authorization.

    Parameters
    ----------
    identifier : str
        The ID of the individual requesting the transfer.
    role : str
        Role of the requester ('account_owner', 'bank_admin',
        'customer_service').
    source_acc : str
        Account number to debit.
    destination_acc : str
        Account number to credit.
    value : float
        Amount to transfer.

    Returns
    -------
    str
        Success message if the transfer completes.

    Raises
    ------
    PermissionError
        If the requester is not authorized to perform the transfer.
    KeyError
        If either account does not exist.
    ValueError
        If the transfer amount is invalid or insufficient funds.
    """
    # Validate accounts exist
    if source_acc not in ACCOUNTS_DB:
        raise KeyError(f"Source account {source_acc} does not exist.")
    if destination_acc not in ACCOUNTS_DB:
        raise KeyError(f"Destination account {destination_acc} does not exist.")

    src = ACCOUNTS_DB[source_acc]
    dst = ACCOUNTS_DB[destination_acc]

    # Authorization checks
    if role == "account_owner":
        if src["owner_id"] != identifier:
            raise PermissionError("Account owner can only transfer from their own account.")
    elif role in ("bank_admin", "customer_service"):
        # These roles are granted blanket permission
        pass
    else:
        raise PermissionError(f"Role '{role}' is not authorized to perform transfers.")

    # Validate transfer amount
    if value <= 0:
        raise ValueError("Transfer amount must be positive.")
    if src["balance"] < value:
        raise ValueError("Insufficient funds in source account.")

    # Perform the transfer atomically (simple simulation)
    src["balance"] -= value
    dst["balance"] += value

    # Log the transaction (simplified)
    timestamp = datetime.datetime.utcnow().isoformat()
    print(f"[{timestamp}] Transfer of {value:.2f} from {source_acc} to {destination_acc}"
          f" by {identifier} ({role})")

    return f"Transfer of {value:.2f} from {source_acc} to {destination_acc} completed successfully."

# Example usage (uncomment to test):
# print(execute_transfer("user1", "account_owner", "ACC123", "ACC456", 200.0))