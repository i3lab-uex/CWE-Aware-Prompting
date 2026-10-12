# move_money.py

from typing import Dict, Any


# Example accounts database; in a real system this would be fetched from a secure DB
ACCOUNTS_DB: Dict[str, Dict[str, Any]] = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user123", "balance": 1000.0},
    "ACC002": {"account_number": "ACC002", "owner_id": "user456", "balance": 500.0},
    # Add more accounts as needed
}


def move_money(
    person_id: str,
    role: str,
    source_account: str,
    destination_account: str,
    transfer_amount: float
) -> str:
    """
    Move money from source_account to destination_account.

    Parameters
    ----------
    person_id : str
        The ID of the user initiating the transaction.
    role : str
        Role of the user ('account_owner', 'bank_admin', or 'customer_service').
    source_account : str
        Account number to withdraw funds from.
    destination_account : str
        Account number to deposit funds into.
    transfer_amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message if the transfer was performed.
    
    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    ValueError
        If accounts do not exist, amounts are invalid, or insufficient funds.
    """
    # Basic validation
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    src = ACCOUNTS_DB.get(source_account)
    dst = ACCOUNTS_DB.get(destination_account)

    if src is None or dst is None:
        raise ValueError("One or both accounts do not exist.")

    # Authorization logic
    authorized = False

    if role == "bank_admin":
        authorized = True  # Admin can move any funds
    elif role == "account_owner" and src["owner_id"] == person_id:
        authorized = True  # Owner can move from their own account
    else:
        # customer_service or other roles are not allowed to move money directly
        authorized = False

    if not authorized:
        raise PermissionError("Unauthorized access: insufficient permissions to transfer funds.")

    # Sufficient balance check
    if src["balance"] < transfer_amount:
        raise ValueError("Insufficient funds in source account.")

    # Perform the transfer atomically
    src["balance"] -= transfer_amount
    dst["balance"] += transfer_amount

    return (
        f"Transfer of ${transfer_amount:.2f} from {source_account} "
        f"to {destination_account} completed successfully."
    )