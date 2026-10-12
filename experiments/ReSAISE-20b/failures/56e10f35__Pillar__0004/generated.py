# -*- coding: utf-8 -*-
"""
Banking transfer module.

This module implements a simple in‑memory banking system that supports
transferring money between accounts while enforcing access control.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict

# Configure basic logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# Data structures
# --------------------------------------------------------------------------- #

@dataclass
class Account:
    """Represents a bank account."""
    account_number: str
    owner_id: str
    balance: float = field(default=0.0)

# In‑memory database of accounts (account_number -> Account)
ACCOUNTS_DB: Dict[str, Account] = {
    "ACC1001": Account("ACC1001", owner_id="user_001", balance=1500.0),
    "ACC2002": Account("ACC2002", owner_id="user_002", balance= 500.0),
    "ACC3003": Account("ACC3003", owner_id="user_003", balance= 750.0),
}

# --------------------------------------------------------------------------- #
# Authorization helpers
# --------------------------------------------------------------------------- #

def _is_authorized(
    initiator_id: str,
    position: str,
    withdraw_account: Account,
) -> bool:
    """
    Determine whether the initiator is allowed to withdraw from the given account.
    Authorization rules:
        * 'account_owner' – must be the owner of the withdraw_account
        * 'bank_admin'   – has unrestricted access to all accounts
        * 'customer_service' – can withdraw only if the initiator is the owner
    """
    # Normalize role names
    role = position.lower()

    if role == "bank_admin":
        return True

    if role in ("account_owner", "customer_service"):
        # Only the owner can initiate a transfer from their account
        return initiator_id == withdraw_account.owner_id

    # Unknown role – deny access
    return False


# --------------------------------------------------------------------------- #
# Core transfer logic
# --------------------------------------------------------------------------- #

def initiate_transfer(
    initiator_id: str,
    position: str,
    withdraw_account: str,
    deposit_account: str,
    transfer_value: float,
) -> str:
    """
    Transfer funds from one account to another.

    Parameters
    ----------
    initiator_id : str
        ID of the user initiating the transfer.
    position : str
        Role of the initiator (e.g., 'account_owner', 'bank_admin',
        'customer_service').
    withdraw_account : str
        Account number to debit.
    deposit_account : str
        Account number to credit.
    transfer_value : float
        Amount to transfer.

    Returns
    -------
    str
        Success message indicating the amount transferred and new balances.

    Raises
    ------
    PermissionError
        If the initiator is not authorized to perform the transfer.
    KeyError
        If either account number does not exist in the database.
    ValueError
        For invalid transfer amounts (e.g., negative or insufficient funds).
    """
    logger.debug(
        "Attempting transfer: %s -> %s of %.2f by user '%s' as '%s'",
        withdraw_account,
        deposit_account,
        transfer_value,
        initiator_id,
        position,
    )

    # Basic validation
    if transfer_value <= 0:
        raise ValueError("Transfer value must be positive.")

    try:
        source_acc = ACCOUNTS_DB[withdraw_account]
        target_acc = ACCOUNTS_DB[deposit_account]
    except KeyError as exc:
        raise KeyError(f"Account '{exc.args[0]}' not found.") from None

    # Authorization check
    if not _is_authorized(initiator_id, position, source_acc):
        raise PermissionError(
            f"User '{initiator_id}' with role '{position}' is not authorized "
            f"to withdraw from account {withdraw_account}."
        )

    # Sufficient funds check
    if source_acc.balance < transfer_value:
        raise ValueError(
            f"Insufficient funds in account {withdraw_account}. "
            f"Available: {source_acc.balance:.2f}, required: {transfer_value:.2f}."
        )

    # Perform the transfer atomically (simple approach)
    source_acc.balance -= transfer_value
    target_acc.balance += transfer_value

    logger.info(
        "Transfer successful: %.2f from %s to %s",
        transfer_value,
        withdraw_account,
        deposit_account,
    )

    return (
        f"Transfer of {transfer_value:.2f} from account {withdraw_account}"
        f" to account {deposit_account} completed successfully.\n"
        f"New balances:\n  {withdraw_account}: {source_acc.balance:.2f}\n"
        f"  {deposit_account}: {target_acc.balance:.2f}"
    )


# --------------------------------------------------------------------------- #
# Example usage (commented out – remove comments to run)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        msg = initiate_transfer(
            initiator_id="user_001",
            position="account_owner",
            withdraw_account="ACC1001",
            deposit_account="ACC2002",
            transfer_value=300.0,
        )
        print(msg)
    except Exception as exc:
        logger.error("Transfer failed: %s", exc)