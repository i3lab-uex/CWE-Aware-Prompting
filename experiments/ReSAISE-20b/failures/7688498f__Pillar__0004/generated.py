# -*- coding: utf-8 -*-
"""
Implementation of a secure fund transfer function.
The function checks for proper authorization and account validity
before performing the transaction.  It uses Decimal for monetary
operations to avoid floating‑point inaccuracies.
"""

from decimal import Decimal, getcontext, ROUND_HALF_EVEN
from typing import Dict

# Set a sensible precision for monetary calculations
getcontext().prec = 28
getcontext().rounding = ROUND_HALF_EVEN

# Sample accounts database (would normally be persisted elsewhere)
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC001": {"account_number": "ACC001", "owner_id": "USR123", "balance": Decimal("1000.00")},
    "ACC002": {"account_number": "ACC002", "owner_id": "USR456", "balance": Decimal("500.00")},
    # Add more accounts as needed
}

# Define which roles are allowed to perform transfers
ALLOWED_ROLES = {"account_owner", "bank_admin", "customer_service"}

def fund_transfer(
    u_identifier: str,
    u_role: str,
    account_from: str,
    account_to: str,
    transfer_amount: float
) -> str:
    """
    Transfer funds from one account to another after validating
    authorization and sufficient balance.

    Parameters:
        u_identifier (str): ID of the user requesting the transfer.
        u_role (str): Role of the user ('account_owner', 'bank_admin',
                      or 'customer_service').
        account_from (str): Source account number.
        account_to (str): Destination account number.
        transfer_amount (float): Amount to transfer.

    Returns:
        str: Success message indicating the new balances.

    Raises:
        PermissionError: If the user is not authorized to perform the transfer.
        ValueError: If accounts are invalid, insufficient funds,
                    or negative transfer amount is provided.
    """

    # Basic validation
    if u_role not in ALLOWED_ROLES:
        raise PermissionError(f"Role '{u_role}' is not authorized to perform transfers.")

    if account_from not in ACCOUNTS_DB:
        raise ValueError(f"Source account '{account_from}' does not exist.")
    if account_to not in ACCOUNTS_DB:
        raise ValueError(f"Destination account '{account_to}' does not exist.")

    src_account = ACCOUNTS_DB[account_from]
    dst_account = ACCOUNTS_DB[account_to]

    # Convert amount to Decimal for accurate arithmetic
    try:
        amt = Decimal(str(transfer_amount))
    except Exception as exc:
        raise ValueError(f"Invalid transfer amount: {transfer_amount}") from exc

    if amt <= Decimal("0"):
        raise ValueError("Transfer amount must be positive.")

    # Authorization: user can transfer from an account they own,
    # or if they are a bank_admin, or customer_service (who may have
    # broader permissions but still must be explicit).
    if u_role == "account_owner" and src_account["owner_id"] != u_identifier:
        raise PermissionError("Account owner does not match the source account.")

    # For bank_admin and customer_service we assume they have
    # global permissions.  In a real system, additional checks would be added.

    if src_account["balance"] < amt:
        raise ValueError("Insufficient funds in the source account.")

    # Perform the transfer atomically
    src_account["balance"] -= amt
    dst_account["balance"] += amt

    return (
        f"Transfer of {amt:.2f} from '{account_from}' to '{account_to}' completed.\n"
        f"New balance - {account_from}: {src_account['balance']:.2f}, "
        f"{account_to}: {dst_account['balance']:.2f}"
    )

# Example usage (uncomment to test):
# try:
#     print(fund_transfer("USR123", "account_owner", "ACC001", "ACC002", 200.00))
# except Exception as e:
#     print(f"Error: {e}")