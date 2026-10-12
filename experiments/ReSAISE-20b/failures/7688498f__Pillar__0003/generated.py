# -*- coding: utf-8 -*-

"""
Financial system fund transfer module.

This implementation demonstrates a simple yet secure
transfer function that respects access control rules
(CWE-284).  It uses a global in‑memory database
(`ACCOUNTS_DB`) to store account information.
"""

from __future__ import annotations

import threading
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Sample accounts database.  In a real system this would be replaced by a
# persistent store (e.g., SQL, NoSQL) and proper authentication tokens.
# --------------------------------------------------------------------------- #
ACCOUNTS_DB: Dict[str, Dict[str, Any]] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user_001", "balance": 5000.00},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "user_002", "balance": 1200.00},
    # ... more accounts
}

# --------------------------------------------------------------------------- #
# Thread lock to guard the shared database during updates.
# This prevents race conditions in concurrent environments.
# --------------------------------------------------------------------------- #
_db_lock = threading.Lock()


def fund_transfer(
    u_identifier: str,
    u_role: str,
    account_from: str,
    account_to: str,
    transfer_amount: float
) -> str:
    """
    Transfer funds between two accounts.

    Parameters
    ----------
    u_identifier : str
        Identifier of the user initiating the transfer.
    u_role : str
        Role of the user (e.g., 'account_owner', 'bank_admin',
        'customer_service').
    account_from : str
        Source account number.
    account_to : str
        Destination account number.
    transfer_amount : float
        Amount to transfer.

    Returns
    -------
    str
        Success message upon completion.

    Raises
    ------
    PermissionError
        If the user is not authorized to transfer from the source account.
    ValueError
        For invalid accounts, negative amounts, or insufficient funds.
    """
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Validate account existence
    with _db_lock:
        src = ACCOUNTS_DB.get(account_from)
        dst = ACCOUNTS_DB.get(account_to)

    if src is None:
        raise ValueError(f"Source account '{account_from}' does not exist.")
    if dst is None:
        raise ValueError(f"Destination account '{account_to}' does not exist.")

    # Authorization check
    is_owner = u_identifier == src["owner_id"]
    has_admin_privileges = u_role in {"bank_admin", "customer_service"}

    if not (is_owner or has_admin_privileges):
        raise PermissionError(
            f"User '{u_identifier}' with role '{u_role}' is not authorized "
            "to transfer from account '{}'.".format(account_from)
        )

    # Perform the transfer atomically
    with _db_lock:
        if src["balance"] < transfer_amount:
            raise ValueError(
                f"Insufficient funds in account '{account_from}'. "
                f"Available: {src['balance']:.2f}, Requested: {transfer_amount:.2f}"
            )
        src["balance"] -= transfer_amount
        dst["balance"] += transfer_amount

    return (
        f"Transfer of {transfer_amount:.2f} from account '{account_from}' "
        f"to account '{account_to}' completed successfully."
    )


# --------------------------------------------------------------------------- #
# Example usage (commented out for unit-test friendliness)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        msg = fund_transfer(
            u_identifier="user_001",
            u_role="account_owner",
            account_from="ACC1001",
            account_to="ACC1002",
            transfer_amount=300.00,
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")