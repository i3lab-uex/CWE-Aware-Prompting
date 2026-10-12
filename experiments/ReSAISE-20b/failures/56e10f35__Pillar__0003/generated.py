# -*- coding: utf-8 -*-

"""
Banking transfer module.

This module implements a secure money transfer function between accounts.
It enforces proper access control to prevent unauthorized fund movements
(CWE-284: Improper Access Control).

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import logging
from typing import Dict, Any

# Configure basic logging for debugging and audit purposes
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# Sample in-memory accounts database.
# In a real application, this would be replaced by persistent storage
ACCOUNTS_DB: Dict[str, Dict[str, Any]] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user123", "balance": 5000.00},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "user456", "balance": 3000.00},
    # Add more accounts as needed
}


def _get_account(account_number: str) -> Dict[str, Any]:
    """
    Retrieve an account from the database.

    Raises:
        KeyError: If the account does not exist.
    """
    try:
        return ACCOUNTS_DB[account_number]
    except KeyError as exc:
        logging.error("Account %s not found.", account_number)
        raise KeyError(f"Account {account_number} does not exist.") from exc


def _authorize(
    initiator_id: str,
    position: str,
    withdraw_account: Dict[str, Any],
) -> None:
    """
    Verify that the initiator is authorized to perform a withdrawal.

    Raises:
        PermissionError: If authorization fails.
    """
    # Admins can transfer from any account
    if position == "bank_admin":
        return

    # Account owners can transfer from their own account
    if position == "account_owner" and withdraw_account["owner_id"] == initiator_id:
        return

    # Customer service can only transfer if explicitly allowed
    if position == "customer_service":
        # For this example, we disallow customer service from transferring
        logging.warning(
            "Customer service %s attempted unauthorized transfer from account %s.",
            initiator_id,
            withdraw_account["account_number"],
        )
        raise PermissionError("Customer service is not authorized to initiate transfers.")

    # Any other case is unauthorized
    logging.warning(
        "Unauthorized transfer attempt by %s (%s) on account %s.",
        initiator_id,
        position,
        withdraw_account["account_number"],
    )
    raise PermissionError("User is not authorized to initiate this transfer.")


def _validate_amount(
    withdraw_account: Dict[str, Any],
    deposit_account: Dict[str, Any],
    amount: float,
) -> None:
    """
    Validate that the transfer amount is positive and funds are sufficient.

    Raises:
        ValueError: If validation fails.
    """
    if amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    if withdraw_account["balance"] < amount:
        raise ValueError("Insufficient funds in the withdrawal account.")


def initiate_transfer(
    initiator_id: str,
    position: str,
    withdraw_account_number: str,
    deposit_account_number: str,
    transfer_value: float,
) -> str:
    """
    Transfer funds between two accounts after performing authorization checks.

    Parameters
    ----------
    initiator_id : str
        ID of the user initiating the transfer.
    position : str
        Role of the initiator (e.g., 'account_owner', 'bank_admin',
        'customer_service').
    withdraw_account_number : str
        Account number to withdraw funds from.
    deposit_account_number : str
        Target account to deposit funds into.
    transfer_value : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message confirming the transfer.

    Raises
    ------
    PermissionError
        If the initiator is not authorized to perform this transfer.
    KeyError
        If either account does not exist.
    ValueError
        For invalid amounts or insufficient funds.
    """
    # Retrieve accounts safely; raise KeyError if not found
    withdraw_account = _get_account(withdraw_account_number)
    deposit_account = _get_account(deposit_account_number)

    # Authorization check
    _authorize(initiator_id, position, withdraw_account)

    # Validate amount and balances
    _validate_amount(withdraw_account, deposit_account, transfer_value)

    # Perform the transfer atomically
    withdraw_account["balance"] -= transfer_value
    deposit_account["balance"] += transfer_value

    # Log the transaction for audit purposes
    logging.info(
        "Transfer of %.2f from %s to %s completed by %s (%s).",
        transfer_value,
        withdraw_account_number,
        deposit_account_number,
        initiator_id,
        position,
    )

    return (
        f"Transfer of ${transfer_value:,.2f} from account "
        f"{withdraw_account_number} to {deposit_account_number} completed successfully."
    )


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         msg = initiate_transfer(
#             initiator_id="user123",
#             position="account_owner",
#             withdraw_account_number="ACC1001",
#             deposit_account_number="ACC1002",
#             transfer_value=1500.00,
#         )
#         print(msg)
#     except Exception as exc:
#         print(f"Transfer failed: {exc}")