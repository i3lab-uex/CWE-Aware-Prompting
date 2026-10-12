# -*- coding: utf-8 -*-
"""
Module providing a secure fund transfer operation.
"""

from __future__ import annotations

import threading
from typing import Dict, Any

# Sample in‑memory database of accounts.
ACCOUNTS_DB: Dict[str, Dict[str, Any]] = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user123", "balance": 1500.00},
    "ACC002": {"account_number": "ACC002", "owner_id": "user456", "balance": 800.00},
    "ACC003": {"account_number": "ACC003", "owner_id": "user123", "balance": 300.00},
}

# Global lock to serialize updates and avoid race conditions.
_db_lock = threading.RLock()


def fund_transfer(
    u_identifier: str,
    u_role: str,
    account_from: str,
    account_to: str,
    transfer_amount: float,
) -> str:
    """
    Transfer money from one account to another with proper authorization checks.

    Parameters
    ----------
    u_identifier : str
        Identifier of the user requesting the transfer.
    u_role : str
        Role of the user (e.g., 'account_owner', 'bank_admin', 'customer_service').
    account_from : str
        Source account number.
    account_to : str
        Destination account number.
    transfer_amount : float
        Amount to transfer.

    Returns
    -------
    str
        Success message indicating the transfer has completed.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    ValueError
        For invalid input values or insufficient funds.
    KeyError
        If one of the account numbers does not exist in the database.
    """
    # Basic validation
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")
    if account_from == account_to:
        raise ValueError("Source and destination accounts must differ.")

    with _db_lock:  # Ensure atomicity of the entire operation
        try:
            src = ACCOUNTS_DB[account_from]
            dst = ACCOUNTS_DB[account_to]
        except KeyError as exc:
            raise KeyError(f"Account '{exc.args[0]}' does not exist.") from exc

        # Authorization logic
        if u_role == "bank_admin":
            authorized = True  # admins can transfer between any accounts
        elif u_role == "account_owner":
            authorized = src["owner_id"] == u_identifier and dst["owner_id"] == u_identifier
        else:
            # other roles (e.g., customer_service) are not allowed to transfer funds directly
            authorized = False

        if not authorized:
            raise PermissionError(
                f"User '{u_identifier}' with role '{u_role}' is not authorized to transfer from "
                f"'{account_from}' to '{account_to}'."
            )

        # Check sufficient balance
        if src["balance"] < transfer_amount:
            raise ValueError(
                f"Insufficient funds in source account '{account_from}'. "
                f"Available: {src['balance']:.2f}, required: {transfer_amount:.2f}."
            )

        # Perform the transfer
        src["balance"] -= transfer_amount
        dst["balance"] += transfer_amount

    return (
        f"Transfer of {transfer_amount:.2f} from '{account_from}' to "
        f"'{account_to}' completed successfully."
    )