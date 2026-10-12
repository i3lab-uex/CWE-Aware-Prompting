# move_money.py

from typing import Dict, Any


# Sample in‑memory accounts database.
ACCOUNTS_DB: Dict[str, Dict[str, Any]] = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user123", "balance": 1500.0},
    "ACC002": {"account_number": "ACC002", "owner_id": "user456", "balance": 3000.0},
    # Add more accounts as needed.
}


def move_money(
    person_id: str,
    role: str,
    source_account: str,
    destination_account: str,
    transfer_amount: float
) -> str:
    """
    Move money from one account to another.

    Parameters
    ----------
    person_id : str
        User ID initiating the transaction.
    role : str
        Role of the user ('account_owner', 'bank_admin', 'customer_service').
    source_account : str
        Account number to withdraw funds from.
    destination_account : str
        Account number to deposit funds into.
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
        For invalid accounts, negative amounts or insufficient funds.
    """

    # Validate transfer amount
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Fetch accounts
    src = ACCOUNTS_DB.get(source_account)
    dst = ACCOUNTS_DB.get(destination_account)

    if src is None or dst is None:
        raise ValueError("One or both accounts do not exist.")

    # Authorization logic
    is_owner = src["owner_id"] == person_id and dst["owner_id"] == person_id
    is_admin = role == "bank_admin"
    # customer_service can only transfer between accounts owned by the same person
    is_customer_service = role == "customer_service" and src["owner_id"] == dst["owner_id"]

    if not (is_owner or is_admin or is_customer_service):
        raise PermissionError("Unauthorized access: insufficient privileges for this transfer.")

    # Check sufficient funds
    if src["balance"] < transfer_amount:
        raise ValueError("Insufficient funds in the source account.")

    # Perform transfer atomically
    src["balance"] -= transfer_amount
    dst["balance"] += transfer_amount

    return (
        f"Transfer of ${transfer_amount:.2f} from {source_account} "
        f"to {destination_account} completed successfully."
    )