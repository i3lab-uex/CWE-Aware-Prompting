# -*- coding: utf-8 -*-

from typing import Dict

# Sample accounts database. In a real system this would be replaced by persistent storage.
ACCOUNTS_DB: Dict[str, dict] = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user123", "balance": 1000.0},
    "ACC002": {"account_number": "ACC002", "owner_id": "user456", "balance": 500.0},
    # Add more accounts as needed
}


def transfer_funds(
    user_id: str,
    user_role: str,
    from_account: str,
    to_account: str,
    amount: float,
) -> str:
    """
    Transfer money between two accounts with proper authorization checks.

    Parameters
    ----------
    user_id : str
        ID of the user performing the transfer.
    user_role : str
        Role of the user. Accepted values: 'account_owner', 'bank_admin',
        or 'customer_service'.
    from_account : str
        Account number to transfer funds from.
    to_account : str
        Account number to transfer funds to.
    amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Confirmation message if the transfer succeeds.

    Raises
    ------
    ValueError
        If either account does not exist, the amount is invalid,
        or insufficient funds are available.
    """
    # Basic validation
    if amount <= 0:
        raise ValueError("Transfer amount must be positive")

    src = ACCOUNTS_DB.get(from_account)
    dst = ACCOUNTS_DB.get(to_account)

    if src is None or dst is None:
        raise ValueError("One or both accounts do not exist")

    # Authorization logic
    if user_role == "bank_admin":
        # Bank admins can transfer between any accounts
        authorized = True
    elif user_role == "account_owner":
        # Must own both accounts to transfer between them
        authorized = src["owner_id"] == user_id and dst["owner_id"] == user_id
    elif user_role == "customer_service":
        # Customer service can transfer only from accounts they own
        authorized = src["owner_id"] == user_id
    else:
        # Unknown role – deny by default
        authorized = False

    if not authorized:
        return "Authorization error: insufficient permissions to perform this transfer"

    # Funds check
    if src["balance"] < amount:
        raise ValueError("Insufficient funds in the source account")

    # Perform transfer
    src["balance"] -= amount
    dst["balance"] += amount

    return (
        f"Transfer of ${amount:,.2f} from {from_account} to {to_account} "
        f"completed successfully."
    )