# -*- coding: utf-8 -*-
"""
Utility module for transferring funds between accounts with proper access control.
"""

from __future__ import annotations

import logging
from typing import Dict, Any

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Example in‑memory database of accounts
ACCOUNTS_DB: Dict[str, Dict[str, Any]] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "U001", "balance": 5000.0},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "U002", "balance": 3000.0},
    "ACC1003": {"account_number": "ACC1003", "owner_id": "U003", "balance": 7500.0},
}


def _is_authorized(u_id: str, u_role: str, source_account: str) -> bool:
    """
    Internal helper to verify if the user has permission to move funds from
    the source account.
    """
    # Bank administrators can transfer any account
    if u_role == "bank_admin":
        return True

    # Account owners can only transfer from their own accounts
    account = ACCOUNTS_DB.get(source_account)
    if not account:
        return False

    return u_role == "account_owner" and account["owner_id"] == u_id


def move_funds(
    u_id: str,
    u_role: str,
    source_account: str,
    destination_account: str,
    money: float,
) -> str:
    """
    Transfer funds between two accounts while enforcing access control.

    Parameters
    ----------
    u_id : str
        Identifier of the individual requesting the transfer.
    u_role : str
        Role held by the individual (e.g., 'account_owner', 'bank_admin',
        'customer_service').
    source_account : str
        Account number from which funds will be withdrawn.
    destination_account : str
        Account number where funds will be deposited.
    money : float
        Amount to transfer.

    Returns
    -------
    str
        Success message indicating completion of the transfer.

    Raises
    ------
    PermissionError
        If the user is not authorized to move funds from the source account.
    ValueError
        For invalid input values (negative amount, missing accounts).
    """

    # Basic input validation
    if money <= 0:
        raise ValueError("Transfer amount must be positive.")
    src = ACCOUNTS_DB.get(source_account)
    dst = ACCOUNTS_DB.get(destination_account)

    if src is None:
        raise ValueError(f"Source account '{source_account}' does not exist.")
    if dst is None:
        raise ValueError(f"Destination account '{destination_account}' does not exist.")

    # Authorization check
    if not _is_authorized(u_id, u_role, source_account):
        logger.warning(
            "Unauthorized transfer attempt by user %s (role: %s) "
            "from account %s to %s for amount %.2f",
            u_id,
            u_role,
            source_account,
            destination_account,
            money,
        )
        raise PermissionError("You do not have permission to transfer funds from this account.")

    # Check sufficient balance
    if src["balance"] < money:
        raise ValueError("Insufficient funds in source account.")

    # Perform the transfer atomically
    src["balance"] -= money
    dst["balance"] += money

    logger.info(
        "User %s (role: %s) transferred %.2f from %s to %s",
        u_id,
        u_role,
        money,
        source_account,
        destination_account,
    )

    return (
        f"Transfer of ${money:,.2f} from account {source_account} "
        f"to account {destination_account} completed successfully."
    )