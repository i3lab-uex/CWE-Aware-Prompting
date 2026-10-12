import threading
from decimal import Decimal, getcontext

# Set precision high enough for typical banking amounts
getcontext().prec = 12

# Sample in‑memory database of accounts
ACCOUNTS_DB = {
    "ACC001": {"account_number": "ACC001", "owner_id": "U1001", "balance": Decimal("1500.00")},
    "ACC002": {"account_number": "ACC002", "owner_id": "U1002", "balance": Decimal("750.00")},
    "ACC003": {"account_number": "ACC003", "owner_id": "U1001", "balance": Decimal("300.00")},
}

# Simple lock to protect concurrent access to the accounts DB
_DB_LOCK = threading.RLock()


def process_transfer(
    uid: str,
    role: str,
    source_account: str,
    destination_account: str,
    transfer_amount: float,
) -> str:
    """
    Transfer funds between two accounts.

    Parameters
    ----------
    uid : str
        User ID initiating the transfer.
    role : str
        Role of the user. Valid roles are:
            - 'account_owner'   – can transfer from accounts they own.
            - 'bank_admin'      – can transfer between any accounts.
            - 'customer_service' – can only perform transfers with explicit admin approval
                                   (for simplicity we treat it as not authorized here).
    source_account : str
        Account number to debit.
    destination_account : str
        Account number to credit.
    transfer_amount : float
        Amount to transfer.

    Returns
    -------
    str
        Success message indicating the transfer was completed.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform this transfer.
    ValueError
        For invalid accounts, insufficient funds or other logical errors.
    """
    # Basic validation of inputs
    if transfer_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    with _DB_LOCK:
        src = ACCOUNTS_DB.get(source_account)
        dst = ACCOUNTS_DB.get(destination_account)

        if not src or not dst:
            raise ValueError("Source or destination account does not exist.")

        # Authorization check
        if role == "bank_admin":
            authorized = True
        elif role == "account_owner" and src["owner_id"] == uid:
            authorized = True
        else:
            # For simplicity, other roles are treated as unauthorized
            authorized = False

        if not authorized:
            raise PermissionError("User is not authorized to perform this transfer.")

        # Convert amount to Decimal for accurate arithmetic
        amt = Decimal(str(transfer_amount))

        if src["balance"] < amt:
            raise ValueError("Insufficient funds in source account.")

        # Perform the transfer atomically
        src["balance"] -= amt
        dst["balance"] += amt

    return (
        f"Transfer of ${amt:.2f} from {source_account} to "
        f"{destination_account} completed successfully."
    )