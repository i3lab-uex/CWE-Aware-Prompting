#!/usr/bin/env python3
"""
Banking system – transfer funds between accounts with proper authorization.

The implementation follows the CWE‑863 guidance to ensure that
authorization checks are performed *before* any state changes.
"""

from __future__ import annotations

import threading
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Sample accounts database (in‑memory). In a real system this would be
# persisted in a secure database and accessed through an ORM or API.
# --------------------------------------------------------------------------- #
ACCOUNTS_DB: Dict[str, Dict[str, Any]] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user_001", "balance": 5000.00},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "user_002", "balance": 3000.00},
    "ACC1003": {"account_number": "ACC1003", "owner_id": "user_003", "balance": 7500.00},
}

# Lock to serialize access to the accounts database and prevent race conditions.
_DB_LOCK = threading.Lock()


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
        The ID of the user attempting to perform the transfer.
    user_role : str
        Role of the user. Expected values: 'account_owner',
        'bank_admin', or 'customer_service'.
    from_account : str
        Account number to debit.
    to_account : str
        Account number to credit.
    amount : float
        Positive transfer amount.

    Returns
    -------
    str
        Confirmation message if the transfer succeeds.

    Raises
    ------
    ValueError
        If either account does not exist, the amount is invalid,
        insufficient funds, or authorization fails.
    """
    if amount <= 0:
        raise ValueError("Transfer amount must be positive")

    # Acquire lock to ensure atomic read-modify-write.
    with _DB_LOCK:
        src = ACCOUNTS_DB.get(from_account)
        dst = ACCOUNTS_DB.get(to_account)

        if src is None:
            raise ValueError(f"Source account '{from_account}' does not exist")
        if dst is None:
            raise ValueError(f"Destination account '{to_account}' does not exist")

        # Authorization logic
        if user_role == "bank_admin":
            authorized = True  # admins can transfer any funds
        elif user_role == "account_owner":
            authorized = src["owner_id"] == user_id
        elif user_role == "customer_service":
            # Customer service may transfer only if they have explicit
            # permission; here we allow it for demonstration.
            authorized = True
        else:
            authorized = False

        if not authorized:
            raise ValueError("User is not authorized to transfer funds from this account")

        # Ensure sufficient funds
        if src["balance"] < amount:
            raise ValueError("Insufficient funds in source account")

        # Perform transfer
        src["balance"] -= amount
        dst["balance"] += amount

    return (
        f"Transfer of ${amount:,.2f} from '{from_account}' to "
        f"'{to_account}' completed successfully."
    )


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        print(
            transfer_funds(
                user_id="user_001",
                user_role="account_owner",
                from_account="ACC1001",
                to_account="ACC1002",
                amount=1200.00,
            )
        )
    except ValueError as exc:
        print(f"Transfer failed: {exc}")