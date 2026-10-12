# transfer_funds.py

from typing import Dict

# Example in‑memory database of accounts.
# In a real system this would be replaced by persistent storage.
ACCOUNTS_DB: Dict[str, dict] = {
    "ACC001": {"account_number": "ACC001", "owner_id": "U1001", "balance": 1500.00},
    "ACC002": {"account_number": "ACC002", "owner_id": "U1002", "balance": 3000.00},
    "ACC003": {"account_number": "ACC003", "owner_id": "U1003", "balance": 500.00},
}

def transfer_funds(
    user_id: str,
    user_role: str,
    from_account: str,
    to_account: str,
    amount: float
) -> str:
    """
    Transfer funds between two accounts with proper authorization checks.

    Parameters
    ----------
    user_id : str
        ID of the user initiating the transfer.
    user_role : str
        Role of the user: 'account_owner', 'bank_admin', or 'customer_service'.
    from_account : str
        Source account number.
    to_account : str
        Destination account number.
    amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Confirmation message if the transfer succeeds.

    Raises
    ------
    ValueError
        If either account does not exist, the amount is non‑positive,
        or insufficient funds are available.
    PermissionError
        If the user lacks authorization to perform the transfer.
    """
    # Validate amount
    if amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Retrieve accounts
    src = ACCOUNTS_DB.get(from_account)
    dst = ACCOUNTS_DB.get(to_account)

    if src is None or dst is None:
        raise ValueError("One or both accounts do not exist.")

    # Authorization logic
    authorized = False

    if user_role == "bank_admin":
        # Admins can transfer between any accounts
        authorized = True

    elif user_role == "account_owner":
        # Owners can transfer only from their own accounts
        if src["owner_id"] == user_id:
            authorized = True

    elif user_role == "customer_service":
        # Customer service is not permitted to transfer funds
        authorized = False

    else:
        # Unknown role – deny access
        authorized = False

    if not authorized:
        raise PermissionError("User is not authorized to perform this transfer.")

    # Check sufficient funds
    if src["balance"] < amount:
        raise ValueError("Insufficient funds in the source account.")

    # Perform transfer atomically
    src["balance"] -= amount
    dst["balance"] += amount

    return (
        f"Transfer of ${amount:,.2f} from {from_account} to {to_account} "
        f"completed successfully."
    )

# Example usage (uncomment for testing)
# if __name__ == "__main__":
#     try:
#         msg = transfer_funds(
#             user_id="U1001",
#             user_role="account_owner",
#             from_account="ACC001",
#             to_account="ACC002",
#             amount=200.0
#         )
#         print(msg)
#     except Exception as e:
#         print(f"Error: {e}")