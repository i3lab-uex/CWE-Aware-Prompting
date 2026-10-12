# -*- coding: utf-8 -*-
"""
Banking transfer utility.

This module implements the `send_funds` function, which safely moves money
between accounts while enforcing strict access control rules.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import logging
from typing import Dict, Any

# Configure a module level logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------
# Sample in‑memory accounts database
# ----------------------------------------------------------------------
ACCOUNTS_DB: Dict[str, Dict[str, Any]] = {
    # Example accounts
    "ACC001": {"account_number": "ACC001", "owner_id": "user_123", "balance": 1500.00},
    "ACC002": {"account_number": "ACC002", "owner_id": "user_456", "balance": 3000.00},
    # Add more accounts as needed
}


# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _get_account(account_number: str) -> Dict[str, Any]:
    """
    Retrieve an account from the database.
    Raises KeyError if the account does not exist.
    """
    try:
        return ACCOUNTS_DB[account_number]
    except KeyError as exc:
        logger.error("Account %s not found", account_number)
        raise KeyError(f"Account '{account_number}' does not exist.") from exc


def _authorize(
    account_holder: str,
    user_role: str,
    withdrawal_account: Dict[str, Any],
) -> None:
    """
    Verify that the user is authorized to withdraw from the given account.
    Only the account owner, a bank administrator, or customer service can perform
    withdrawals.  This function raises PermissionError if the check fails.
    """
    # Check role-based permissions
    if user_role == "bank_admin":
        return  # full access

    if user_role == "customer_service":
        # Customer service can only act on behalf of the account owner
        if account_holder != withdrawal_account["owner_id"]:
            logger.warning(
                "Customer service (%s) attempted to withdraw from %s "
                "owned by %s",
                account_holder,
                withdrawal_account["account_number"],
                withdrawal_account["owner_id"],
            )
            raise PermissionError("Customer service cannot act on behalf of other owners.")
        return

    # For regular users, must be the account owner
    if user_role == "account_owner":
        if account_holder != withdrawal_account["owner_id"]:
            logger.warning(
                "User %s attempted to withdraw from account owned by %s",
                account_holder,
                withdrawal_account["owner_id"],
            )
            raise PermissionError("Only the account owner can withdraw from this account.")
        return

    # Any other role is not permitted
    logger.warning("Unauthorized role %s for account holder %s", user_role, account_holder)
    raise PermissionError(f"Role '{user_role}' is not authorized to perform transfers.")


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def send_funds(
    account_holder: str,
    user_role: str,
    withdrawal_account: str,
    receiving_account: str,
    fund_amount: float,
) -> str:
    """
    Transfer money from `withdrawal_account` to `receiving_account`.

    Parameters
    ----------
    account_holder : str
        The ID of the user initiating the transaction.
    user_role : str
        Role of the user. Must be one of 'account_owner', 'bank_admin',
        or 'customer_service'.
    withdrawal_account : str
        Account number to withdraw funds from.
    receiving_account : str
        Account number to deposit funds into.
    fund_amount : float
        Amount of money to transfer. Must be positive and <= balance.

    Returns
    -------
    str
        Success message confirming the transfer.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    KeyError
        If either account does not exist.
    ValueError
        If the amount is invalid or insufficient funds.
    """
    if fund_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Retrieve account records
    withdrawal_acct = _get_account(withdrawal_account)
    receiving_acct = _get_account(receiving_account)

    # Authorization check
    _authorize(account_holder, user_role, withdrawal_acct)

    # Check sufficient funds
    if withdrawal_acct["balance"] < fund_amount:
        logger.error(
            "Insufficient funds in account %s: requested %.2f, available %.2f",
            withdrawal_account,
            fund_amount,
            withdrawal_acct["balance"],
        )
        raise ValueError("Insufficient funds for the transfer.")

    # Perform the transfer atomically
    withdrawal_acct["balance"] -= fund_amount
    receiving_acct["balance"] += fund_amount

    logger.info(
        "Transferred %.2f from %s (owner: %s) to %s. New balances: "
        "%.2f -> %.2f",
        fund_amount,
        withdrawal_account,
        withdrawal_acct["owner_id"],
        receiving_account,
        withdrawal_acct["balance"] + fund_amount,  # original balance
        receiving_acct["balance"],
    )

    return (
        f"Successfully transferred ${fund_amount:,.2f} from "
        f"{withdrawal_account} to {receiving_account}. "
        f"New balance: ${withdrawal_acct['balance']:,.2f}."
    )


# ----------------------------------------------------------------------
# Example usage (for testing only)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    try:
        msg = send_funds(
            account_holder="user_123",
            user_role="account_owner",
            withdrawal_account="ACC001",
            receiving_account="ACC002",
            fund_amount=200.0,
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")