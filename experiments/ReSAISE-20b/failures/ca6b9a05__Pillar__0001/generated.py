import threading

# Sample accounts database; in a real system this would be persisted securely.
ACCOUNTS_DB = {
    'ACC1001': {'account_number': 'ACC1001', 'owner_id': 'user123', 'balance': 5000.00},
    'ACC1002': {'account_number': 'ACC1002', 'owner_id': 'user456', 'balance': 3000.00},
    # ... additional accounts ...
}

# A lock to protect concurrent modifications of the accounts database
_DB_LOCK = threading.Lock()

def move_funds(u_id: str,
               u_role: str,
               source_account: str,
               destination_account: str,
               money: float) -> str:
    """
    Transfer funds between two accounts with proper authorization checks.

    Args:
        u_id: Identifier of the individual requesting the transfer.
        u_role: Role of the individual (e.g., 'account_owner', 'bank_admin',
                'customer_service').
        source_account: Account number to debit.
        destination_account: Account number to credit.
        money: Amount to transfer.

    Returns:
        A success message if the transfer is authorized and completed.

    Raises:
        PermissionError: If the user is not authorized to perform this transfer.
        ValueError: If accounts are missing, insufficient funds, or invalid amount.
    """
    if money <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Validate accounts exist
    src = ACCOUNTS_DB.get(source_account)
    dst = ACCOUNTS_DB.get(destination_account)

    if src is None or dst is None:
        raise ValueError("One or both accounts do not exist.")

    # Authorization logic
    authorized = False

    if u_role == 'bank_admin' or u_role == 'customer_service':
        # Admins and customer service have blanket permission
        authorized = True

    elif u_role == 'account_owner':
        # Owner must own the source account
        if src['owner_id'] == u_id:
            authorized = True

    # Add any additional role checks here if necessary

    if not authorized:
        raise PermissionError("User is not authorized to perform this transfer.")

    # Perform the transfer atomically
    with _DB_LOCK:
        if src['balance'] < money:
            raise ValueError("Insufficient funds in the source account.")

        src['balance'] -= money
        dst['balance'] += money

    return f"Transfer of ${money:.2f} from {source_account} to {destination_account} completed successfully."

# Example usage (for testing purposes only; remove in production)
if __name__ == "__main__":
    try:
        print(move_funds('user123', 'account_owner', 'ACC1001', 'ACC1002', 200.0))
    except Exception as e:
        print(f"Error: {e}")