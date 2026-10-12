import threading

# Example accounts database; in a real system this would be persisted securely.
ACCOUNTS_DB = {
    "ACC123": {"account_number": "ACC123", "owner_id": "user1", "balance": 1000.0},
    "ACC456": {"account_number": "ACC456", "owner_id": "user2", "balance": 500.0},
    # add more accounts as needed
}

# A lock to protect concurrent modifications of account balances.
_db_lock = threading.Lock()


def execute_transfer(identifier: str, role: str,
                     source_acc: str, destination_acc: str,
                     value: float) -> str:
    """
    Transfer money from source_acc to destination_acc if the caller is authorized.

    Args:
        identifier (str): ID of the user requesting the transfer.
        role (str): Role of the requester ('account_owner', 'bank_admin',
                    'customer_service', etc.).
        source_acc (str): Account number to debit.
        destination_acc (str): Account number to credit.
        value (float): Amount to transfer.

    Returns:
        str: Success message indicating the completed transfer.

    Raises:
        PermissionError: If the user is not authorized to perform this transfer.
        ValueError: If accounts are missing, insufficient funds, or invalid amount.
    """
    # Basic validation
    if value <= 0:
        raise ValueError("Transfer amount must be positive.")
    if source_acc == destination_acc:
        raise ValueError("Source and destination accounts must differ.")

    # Retrieve account records
    src = ACCOUNTS_DB.get(source_acc)
    dst = ACCOUNTS_DB.get(destination_acc)

    if src is None or dst is None:
        raise ValueError("One or both accounts do not exist.")

    # Authorization logic
    if role == "bank_admin":
        authorized = True
    elif role == "account_owner" and src["owner_id"] == identifier:
        authorized = True
    else:
        authorized = False

    if not authorized:
        raise PermissionError("User is not authorized to perform this transfer.")

    # Perform the transfer atomically
    with _db_lock:
        if src["balance"] < value:
            raise ValueError("Insufficient funds in source account.")
        src["balance"] -= value
        dst["balance"] += value

    return (f"Transfer of ${value:,.2f} from {source_acc} "
            f"to {destination_acc} completed successfully.")


# Example usage (uncomment to test)
# try:
#     msg = execute_transfer("user1", "account_owner", "ACC123", "ACC456", 200.0)
#     print(msg)
# except Exception as e:
#     print(f"Error: {e}")