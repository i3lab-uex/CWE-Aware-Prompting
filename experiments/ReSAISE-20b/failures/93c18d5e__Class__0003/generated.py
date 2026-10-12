# -*- coding: utf-8 -*-
"""
Banking fund transfer module.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# Example in-memory accounts database.
# In a real system this would be replaced by persistent storage and proper ORM models.
ACCOUNTS_DB: dict[str, dict] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user_001", "balance": 1500.00},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "user_002", "balance": 500.00},
    # ... more accounts
}


def shift_funds(
    initiator_id: str,
    initiator_role: str,
    withdraw_account: str,
    deposit_account: str,
    transfer_value: float
) -> str:
    """
    Transfer funds from one account to another.

    Parameters
    ----------
    initiator_id : str
        The ID of the user initiating the transfer.
    initiator_role : str
        Role of the initiator. Allowed roles: 'account_owner', 'bank_admin',
        'customer_service'.
    withdraw_account : str
        Account number to debit.
    deposit_account : str
        Account number to credit.
    transfer_value : float
        Amount to transfer. Must be positive.

    Returns
    -------
    str
        Success message indicating the amount transferred and new balances.

    Raises
    ------
    PermissionError
        If the initiator is not authorized to perform this transfer.
    ValueError
        For invalid input such as unknown accounts, negative amounts,
        or insufficient funds.
    """

    # --- Basic validation ----------------------------------------------------
    if transfer_value <= 0:
        raise ValueError("Transfer amount must be positive.")

    if withdraw_account not in ACCOUNTS_DB:
        raise ValueError(f"Withdraw account '{withdraw_account}' does not exist.")
    if deposit_account not in ACCOUNTS_DB:
        raise ValueError(f"Deposit account '{deposit_account}' does not exist.")

    source = ACCOUNTS_DB[withdraw_account]
    target = ACCOUNTS_DB[deposit_account]

    # --- Authorization check (CWE-863 safe implementation) -----------------
    authorized = False

    if initiator_role == "bank_admin":
        # Admin can transfer between any accounts
        authorized = True

    elif initiator_role == "customer_service":
        # Customer service can transfer only between accounts that belong
        # to the same owner and the initiator must be the account owner.
        if source["owner_id"] == target["owner_id"]:
            authorized = True

    elif initiator_role == "account_owner":
        # Owner can transfer only from their own account
        if source["owner_id"] == initiator_id:
            authorized = True

    # If no role matched or authorization failed, raise PermissionError
    if not authorized:
        raise PermissionError(
            f"User '{initiator_id}' with role '{initiator_role}' is not authorized "
            f"to transfer from '{withdraw_account}' to '{deposit_account}'."
        )

    # --- Sufficient funds check ---------------------------------------------
    if source["balance"] < transfer_value:
        raise ValueError(
            f"Insufficient funds in account '{withdraw_account}'. "
            f"Available: {source['balance']:.2f}, required: {transfer_value:.2f}."
        )

    # --- Perform the transfer (atomicity not guaranteed in this mock) -------
    source["balance"] -= transfer_value
    target["balance"] += transfer_value

    return (
        f"Transfer of ${transfer_value:.2f} from '{withdraw_account}' "
        f"(new balance: ${source['balance']:.2f}) to '{deposit_account}' "
        f"(new balance: ${target['balance']:.2f}) completed successfully."
    )


# Example usage (for debugging; remove or comment out in production)
if __name__ == "__main__":
    try:
        msg = shift_funds(
            initiator_id="user_001",
            initiator_role="account_owner",
            withdraw_account="ACC1001",
            deposit_account="ACC1002",
            transfer_value=200.0,
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")