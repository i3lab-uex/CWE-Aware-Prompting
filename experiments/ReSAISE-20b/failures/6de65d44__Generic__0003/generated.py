#!/usr/bin/env python3
"""
Banking system – transfer money between accounts.

The function `move_money` performs the following checks before
moving funds:

1. Both source and destination accounts exist.
2. The initiating user is authorized to perform the transfer
   (either owns the source account or has an elevated role).
3. The source account has sufficient balance for the transfer.

If all checks pass, the balances are updated and a success message
is returned.  Otherwise an appropriate exception is raised.
"""

from __future__ import annotations

import threading
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Dummy database – in a real system this would be replaced by a persistent store
# --------------------------------------------------------------------------- #
ACCOUNTS_DB: Dict[str, Dict[str, Any]] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user_123", "balance": 5000.00},
    "ACC2002": {"account_number": "ACC2002", "owner_id": "user_456", "balance": 3000.00},
    "ACC3003": {"account_number": "ACC3003", "owner_id": "user_789", "balance": 7500.00},
}

# A lock to guard concurrent updates to the accounts database
_db_lock = threading.RLock()


def move_money(
    person_id: str,
    role: str,
    source_account: str,
    destination_account: str,
    transfer_amount: float,
) -> str:
    """
    Transfer money from `source_account` to `destination_account`.

    Parameters
    ----------
    person_id : str
        The ID of the user initiating the transfer.
    role : str
        Role of the user. Accepted values: 'account_owner',
        'bank_admin', or 'customer_service'.
    source_account : str
        Account number to withdraw funds from.
    destination_account : str
        Account number to deposit funds into.
    transfer_amount : float
        Amount of money to transfer. Must be positive.

    Returns
    -------
    str
        Success message confirming the transfer.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    ValueError
        For invalid accounts, insufficient funds, or non‑positive amount.
    """
    # Basic input validation
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    with _db_lock:
        src = ACCOUNTS_DB.get(source_account)
        dst = ACCOUNTS_DB.get(destination_account)

        if src is None:
            raise ValueError(f"Source account '{source_account}' does not exist.")
        if dst is None:
            raise ValueError(f"Destination account '{destination_account}' does not exist.")

        # Authorization check
        is_owner = src["owner_id"] == person_id
        has_privilege = role in {"bank_admin", "customer_service"}
        if not (is_owner or has_privilege):
            raise PermissionError(
                f"User '{person_id}' with role '{role}' is not authorized "
                f"to transfer from account '{source_account}'."
            )

        # Sufficient funds check
        if src["balance"] < transfer_amount:
            raise ValueError(
                f"Insufficient funds in account '{source_account}'. "
                f"Available: {src['balance']:.2f}, required: {transfer_amount:.2f}."
            )

        # Perform the transfer atomically
        src["balance"] -= transfer_amount
        dst["balance"] += transfer_amount

    return (
        f"Transfer of ${transfer_amount:.2f} from account "
        f"{source_account} to {destination_account} completed successfully."
    )