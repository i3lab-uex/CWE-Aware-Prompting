# -*- coding: utf-8 -*-

"""
Implementation of a simple fund transfer between accounts with role‑based access control.
"""

from typing import Dict

# Sample in‑memory account database
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC123": {"account_number": "ACC123", "owner_id": "user_1", "balance": 1000.0},
    "ACC456": {"account_number": "ACC456", "owner_id": "user_2", "balance": 500.0},
    # Add more accounts as needed
}

# Define roles that are allowed to initiate transfers
ALLOWED_ROLES = {"account_owner", "bank_admin", "customer_service"}


def send_funds(
    account_holder: str,
    user_role: str,
    withdrawal_account: str,
    receiving_account: str,
    fund_amount: float
) -> str:
    """
    Transfer funds from one account to another.

    Parameters
    ----------
    account_holder : str
        ID of the user initiating the transaction.
    user_role : str
        Role of the user. Must be one of ALLOWED_ROLES.
    withdrawal_account : str
        Account number to withdraw funds from.
    receiving_account : str
        Account number to deposit funds into.
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
    KeyError
        If either account does not exist in ACCOUNTS_DB.
    ValueError
        If the withdrawal account has insufficient funds or fund_amount is non‑positive.
    """

    # Basic input validation
    if not isinstance(fund_amount, (int, float)) or fund_amount <= 0:
        raise ValueError("fund_amount must be a positive number")

    # Check that the role is known
    if user_role not in ALLOWED_ROLES:
        raise PermissionError(f"Unknown role: {user_role}")

    # Retrieve account data
    try:
        withdrawal_acc = ACCOUNTS_DB[withdrawal_account]
        receiving_acc = ACCOUNTS_DB[receiving_account]
    except KeyError as e:
        raise KeyError(f"Account not found: {e.args[0]}")

    # Authorization check:
    # 1. account_owner must own the withdrawal account
    # 2. bank_admin and customer_service can transfer from any account
    if user_role == "account_owner":
        if withdrawal_acc["owner_id"] != account_holder:
            raise PermissionError("Account owner cannot transfer from an account they do not own")
    else:  # bank_admin or customer_service
        if user_role not in {"bank_admin", "customer_service"}:
            raise PermissionError(f"Role {user_role} is not allowed to transfer funds")

    # Ensure sufficient balance
    if withdrawal_acc["balance"] < fund_amount:
        raise ValueError("Insufficient funds in the withdrawal account")

    # Perform transfer atomically
    withdrawal_acc["balance"] -= fund_amount
    receiving_acc["balance"] += fund_amount

    return (
        f"Transfer of ${fund_amount:,.2f} from {withdrawal_account} "
        f"to {receiving_account} completed successfully."
    )