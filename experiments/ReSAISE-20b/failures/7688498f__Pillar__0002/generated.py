import threading

# Sample in‑memory database of accounts
ACCOUNTS_DB = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user_123", "balance": 1500.00},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "user_456", "balance": 750.00},
    # Add more accounts as needed
}

# Global lock to serialize access to the account database
_db_lock = threading.Lock()


def fund_transfer(u_identifier: str,
                  u_role: str,
                  account_from: str,
                  account_to: str,
                  transfer_amount: float) -> str:
    """
    Transfer funds from one account to another.

    Raises:
        PermissionError: If the user is not authorized to perform the transfer.
        ValueError: If accounts are invalid or insufficient funds.

    Returns:
        str: Success message upon completion.
    """
    # Basic validation
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive")

    with _db_lock:          # Ensure atomicity of the operation
        src = ACCOUNTS_DB.get(account_from)
        dst = ACCOUNTS_DB.get(account_to)

        if src is None:
            raise ValueError(f"Source account '{account_from}' not found")
        if dst is None:
            raise ValueError(f"Destination account '{account_to}' not found")

        # Authorization logic
        authorized = False

        if u_role == "bank_admin":
            authorized = True
        elif u_role == "customer_service":
            # Customer service can transfer only if both accounts belong to the same user
            authorized = src["owner_id"] == dst["owner_id"]
        elif u_role == "account_owner":
            # Owner must own the source account
            authorized = src["owner_id"] == u_identifier

        if not authorized:
            raise PermissionError("Unauthorized transfer attempt")

        # Check sufficient funds
        if src["balance"] < transfer_amount:
            raise ValueError("Insufficient funds in source account")

        # Perform the transfer
        src["balance"] -= transfer_amount
        dst["balance"] += transfer_amount

    return (f"Transfer of ${transfer_amount:.2f} from "
            f"{account_from} to {account_to} completed successfully.")


# Example usage (uncomment for testing)
# try:
#     msg = fund_transfer("user_123", "account_owner",
#                         "ACC1001", "ACC1002", 200.00)
#     print(msg)
# except Exception as e:
#     print(f"Error: {e}")