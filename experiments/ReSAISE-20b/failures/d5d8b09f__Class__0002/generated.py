#!/usr/bin/env python3
"""
Secure fund transfer implementation.
"""

from typing import Dict

# Sample accounts database; in a real system this would be persisted securely.
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user_123", "balance": 5000.0},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "user_456", "balance": 3000.0},
    "ACC1003": {"account_number": "ACC1003", "owner_id": "user_789", "balance": 7500.0},
}


def _get_account(account_number: str) -> Dict:
    """
    Retrieve an account record from the database.
    Raises KeyError if the account does not exist.
    """
    try:
        return ACCOUNTS_DB[account_number]
    except KeyError as exc:
        raise KeyError(f"Account {account_number} not found.") from exc


def _authorize_transfer(
    account_holder: str,
    user_role: str,
    withdrawal_account: str,
) -> None:
    """
    Verify that the user is authorized to initiate a transfer from
    the withdrawal account.
    Raises PermissionError if not authorized.
    """
    # Admins have unrestricted access
    if user_role == "bank_admin":
        return

    # Account owners can transfer only from their own account
    if user_role == "account_owner":
        acct = _get_account(withdrawal_account)
        if acct["owner_id"] != account_holder:
            raise PermissionError(
                f"User {account_holder} is not the owner of account {withdrawal_account}"
            )
        return

    # Other roles are not permitted to transfer funds
    raise PermissionError(
        f"User role '{user_role}' is not authorized to transfer funds."
    )


def send_funds(
    account_holder: str,
    user_role: str,
    withdrawal_account: str,
    receiving_account: str,
    fund_amount: float,
) -> str:
    """
    Move money from one account to another.

    Parameters
    ----------
    account_holder : str
        The ID of the user initiating the transaction.
    user_role : str
        Role of the user ('account_owner', 'bank_admin', or 'customer_service').
    withdrawal_account : str
        Account number to withdraw from.
    receiving_account : str
        Account number to deposit into.
    fund_amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message upon completion.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    KeyError
        If either account does not exist.
    ValueError
        If the fund amount is non‑positive or insufficient balance.
    """
    if fund_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Authorization check
    _authorize_transfer(account_holder, user_role, withdrawal_account)

    # Retrieve accounts (will raise KeyError if missing)
    withdraw_acct = _get_account(withdrawal_account)
    receive_acct = _get_account(receiving_account)

    # Check sufficient funds
    if withdraw_acct["balance"] < fund_amount:
        raise ValueError(
            f"Insufficient funds in account {withdrawal_account}."
        )

    # Perform the transfer atomically
    withdraw_acct["balance"] -= fund_amount
    receive_acct["balance"] += fund_amount

    return (
        f"Transfer of ${fund_amount:.2f} from account {withdrawal_account} "
        f"to account {receiving_account} completed successfully."
    )