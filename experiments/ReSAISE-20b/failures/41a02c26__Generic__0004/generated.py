import decimal
from typing import Dict

# Example accounts database. In a real system this would be replaced by a secure datastore.
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC123": {"account_number": "ACC123", "owner_id": "user1", "balance": decimal.Decimal("1000.00")},
    "ACC456": {"account_number": "ACC456", "owner_id": "user2", "balance": decimal.Decimal("500.00")},
    # Add more accounts as needed
}

# Allowed roles for initiating a transfer and the required ownership check
ALLOWED_ROLES = {"account_owner", "bank_admin", "customer_service"}


def process_transfer(
    uid: str,
    role: str,
    source_account: str,
    destination_account: str,
    transfer_amount: float,
) -> str:
    """
    Transfer money from source_account to destination_account.

    Parameters
    ----------
    uid : str
        User ID initiating the transfer.
    role : str
        Role of the user ('account_owner', 'bank_admin', 'customer_service').
    source_account : str
        Account number to withdraw funds from.
    destination_account : str
        Account number to credit funds to.
    transfer_amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message confirming the transfer.

    Raises
    ------
    PermissionError
        If user is not authorized to perform the transfer.
    ValueError
        For invalid account numbers, insufficient funds, or negative amount.
    """
    # Validate role
    if role not in ALLOWED_ROLES:
        raise PermissionError(f"Role '{role}' is not authorized to perform transfers.")

    # Validate accounts exist
    src = ACCOUNTS_DB.get(source_account)
    dst = ACCOUNTS_DB.get(destination_account)

    if src is None:
        raise ValueError(f"Source account '{source_account}' does not exist.")
    if dst is None:
        raise ValueError(f"Destination account '{destination_account}' does not exist.")

    # Convert transfer amount to Decimal for precision
    try:
        amount = decimal.Decimal(str(transfer_amount))
    except (decimal.InvalidOperation, TypeError):
        raise ValueError("Transfer amount must be a numeric value.")

    if amount <= 0:
        raise ValueError("Transfer amount must be greater than zero.")

    # Ownership check: only account owners or privileged roles can transfer
    if role == "account_owner" and uid != src["owner_id"]:
        raise PermissionError("Account owner can only transfer from their own account.")

    # Check sufficient funds
    if src["balance"] < amount:
        raise ValueError("Insufficient funds in source account.")

    # Perform the transfer atomically (simplified for this example)
    src["balance"] -= amount
    dst["balance"] += amount

    return (
        f"Transfer of {amount:.2f} from account '{source_account}' "
        f"to account '{destination_account}' completed successfully."
    )