# transfer_funds.py

from __future__ import annotations
import threading
from typing import Dict

# Example in‑memory database of accounts.
# In a real system this would be replaced with persistent storage.
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user123", "balance": 1500.00},
    "ACC2002": {"account_number": "ACC2002", "owner_id": "user456", "balance": 3000.00},
    "ACC3003": {"account_number": "ACC3003", "owner_id": "user123", "balance": 500.00},
}

# A lock per account to prevent race conditions during concurrent transfers.
ACCOUNT_LOCKS: Dict[str, threading.Lock] = {acc: threading.Lock() for acc in ACCOUNTS_DB}


def transfer_funds(
    user_id: str,
    user_role: str,
    from_account: str,
    to_account: str,
    amount: float
) -> str:
    """
    Transfer funds between two accounts after performing authorization checks.

    Parameters
    ----------
    user_id : str
        The ID of the user attempting the transfer.
    user_role : str
        Role of the user: 'account_owner', 'bank_admin', or 'customer_service'.
    from_account : str
        Account number to transfer funds from.
    to_account : str
        Account number to transfer funds to.
    amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Confirmation message if the transfer is successful.

    Raises
    ------
    ValueError
        If either account does not exist, if the amount is non‑positive,
        or if insufficient funds are available.
    PermissionError
        If the user is not authorized to perform the transfer.
    """
    if amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Validate existence of both accounts
    from_acc = ACCOUNTS_DB.get(from_account)
    to_acc   = ACCOUNTS_DB.get(to_account)

    if from_acc is None or to_acc is None:
        raise ValueError("One or both accounts do not exist.")

    # Authorization logic
    if user_role == "bank_admin":
        authorized = True  # Admin can transfer any accounts
    elif user_role == "account_owner":
        authorized = from_acc["owner_id"] == user_id
    elif user_role == "customer_service":
        # Customer service can transfer only between accounts owned by the same user
        authorized = (
            from_acc["owner_id"] == to_acc["owner_id"]
            and from_acc["owner_id"] == user_id
        )
    else:
        authorized = False

    if not authorized:
        raise PermissionError("User is not authorized to perform this transfer.")

    # Use a consistent lock order to avoid deadlocks
    first_lock, second_lock = (
        (ACCOUNT_LOCKS[from_account], ACCOUNT_LOCKS[to_account])
        if from_account < to_account
        else (ACCOUNT_LOCKS[to_account], ACCOUNT_LOCKS[from_account])
    )

    with first_lock:
        with second_lock:
            # Re‑check balance after acquiring locks
            if from_acc["balance"] < amount:
                raise ValueError("Insufficient funds in the source account.")

            # Perform transfer
            from_acc["balance"] -= amount
            to_acc["balance"]   += amount

    return (
        f"Transferred ${amount:,.2f} from {from_account} to "
        f"{to_account}. New balance of {from_account}: ${from_acc['balance']:,.2f}."
    )


# Example usage (uncomment to test):
# try:
#     msg = transfer_funds("user123", "account_owner", "ACC1001", "ACC3003", 200)
#     print(msg)
# except Exception as e:
#     print(f"Error: {e}")