import threading
from decimal import Decimal, InvalidOperation

# Example in-memory accounts database
ACCOUNTS_DB = {
    "ACC123": {"account_number": "ACC123", "owner_id": "user_1", "balance": Decimal("1000.00")},
    "ACC456": {"account_number": "ACC456", "owner_id": "user_2", "balance": Decimal("500.00")},
    # Add more accounts as needed
}

# Global lock to serialize access to the accounts database
_ACCOUNTS_LOCK = threading.Lock()


def process_transfer(
    uid: str,
    role: str,
    source_account: str,
    destination_account: str,
    transfer_amount: float,
) -> str:
    """
    Transfer money from one account to another.

    Parameters
    ----------
    uid : str
        ID of the user initiating the transfer.
    role : str
        Role of the user. Allowed values: 'account_owner', 'bank_admin'.
    source_account : str
        Account number to withdraw funds from.
    destination_account : str
        Account number to credit funds to.
    transfer_amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message if the transfer is completed.

    Raises
    ------
    PermissionError
        If the user does not have permission to perform this transfer.
    ValueError
        If input validation fails (non‑existent accounts, insufficient funds,
        negative amount, etc.).
    """

    # Basic input validation
    if role not in {"account_owner", "bank_admin"}:
        raise ValueError(f"Unsupported role: {role}")

    try:
        amount = Decimal(str(transfer_amount))
    except (InvalidOperation, ValueError):
        raise ValueError("Transfer amount must be a numeric value.")

    if amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    with _ACCOUNTS_LOCK:  # Ensure atomic read‑modify‑write
        src = ACCOUNTS_DB.get(source_account)
        dst = ACCOUNTS_DB.get(destination_account)

        if src is None:
            raise ValueError(f"Source account '{source_account}' does not exist.")
        if dst is None:
            raise ValueError(f"Destination account '{destination_account}' does not exist.")

        # Authorization checks
        if role == "account_owner":
            if src["owner_id"] != uid:
                raise PermissionError("User is not the owner of the source account.")
        # bank_admin can transfer any accounts

        if src["balance"] < amount:
            raise ValueError("Insufficient funds in the source account.")

        # Perform transfer
        src["balance"] -= amount
        dst["balance"] += amount

    return (
        f"Transfer of {amount:.2f} from {source_account} to "
        f"{destination_account} completed successfully."
    )