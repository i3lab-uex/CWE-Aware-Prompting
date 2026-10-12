#!/usr/bin/env python3
"""
Banking system – transfer money between accounts.
"""

from __future__ import annotations

import threading
from typing import Dict

# --------------------------------------------------------------------------- #
# Mock database – in a real system this would be replaced by a persistent store
# --------------------------------------------------------------------------- #
ACCOUNTS_DB: Dict[str, Dict[str, object]] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user_123", "balance": 1500.00},
    "ACC2002": {"account_number": "ACC2002", "owner_id": "user_456", "balance": 3000.00},
    "ACC3003": {"account_number": "ACC3003", "owner_id": "user_789", "balance": 500.00},
}

# A simple lock to guard the mock DB during updates.
_DB_LOCK = threading.Lock()


def _get_account(account_number: str) -> Dict[str, object]:
    """Retrieve account dict; raise KeyError if not found."""
    try:
        return ACCOUNTS_DB[account_number]
    except KeyError as exc:
        raise ValueError(f"Account '{account_number}' does not exist.") from exc


def _authorize(person_id: str, role: str, source_account: Dict[str, object]) -> None:
    """Verify that the user can initiate a transfer from source_account."""
    if role == "bank_admin":
        return  # full access

    if role == "account_owner" and source_account["owner_id"] == person_id:
        return

    # customer_service or any other role is not permitted
    raise PermissionError(
        f"User '{person_id}' with role '{role}' is not authorized to transfer from "
        f"account '{source_account['account_number']}'."
    )


def move_money(
    person_id: str,
    role: str,
    source_account: str,
    destination_account: str,
    transfer_amount: float,
) -> str:
    """
    Move money from one account to another.

    Parameters
    ----------
    person_id : str
        Identifier of the user initiating the transfer.
    role : str
        Role of the user ('account_owner', 'bank_admin', or 'customer_service').
    source_account : str
        Account number to withdraw from.
    destination_account : str
        Account number to deposit into.
    transfer_amount : float
        Amount of money to transfer. Must be > 0.

    Returns
    -------
    str
        Success message confirming the transfer.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform this transfer.
    ValueError
        For invalid account numbers, insufficient funds or non‑positive amounts.
    """

    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    with _DB_LOCK:  # Ensure atomicity of the read‑modify‑write cycle
        src_acc = _get_account(source_account)
        dst_acc = _get_account(destination_account)

        # Authorization check
        _authorize(person_id, role, src_acc)

        if src_acc["balance"] < transfer_amount:
            raise ValueError(
                f"Insufficient funds in source account '{source_account}'. "
                f"Available: {src_acc['balance']:.2f}"
            )

        # Perform transfer
        src_acc["balance"] -= transfer_amount
        dst_acc["balance"] += transfer_amount

    return (
        f"Transfer of ${transfer_amount:.2f} from account '{source_account}' "
        f"to account '{destination_account}' completed successfully."
    )


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     try:
#         msg = move_money(
#             person_id="user_123",
#             role="account_owner",
#             source_account="ACC1001",
#             destination_account="ACC2002",
#             transfer_amount=250.00,
#         )
#         print(msg)
#     except Exception as e:
#         print(f"Error: {e}")