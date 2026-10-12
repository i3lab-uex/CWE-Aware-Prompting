import threading
from typing import Dict

# Example accounts database
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC123": {"account_number": "ACC123", "owner_id": "user_1", "balance": 1000.0},
    "ACC456": {"account_number": "ACC456", "owner_id": "user_2", "balance": 500.0},
    # ... other accounts
}

# Lock to ensure atomic updates across the entire DB
DB_LOCK = threading.Lock()


def execute_transfer(
    identifier: str,
    role: str,
    source_acc: str,
    destination_acc: str,
    value: float
) -> str:
    """
    Transfer money between two accounts.

    Parameters
    ----------
    identifier : str
        Identifier of the individual requesting the transfer.
    role : str
        Role held by the individual. Allowed roles: 'account_owner', 'bank_admin',
        'customer_service'.
    source_acc : str
        Account number to debit.
    destination_acc : str
        Account number to credit.
    value : float
        Amount to transfer.

    Returns
    -------
    str
        Success message upon completion.

    Raises
    ------
    PermissionError
        If the caller is not authorized to perform this transfer.
    ValueError
        For invalid account numbers or insufficient funds.
    """

    # Basic validation
    if value <= 0:
        raise ValueError("Transfer amount must be positive")

    with DB_LOCK:  # Ensure consistency
        src = ACCOUNTS_DB.get(source_acc)
        dst = ACCOUNTS_DB.get(destination_acc)

        if src is None or dst is None:
            raise ValueError("One or both account numbers are invalid")

        # Authorization logic
        if role == "bank_admin":
            authorized = True
        elif role == "customer_service":
            # Customer service can transfer only between accounts of the same user
            authorized = src["owner_id"] == dst["owner_id"]
        elif role == "account_owner":
            authorized = identifier == src["owner_id"] and identifier == dst["owner_id"]
        else:
            authorized = False

        if not authorized:
            raise PermissionError("Unauthorized transfer attempt")

        # Check sufficient funds
        if src["balance"] < value:
            raise ValueError("Insufficient funds in source account")

        # Perform transfer
        src["balance"] -= value
        dst["balance"] += value

    return (
        f"Transfer of ${value:,.2f} from {source_acc} to {destination_acc} "
        f"completed successfully."
    )