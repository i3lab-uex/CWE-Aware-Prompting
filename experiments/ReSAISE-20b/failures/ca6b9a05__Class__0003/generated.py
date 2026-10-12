# -*- coding: utf-8 -*-
"""
A minimal financial transfer module with secure authorization checks.
"""

from typing import Dict

# Example accounts database
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user_a", "balance": 5000.00},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "user_b", "balance": 3000.00},
    "ACC1003": {"account_number": "ACC1003", "owner_id": "user_c", "balance": 7500.00},
}

# Roles that can perform any transfer
ALLOWED_ROLES = {"bank_admin", "customer_service"}


def _is_authorized(u_id: str, u_role: str, src_acc: Dict) -> bool:
    """
    Determines if the user is allowed to initiate a transfer from src_acc.
    The function uses strict checks:
      - Admins and CS can do anything
      - Account owners can only transfer from their own accounts
    """
    if u_role in ALLOWED_ROLES:
        return True

    # Only the owner of the source account may initiate a transfer
    return src_acc.get("owner_id") == u_id


def move_funds(
    u_id: str,
    u_role: str,
    source_account: str,
    destination_account: str,
    money: float
) -> str:
    """
    Transfer `money` from `source_account` to `destination_account`.

    Raises:
        KeyError: If either account number does not exist.
        PermissionError: If the user is not authorized to perform this transfer.
        ValueError: If funds are insufficient or money is non‑positive.

    Returns:
        str: Success message.
    """
    if money <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Retrieve accounts from the database
    src_acc = ACCOUNTS_DB.get(source_account)
    dst_acc = ACCOUNTS_DB.get(destination_account)

    if src_acc is None or dst_acc is None:
        missing = [acc for acc, val in [(source_account, src_acc), (destination_account, dst_acc)] if val is None]
        raise KeyError(f"Account(s) not found: {', '.join(missing)}")

    # Authorization check (CWE-863 safe implementation)
    if not _is_authorized(u_id, u_role, src_acc):
        raise PermissionError("User is not authorized to transfer from this account.")

    # Ensure sufficient funds
    if src_acc["balance"] < money:
        raise ValueError("Insufficient balance in source account.")

    # Perform transfer atomically
    src_acc["balance"] -= money
    dst_acc["balance"] += money

    return (
        f"Transfer of ${money:,.2f} from {source_account} to "
        f"{destination_account} completed successfully."
    )


# Example usage
if __name__ == "__main__":
    try:
        msg = move_funds(
            u_id="user_a",
            u_role="account_owner",
            source_account="ACC1001",
            destination_account="ACC1002",
            money=1500.00,
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")