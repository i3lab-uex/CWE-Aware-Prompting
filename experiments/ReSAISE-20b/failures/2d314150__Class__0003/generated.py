import datetime

# Mock database of accounts
ACCOUNTS_DB = {
    "ACC123": {"account_number": "ACC123", "owner_id": "U001", "balance": 1000.00},
    "ACC456": {"account_number": "ACC456", "owner_id": "U002", "balance": 500.00},
    "ACC789": {"account_number": "ACC789", "owner_id": "U001", "balance": 750.00},
}


def transfer_funds(user_id: str,
                   user_role: str,
                   from_account: str,
                   to_account: str,
                   amount: float) -> str:
    """
    Transfer funds between two accounts with proper authorization checks.

    Args:
        user_id (str): ID of the user attempting the transfer.
        user_role (str): Role of the user ('account_owner', 'bank_admin',
                         or 'customer_service').
        from_account (str): Account number to debit.
        to_account (str): Account number to credit.
        amount (float): Amount to transfer.

    Returns:
        str: Confirmation message upon successful transfer.

    Raises:
        ValueError: If accounts do not exist, insufficient funds,
                    or invalid transfer amount.
    """

    # Basic validation
    if amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Retrieve accounts
    src = ACCOUNTS_DB.get(from_account)
    dst = ACCOUNTS_DB.get(to_account)

    if not src or not dst:
        raise ValueError("One or both accounts do not exist.")

    # Authorization logic
    authorized = False

    if user_role == "bank_admin":
        # Bank admins can transfer between any accounts
        authorized = True

    elif user_role == "customer_service":
        # Customer service can transfer only between accounts owned by the same user
        if src["owner_id"] == dst["owner_id"]:
            authorized = True

    elif user_role == "account_owner":
        # Account owner can transfer only from their own account
        if src["owner_id"] == user_id:
            authorized = True

    # Prevent CWE-863: ensure check is performed before any state changes
    if not authorized:
        return "Authorization error: insufficient permissions to transfer funds."

    # Check sufficient funds
    if src["balance"] < amount:
        raise ValueError("Insufficient funds in the source account.")

    # Perform transfer
    src["balance"] -= amount
    dst["balance"] += amount

    # Optional: log the transaction (not implemented here)
    timestamp = datetime.datetime.utcnow().isoformat()
    return (
        f"Transfer successful: {amount:.2f} transferred from "
        f"{from_account} to {to_account} on {timestamp}."
    )