# transfer_funds.py

"""
Banking system: transfer funds between accounts with proper authorization.
"""

from __future__ import annotations
import threading

# Sample in-memory database of accounts.
# In a real system this would be replaced with persistent storage and proper concurrency control.
ACCOUNTS_DB = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "U001", "balance": 5000.0},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "U002", "balance": 3000.0},
    "ACC1003": {"account_number": "ACC1003", "owner_id": "U003", "balance": 7500.0},
}

# Lock for thread‑safe operations on ACCOUNTS_DB
_db_lock = threading.RLock()


def transfer_funds(
    user_id: str,
    user_role: str,
    from_account: str,
    to_account: str,
    amount: float,
) -> str:
    """
    Transfer money from one account to another with authorization checks.

    Parameters
    ----------
    user_id : str
        ID of the user performing the transfer.
    user_role : str
        Role of the user. Accepted values are:
            * 'account_owner'  – can transfer only from accounts they own.
            * 'bank_admin'     – full access to all accounts.
            * 'customer_service'
                – can transfer only between accounts that belong to the same user.
    from_account : str
        Source account number.
    to_account : str
        Destination account number.
    amount : float
        Amount of money to transfer. Must be > 0.

    Returns
    -------
    str
        Confirmation message if the transfer succeeded.

    Raises
    ------
    ValueError
        If either account does not exist, if the amount is invalid,
        or if there are insufficient funds.
    PermissionError
        If the user does not have permission to perform the transfer.
    """

    if amount <= 0:
        raise ValueError("Transfer amount must be greater than zero.")

    # Acquire lock to ensure atomic read‑modify‑write
    with _db_lock:
        src = ACCOUNTS_DB.get(from_account)
        dst = ACCOUNTS_DB.get(to_account)

        if src is None or dst is None:
            raise ValueError("One or both accounts do not exist.")

        # Authorization logic
        if user_role == "bank_admin":
            # Admin can transfer between any accounts
            authorized = True
        elif user_role == "account_owner":
            # Must own the source account
            authorized = src["owner_id"] == user_id
        elif user_role == "customer_service":
            # Can transfer only between accounts that belong to the same owner
            authorized = src["owner_id"] == dst["owner_id"]
        else:
            # Unknown role – deny access
            authorized = False

        if not authorized:
            raise PermissionError("User is not authorized to perform this transfer.")

        # Check sufficient funds
        if src["balance"] < amount:
            raise ValueError("Insufficient funds in source account.")

        # Perform the transfer
        src["balance"] -= amount
        dst["balance"] += amount

    return (
        f"Transfer of ${amount:,.2f} from {from_account} to {to_account} "
        f"completed successfully."
    )


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         msg = transfer_funds(
#             user_id="U001",
#             user_role="account_owner",
#             from_account="ACC1001",
#             to_account="ACC1002",
#             amount=1500.0,
#         )
#         print(msg)
#     except Exception as e:
#         print(f"Error: {e}")