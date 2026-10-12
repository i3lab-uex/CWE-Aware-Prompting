# -*- coding: utf-8 -*-
"""
Banking utilities – fund transfer module.
"""

from __future__ import annotations

import datetime
from typing import Dict, Any


# Example in‑memory accounts database.
ACCOUNTS_DB: Dict[str, Dict[str, Any]] = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user_1", "balance": 1200.50},
    "ACC002": {"account_number": "ACC002", "owner_id": "user_2", "balance": 500.00},
    # Add more accounts as needed.
}


class BankError(Exception):
    """Base class for bank‑related errors."""


class UnauthorizedAccess(BankError, PermissionError):
    """Raised when a user is not authorized to perform an operation."""


class InsufficientFunds(BankError, ValueError):
    """Raised when the source account lacks sufficient balance."""


class AccountNotFound(BankError, KeyError):
    """Raised when an account number does not exist in the database."""


def _get_account(account_number: str) -> Dict[str, Any]:
    """
    Retrieve an account from the database.

    Raises:
        AccountNotFound: if the account does not exist.
    """
    try:
        return ACCOUNTS_DB[account_number]
    except KeyError as exc:
        raise AccountNotFound(f"Account {account_number} not found") from exc


def _is_authorized(
    initiator_id: str,
    initiator_role: str,
    source_account: Dict[str, Any],
) -> bool:
    """
    Determine whether the initiator has permission to withdraw from the source account.

    Rules:
        - `account_owner`: can only act on their own account.
        - `bank_admin` and `customer_service`: allowed to act on any account.
    """
    if initiator_role in {"bank_admin", "customer_service"}:
        return True
    if initiator_role == "account_owner" and source_account["owner_id"] == initiator_id:
        return True
    return False


def shift_funds(
    initiator_id: str,
    initiator_role: str,
    withdraw_account: str,
    deposit_account: str,
    transfer_value: float,
) -> str:
    """
    Transfer money from one account to another.

    Parameters
    ----------
    initiator_id : str
        User ID initiating the transaction.
    initiator_role : str
        Role of the user (`account_owner`, `bank_admin`, or `customer_service`).
    withdraw_account : str
        Account number to withdraw funds from.
    deposit_account : str
        Account number to deposit funds into.
    transfer_value : float
        Amount to transfer.

    Returns
    -------
    str
        Success message if the transfer succeeds.

    Raises
    ------
    UnauthorizedAccess
        If the initiator is not allowed to perform this transfer.
    InsufficientFunds
        If the source account has insufficient balance.
    AccountNotFound
        If either account number is invalid.
    ValueError
        If the transfer value is non‑positive.
    """
    if transfer_value <= 0:
        raise ValueError("Transfer value must be positive")

    source = _get_account(withdraw_account)
    destination = _get_account(deposit_account)

    if not _is_authorized(initiator_id, initiator_role, source):
        raise UnauthorizedAccess(
            f"User {initiator_id} with role '{initiator_role}' "
            f"is not authorized to withdraw from account {withdraw_account}"
        )

    if source["balance"] < transfer_value:
        raise InsufficientFunds(
            f"Insufficient funds in account {withdraw_account}. "
            f"Available: {source['balance']}, required: {transfer_value}"
        )

    # Perform the transfer atomically (simple simulation)
    source["balance"] -= transfer_value
    destination["balance"] += transfer_value

    timestamp = datetime.datetime.utcnow().isoformat()
    return (
        f"Transfer of {transfer_value:.2f} from {withdraw_account} to "
        f"{deposit_account} completed successfully at {timestamp}."
    )