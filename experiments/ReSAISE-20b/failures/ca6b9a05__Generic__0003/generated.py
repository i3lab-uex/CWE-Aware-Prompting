# -*- coding: utf-8 -*-
"""
Financial transfer utility.

This module provides a single public function `move_funds` which handles
transferring money between accounts while enforcing role‑based permissions.
"""

from __future__ import annotations
import logging
from typing import Dict

# Configure a basic logger for audit purposes
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(module)s] %(message)s",
)

# Sample in‑memory accounts database
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "U001", "balance": 1500.00},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "U002", "balance": 2500.00},
    "ACC1003": {"account_number": "ACC1003", "owner_id": "U003", "balance": 500.00},
}


def _authorize_transfer(
    u_id: str, u_role: str, src_account: str, dst_account: str
) -> None:
    """
    Validate that the user has permission to move funds between the specified accounts.

    Raises
    ------
    PermissionError
        If the user does not have sufficient privileges.
    ValueError
        If either account number is unknown.
    """
    if src_account not in ACCOUNTS_DB:
        raise ValueError(f"Source account '{src_account}' does not exist.")
    if dst_account not in ACCOUNTS_DB:
        raise ValueError(f"Destination account '{dst_account}' does not exist.")

    src_owner = ACCOUNTS_DB[src_account]["owner_id"]
    dst_owner = ACCOUNTS_DB[dst_account]["owner_id"]

    # Bank administrators can move any funds
    if u_role == "bank_admin":
        return

    # Account owners can only transfer from their own accounts
    if u_role == "account_owner":
        if u_id != src_owner:
            raise PermissionError(
                f"User '{u_id}' is not the owner of source account '{src_account}'."
            )
        return

    # Customer service staff are not permitted to move funds
    if u_role == "customer_service":
        raise PermissionError(
            f"User role '{u_role}' is not authorized to transfer funds."
        )

    # Default: deny all other roles
    raise PermissionError(
        f"User role '{u_role}' is not recognized or authorized for transfers."
    )


def move_funds(
    u_id: str,
    u_role: str,
    source_account: str,
    destination_account: str,
    money: float,
) -> str:
    """
    Transfer funds between two accounts after performing authorization checks.

    Parameters
    ----------
    u_id : str
        Identifier of the individual requesting the transfer.
    u_role : str
        Role of the individual (e.g., 'account_owner', 'bank_admin',
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
        Success message indicating the completed transfer.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform this transfer.
    ValueError
        For invalid accounts or insufficient balance.
    """
    # Basic input validation
    if money <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Authorize the transaction
    _authorize_transfer(u_id, u_role, source_account, destination_account)

    src_acc = ACCOUNTS_DB[source_account]
    dst_acc = ACCOUNTS_DB[destination_account]

    # Check for sufficient balance
    if src_acc["balance"] < money:
        raise ValueError(
            f"Insufficient funds in source account '{source_account}'. "
            f"Available: {src_acc['balance']:.2f}, Requested: {money:.2f}"
        )

    # Perform the transfer atomically
    src_acc["balance"] -= money
    dst_acc["balance"] += money

    # Log the transaction for audit
    logging.info(
        f"User '{u_id}' ({u_role}) transferred {money:.2f} "
        f"from '{source_account}' to '{destination_account}'."
    )

    return (
        f"Transfer of {money:.2f} from account '{source_account}' "
        f"to account '{destination_account}' completed successfully."
    )