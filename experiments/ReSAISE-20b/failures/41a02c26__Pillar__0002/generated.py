import threading
from typing import Dict

# ------------------------------------------------------------------
# Mock database of accounts.
# Each account is a dict with keys: 'account_number', 'owner_id', 'balance'.
# In a real system this would be replaced by a persistent store.
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC123": {"account_number": "ACC123", "owner_id": "user1", "balance": 1000.0},
    "ACC456": {"account_number": "ACC456", "owner_id": "user2", "balance": 500.0},
    # ... additional accounts ...
}

# A lock to protect concurrent access to the account balances.
_db_lock = threading.Lock()


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
        ID of the user initiating the transfer.
    role : str
        Role of the user (e.g., 'account_owner', 'bank_admin', 'customer_service').
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
        If the user is not authorized to perform this transfer.
    ValueError
        If accounts are missing, amount invalid or insufficient funds.
    """
    # Validate input parameters
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    with _db_lock:
        src = ACCOUNTS_DB.get(source_account)
        dst = ACCOUNTS_DB.get(destination_account)

        if src is None or dst is None:
            raise ValueError("Source or destination account does not exist.")

        # Authorization check
        authorized = False

        if role == "account_owner" and src["owner_id"] == uid:
            authorized = True
        elif role in {"bank_admin", "customer_service"}:
            # Admins and customer service can transfer any funds,
            # but we still enforce that the source account has sufficient balance.
            authorized = True

        if not authorized:
            raise PermissionError(
                f"User '{uid}' with role '{role}' is not authorized to transfer from account {source_account}."
            )

        # Sufficient balance check
        if src["balance"] < transfer_amount:
            raise ValueError(
                f"Insufficient funds in source account {source_account}. "
                f"Available: {src['balance']}, Required: {transfer_amount}."
            )

        # Perform the transfer atomically
        src["balance"] -= transfer_amount
        dst["balance"] += transfer_amount

    # Return a clear confirmation message
    return (
        f"Transfer of {transfer_amount:.2f} from account {source_account} "
        f"to account {destination_account} completed successfully."
    )