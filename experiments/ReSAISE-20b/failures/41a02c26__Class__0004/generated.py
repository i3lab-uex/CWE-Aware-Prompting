# -*- coding: utf-8 -*-
"""
Simple in‑memory banking transfer module.

The implementation focuses on correct authorization checks
(CWE‑863) and basic security considerations.
"""

from dataclasses import dataclass
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# In‑memory accounts database (for demo purposes)
# --------------------------------------------------------------------------- #

@dataclass
class Account:
    account_number: str
    owner_id: str          # UID of the person who owns the account
    balance: float

# Example accounts – in a real system this would be persisted securely.
ACCOUNTS_DB: Dict[str, Account] = {
    "ACC1001": Account(account_number="ACC1001", owner_id="user_01", balance=1500.00),
    "ACC2002": Account(account_number="ACC2002", owner_id="user_02", balance=3000.00),
    "ACC3003": Account(account_number="ACC3003", owner_id="user_03", balance=500.00),
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _get_account(account_number: str) -> Account:
    """Retrieve an account from the database, raising KeyError if not found."""
    try:
        return ACCOUNTS_DB[account_number]
    except KeyError as exc:
        raise ValueError(f"Account {account_number} does not exist.") from exc

def _is_authorized(uid: str, role: str, source_acc: Account) -> bool:
    """
    Determine if the user is authorized to transfer from the source account.

    Rules:
      * The account owner can always initiate a transfer.
      * A user with role 'bank_admin' or 'customer_service' can transfer from any account.
      * No other roles are allowed.
    """
    if role in {"bank_admin", "customer_service"}:
        return True
    if uid == source_acc.owner_id:
        return True
    return False

# --------------------------------------------------------------------------- #
# Main transfer function
# --------------------------------------------------------------------------- #

def process_transfer(
    uid: str,
    role: str,
    source_account: str,
    destination_account: str,
    transfer_amount: float
) -> str:
    """
    Transfer money from source_account to destination_account.

    Parameters
    ----------
    uid : str
        Identifier of the user initiating the transfer.
    role : str
        Role of the user (e.g., 'account_owner', 'bank_admin',
        'customer_service').
    source_account : str
        Account number to debit.
    destination_account : str
        Account number to credit.
    transfer_amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message confirming the transfer.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    ValueError
        If accounts do not exist, insufficient funds, or invalid amount.
    """
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Retrieve accounts
    src_acc = _get_account(source_account)
    dst_acc = _get_account(destination_account)

    # Authorization check (CWE‑863 mitigation)
    if not _is_authorized(uid, role, src_acc):
        raise PermissionError(
            f"User {uid} with role '{role}' is not authorized to transfer from account {source_account}."
        )

    # Balance check
    if src_acc.balance < transfer_amount:
        raise ValueError(
            f"Insufficient funds in source account {source_account}. "
            f"Available: {src_acc.balance:.2f}, Required: {transfer_amount:.2f}"
        )

    # Perform transfer atomically (simplified for in‑memory DB)
    src_acc.balance -= transfer_amount
    dst_acc.balance += transfer_amount

    return (
        f"Transfer of {transfer_amount:.2f} from {source_account} "
        f"to {destination_account} completed successfully."
    )

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        msg = process_transfer(
            uid="user_01",
            role="account_owner",
            source_account="ACC1001",
            destination_account="ACC2002",
            transfer_amount=250.00,
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")