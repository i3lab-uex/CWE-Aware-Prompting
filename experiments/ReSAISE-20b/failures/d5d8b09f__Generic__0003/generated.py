# -*- coding: utf-8 -*-
"""
Banking fund transfer module.
"""

from __future__ import annotations
import threading

# Sample in-memory accounts database.
ACCOUNTS_DB = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user_a", "balance": 1500.00},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "user_b", "balance": 2500.00},
    # Add more accounts as needed.
}

# Global lock to prevent race conditions during concurrent transfers.
_DB_LOCK = threading.Lock()


def send_funds(
    account_holder: str,
    user_role: str,
    withdrawal_account: str,
    receiving_account: str,
    fund_amount: float,
) -> str:
    """
    Transfer funds from one account to another.

    Parameters
    ----------
    account_holder : str
        ID of the user initiating the transfer.
    user_role : str
        Role of the user. Accepted values are:
            - 'account_owner'
            - 'bank_admin'
    withdrawal_account : str
        Account number to withdraw from.
    receiving_account : str
        Account number to deposit into.
    fund_amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message confirming the transfer.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    ValueError
        For invalid accounts, negative amounts or insufficient funds.
    """
    if fund_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Verify accounts exist
    with _DB_LOCK:
        from_acc = ACCOUNTS_DB.get(withdrawal_account)
        to_acc = ACCOUNTS_DB.get(receiving_account)

    if not from_acc:
        raise ValueError(f"Withdrawal account '{withdrawal_account}' does not exist.")
    if not to_acc:
        raise ValueError(f"Receiving account '{receiving_account}' does not exist.")

    # Authorization logic
    authorized = False
    if user_role == "bank_admin":
        authorized = True
    elif user_role == "account_owner" and from_acc["owner_id"] == account_holder:
        authorized = True

    if not authorized:
        raise PermissionError("User is not authorized to perform this transfer.")

    # Perform the transfer atomically
    with _DB_LOCK:
        if from_acc["balance"] < fund_amount:
            raise ValueError("Insufficient funds in the withdrawal account.")

        # Update balances
        from_acc["balance"] -= fund_amount
        to_acc["balance"] += fund_amount

    return (
        f"Transfer of ${fund_amount:,.2f} from {withdrawal_account} "
        f"to {receiving_account} completed successfully."
    )