# -*- coding: utf-8 -*-
"""
A minimal, but safe implementation of a money transfer between two bank accounts.
The function enforces proper authorization and performs the update atomically.
"""

from __future__ import annotations

import threading
from typing import Dict, Any

# --- Sample in‑memory database -----------------------------------------------
ACCOUNTS_DB: Dict[str, Dict[str, Any]] = {
    # account_number : {owner_id: str, balance: float}
    "ACC123": {"account_number": "ACC123", "owner_id": "user_1", "balance": 1000.0},
    "ACC456": {"account_number": "ACC456", "owner_id": "user_2", "balance": 500.0},
    # ... more accounts
}

# Lock for synchronising access to the database (simple demo, not a real DB lock)
DB_LOCK = threading.RLock()


def _authorize_transfer(
    initiator_id: str,
    position: str,
    withdraw_account: str,
) -> None:
    """
    Checks whether the initiator is allowed to transfer from the given account.
    Raises PermissionError if not authorised.

    Rules:
      * The initiator must be the owner of the withdraw_account.
      * Or the initiator must have a 'bank_admin' position.
    """
    account = ACCOUNTS_DB.get(withdraw_account)
    if not account:
        raise KeyError(f"Withdraw account {withdraw_account} does not exist")

    if position == "bank_admin":
        return  # admins can transfer from any account

    if initiator_id != account["owner_id"]:
        raise PermissionError(
            f"User '{initiator_id}' is not authorised to withdraw from account "
            f"'{withdraw_account}'."
        )


def _validate_and_prepare(
    withdraw_account: str,
    deposit_account: str,
    transfer_value: float,
) -> None:
    """
    Validates the accounts and balance before performing a transfer.
    Raises ValueError on any invalid condition.
    """
    if transfer_value <= 0:
        raise ValueError("Transfer value must be a positive amount")

    if withdraw_account == deposit_account:
        raise ValueError("Withdraw and deposit accounts must differ")

    with DB_LOCK:
        withdraw_acct = ACCOUNTS_DB.get(withdraw_account)
        deposit_acct = ACCOUNTS_DB.get(deposit_account)

        if not withdraw_acct:
            raise KeyError(f"Withdraw account {withdraw_account} does not exist")
        if not deposit_acct:
            raise KeyError(f"Deposit account {deposit_account} does not exist")

        if withdraw_acct["balance"] < transfer_value:
            raise ValueError(
                f"Insufficient funds in account {withdraw_account}: "
                f"{withdraw_acct['balance']} available, {transfer_value} required."
            )


def initiate_transfer(
    initiator_id: str,
    position: str,
    withdraw_account: str,
    deposit_account: str,
    transfer_value: float,
) -> str:
    """
    Performs a money transfer between two accounts after verifying authorization.

    Parameters
    ----------
    initiator_id : str
        ID of the user initiating the transfer.
    position : str
        Role of the initiator (e.g., 'account_owner', 'bank_admin').
    withdraw_account : str
        Account number to debit.
    deposit_account : str
        Account number to credit.
    transfer_value : float
        Amount to transfer.

    Returns
    -------
    str
        Success message confirming the transfer.

    Raises
    ------
    PermissionError
        If the initiator is not authorised to transfer from the withdraw account.
    KeyError, ValueError
        For invalid accounts or insufficient funds.
    """
    # 1. Authorise the transfer
    _authorize_transfer(initiator_id, position, withdraw_account)

    # 2. Validate accounts and balance
    _validate_and_prepare(withdraw_account, deposit_account, transfer_value)

    # 3. Perform the transfer atomically
    with DB_LOCK:
        ACCOUNTS_DB[withdraw_account]["balance"] -= transfer_value
        ACCOUNTS_DB[deposit_account]["balance"] += transfer_value

    return (
        f"Transfer of {transfer_value:.2f} from '{withdraw_account}' "
        f"to '{deposit_account}' completed successfully."
    )