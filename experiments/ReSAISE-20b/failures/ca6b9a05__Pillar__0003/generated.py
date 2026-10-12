# -*- coding: utf-8 -*-
"""
Financial transfer helper module.

This module implements a single function `move_funds` that performs
fund transfers between accounts while enforcing access control rules.
The implementation follows the requirements for CWE‑284 (Improper Access
Control) by ensuring that only authorized users can initiate a transfer.
"""

from __future__ import annotations

import decimal
from typing import Dict, Any

# Example in‑memory database of accounts.
ACCOUNTS_DB: Dict[str, Dict[str, Any]] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user_001", "balance": decimal.Decimal("1500.00")},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "user_002", "balance": decimal.Decimal("2500.00")},
    # Add more accounts as needed
}

# Allowed roles that can initiate a transfer
ALLOWED_ROLES = {"account_owner", "bank_admin", "customer_service"}

# Roles that are allowed to transfer funds from any account
ADMIN_ROLES = {"bank_admin"}


def _get_account(account_number: str) -> Dict[str, Any]:
    """
    Retrieve an account from the database.

    Parameters
    ----------
    account_number : str
        The account number to look up.

    Returns
    -------
    dict
        The account dictionary.

    Raises
    ------
    KeyError
        If the account does not exist.
    """
    try:
        return ACCOUNTS_DB[account_number]
    except KeyError as exc:
        raise KeyError(f"Account {account_number} does not exist.") from exc


def _check_authorization(u_id: str, u_role: str, source_account: Dict[str, Any]) -> None:
    """
    Verify that the caller is authorized to transfer funds from the source account.

    Parameters
    ----------
    u_id : str
        Identifier of the user making the request.
    u_role : str
        Role of the user.
    source_account : dict
        The account dictionary from which funds will be withdrawn.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    """
    if u_role not in ALLOWED_ROLES:
        raise PermissionError(f"Role '{u_role}' is not permitted to transfer funds.")

    if u_role in ADMIN_ROLES:
        # Administrators can move any funds
        return

    if u_role == "account_owner" and source_account["owner_id"] != u_id:
        raise PermissionError("Account owners can only transfer from their own accounts.")

    # For other roles (e.g., customer_service) you can add further restrictions here
    if u_role == "customer_service":
        # Example restriction: cannot transfer more than a threshold
        raise PermissionError("Customer service role does not have transfer privileges.")


def move_funds(u_id: str,
               u_role: str,
               source_account_number: str,
               destination_account_number: str,
               money: float) -> str:
    """
    Transfer funds between two accounts after verifying authorization.

    Parameters
    ----------
    u_id : str
        Identifier of the individual requesting the transfer.
    u_role : str
        Role held by the individual.
    source_account_number : str
        Account from which funds will be removed.
    destination_account_number : str
        Account where funds will be deposited.
    money : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message indicating the transfer was completed.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    KeyError
        If either account does not exist.
    ValueError
        If the amount is negative or insufficient funds are available.
    """
    if money <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Retrieve accounts
    src_acc = _get_account(source_account_number)
    dst_acc = _get_account(destination_account_number)

    # Authorization check
    _check_authorization(u_id, u_role, src_acc)

    # Use Decimal for precise monetary calculations
    amount = decimal.Decimal(str(money))

    if src_acc["balance"] < amount:
        raise ValueError(f"Insufficient funds in source account {source_account_number}.")

    # Perform the transfer
    src_acc["balance"] -= amount
    dst_acc["balance"] += amount

    return (
        f"Transfer of {amount:.2f} from {source_account_number} "
        f"to {destination_account_number} completed successfully."
    )