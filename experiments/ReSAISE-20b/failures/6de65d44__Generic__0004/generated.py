import threading
from typing import Dict

# Example in-memory accounts database
ACCOUNTS_DB: Dict[str, dict] = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user123", "balance": 1500.0},
    "ACC002": {"account_number": "ACC002", "owner_id": "user456", "balance": 2000.0},
    # Add more accounts as needed
}

# Global lock to simulate atomic updates in a multi‑threaded environment
_db_lock = threading.Lock()


def move_money(
    person_id: str,
    role: str,
    source_account: str,
    destination_account: str,
    transfer_amount: float,
) -> str:
    """
    Move money from `source_account` to `destination_account`.

    Parameters
    ----------
    person_id : str
        ID of the user initiating the transfer.
    role : str
        Role of the user: 'account_owner', 'bank_admin', or 'customer_service'.
    source_account : str
        Account number to withdraw from.
    destination_account : str
        Account number to deposit into.
    transfer_amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message if the transfer succeeded.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform this transfer.
    ValueError
        For invalid accounts, insufficient funds or negative amounts.
    """
    # Basic input validation
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    with _db_lock:  # Ensure atomicity
        src = ACCOUNTS_DB.get(source_account)
        dst = ACCOUNTS_DB.get(destination_account)

        if src is None or dst is None:
            raise ValueError("Source or destination account does not exist.")

        # Authorization logic
        if role == "account_owner":
            if src["owner_id"] != person_id:
                raise PermissionError("Account owner can only transfer from their own account.")
        elif role == "bank_admin":
            # Admins have full privileges
            pass
        else:
            raise PermissionError("Unauthorized role for transferring money.")

        # Check sufficient funds
        if src["balance"] < transfer_amount:
            raise ValueError("Insufficient funds in source account.")

        # Perform the transfer
        src["balance"] -= transfer_amount
        dst["balance"] += transfer_amount

    return (
        f"Transfer of {transfer_amount:.2f} from '{source_account}' "
        f"to '{destination_account}' completed successfully."
    )