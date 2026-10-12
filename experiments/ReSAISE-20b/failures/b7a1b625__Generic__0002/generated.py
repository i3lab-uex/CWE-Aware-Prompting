#!/usr/bin/env python3
"""
Utility for transferring funds between accounts with basic authorization.
"""

from __future__ import annotations

import logging
from typing import Dict, Any

# Setup basic logger for debugging (in a real system use a more robust logging config)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Sample in-memory accounts database. In a real application this would be
# replaced by persistent storage or an ORM.
ACCOUNTS_DB: Dict[str, Dict[str, Any]] = {
    "ACC001": {"account_number": "ACC001", "owner_id": "USR1001", "balance": 5000.00},
    "ACC002": {"account_number": "ACC002", "owner_id": "USR1002", "balance": 3000.00},
    # Add more accounts as needed
}


def execute_transfer(
    employee_id: str,
    role_value: str,
    source_acct: str,
    target_acct: str,
    total_amount: float,
) -> str:
    """
    Transfer money from one account to another after verifying permissions.

    Parameters
    ----------
    employee_id : str
        ID of the user initiating the transfer.
    role_value : str
        Role of the employee (e.g., 'account_owner', 'bank_admin',
        'customer_service').
    source_acct : str
        Account number to withdraw from.
    target_acct : str
        Account number to deposit into.
    total_amount : float
        Amount to transfer.

    Returns
    -------
    str
        Success message confirming the transfer.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform this transfer.
    KeyError
        If either account does not exist in the database.
    ValueError
        If the source account lacks sufficient funds or if the amount is invalid.
    """

    logger.debug(
        "Attempting transfer: %s -> %s, amount=%.2f by employee=%s role=%s",
        source_acct,
        target_acct,
        total_amount,
        employee_id,
        role_value,
    )

    # Basic validation of input
    if total_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Retrieve account data
    try:
        src_account = ACCOUNTS_DB[source_acct]
        tgt_account = ACCOUNTS_DB[target_acct]
    except KeyError as e:
        raise KeyError(f"Account not found: {e.args[0]}") from None

    # Authorization logic
    if role_value == "bank_admin":
        authorized = True  # Admins can transfer any account
    elif role_value == "account_owner":
        authorized = src_account["owner_id"] == employee_id
    elif role_value == "customer_service":
        # For this example, customer service cannot initiate transfers
        authorized = False
    else:
        authorized = False

    if not authorized:
        logger.warning(
            "Unauthorized transfer attempt by %s (%s) from %s",
            employee_id,
            role_value,
            source_acct,
        )
        raise PermissionError("You are not authorized to perform this transfer.")

    # Check sufficient funds
    if src_account["balance"] < total_amount:
        raise ValueError("Insufficient funds in source account.")

    # Perform the transfer
    src_account["balance"] -= total_amount
    tgt_account["balance"] += total_amount

    logger.info(
        "Transfer successful: %.2f from %s to %s. New balances -> Source: %.2f, Target: %.2f",
        total_amount,
        source_acct,
        target_acct,
        src_account["balance"],
        tgt_account["balance"],
    )

    return (
        f"Transfer of ${total_amount:,.2f} from {source_acct} "
        f"to {target_acct} completed successfully."
    )


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         msg = execute_transfer("USR1001", "account_owner", "ACC001", "ACC002", 1500.00)
#         print(msg)
#     except Exception as e:
#         print(f"Error: {e}")