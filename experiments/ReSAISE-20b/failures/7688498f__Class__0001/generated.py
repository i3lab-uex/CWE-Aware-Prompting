import threading

# Example accounts database (in-memory)
ACCOUNTS_DB = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user123", "balance": 5000.0},
    "ACC002": {"account_number": "ACC002", "owner_id": "user456", "balance": 3000.0},
    # Add more accounts as needed
}

# A simple lock to simulate atomic updates for the demo
db_lock = threading.Lock()


def fund_transfer(u_identifier: str,
                  u_role: str,
                  account_from: str,
                  account_to: str,
                  transfer_amount: float) -> str:
    """
    Transfer funds between two accounts after performing authorization checks.

    Args:
        u_identifier: The identifier of the user initiating the transfer.
        u_role: Role of the user (e.g., 'account_owner', 'bank_admin', 'customer_service').
        account_from: Source account number.
        account_to: Destination account number.
        transfer_amount: Amount to transfer.

    Returns:
        Success message on successful transfer.

    Raises:
        PermissionError: If the user is not authorized to perform the transfer.
        ValueError: For invalid input or insufficient funds.
    """
    # Basic validation
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive")

    with db_lock:  # Ensure atomicity for this demo
        src = ACCOUNTS_DB.get(account_from)
        dst = ACCOUNTS_DB.get(account_to)

        if not src or not dst:
            raise ValueError("One or both accounts do not exist")

        # Authorization logic
        authorized = False

        if u_role == "bank_admin":
            authorized = True  # Admin can transfer between any accounts
        elif u_role == "account_owner":
            # Owner must own both source and destination accounts
            if src["owner_id"] == u_identifier and dst["owner_id"] == u_identifier:
                authorized = True
        elif u_role == "customer_service":
            # Customer service may transfer only if owner is explicitly verified
            # For simplicity, we require that the source account belongs to the user
            if src["owner_id"] == u_identifier:
                authorized = True

        if not authorized:
            raise PermissionError("User is not authorized to perform this transfer")

        # Funds check
        if src["balance"] < transfer_amount:
            raise ValueError("Insufficient funds in the source account")

        # Perform the transfer
        src["balance"] -= transfer_amount
        dst["balance"] += transfer_amount

    return f"Transfer of {transfer_amount:.2f} from {account_from} to {account_to} completed successfully."

# Example usage:
if __name__ == "__main__":
    try:
        message = fund_transfer(
            u_identifier="user123",
            u_role="account_owner",
            account_from="ACC001",
            account_to="ACC002",
            transfer_amount=1000.0,
        )
        print(message)
    except Exception as e:
        print(f"Error: {e}")