import threading
from typing import Dict

# Simulated accounts database
ACCOUNTS_DB: Dict[str, dict] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user123", "balance": 1500.0},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "user456", "balance": 2500.0},
    # Add more accounts as needed
}

# Simple lock to ensure thread‑safe balance updates
db_lock = threading.Lock()


def initiate_transfer(
    initiator_id: str,
    position: str,
    withdraw_account: str,
    deposit_account: str,
    transfer_value: float
) -> str:
    """
    Transfer money from one account to another if the initiator is authorized.

    Parameters
    ----------
    initiator_id : str
        ID of the user initiating the transfer.
    position : str
        Role of the initiator (e.g., 'account_owner', 'bank_admin',
        'customer_service').
    withdraw_account : str
        Account number to debit.
    deposit_account : str
        Account number to credit.
    transfer_value : float
        Amount to transfer.

    Returns
    -------
    str
        Success message if the transfer was completed.

    Raises
    ------
    PermissionError
        If the initiator is not authorized to perform this transfer.
    KeyError
        If either account does not exist in the database.
    ValueError
        If the transfer_value is non‑positive or insufficient funds exist.
    """
    # Basic input validation
    if transfer_value <= 0:
        raise ValueError("Transfer amount must be positive")

    # Retrieve accounts
    try:
        withdraw_acc = ACCOUNTS_DB[withdraw_account]
        deposit_acc = ACCOUNTS_DB[deposit_account]
    except KeyError as e:
        raise KeyError(f"Account {e.args[0]} does not exist") from None

    # Authorization check
    authorized = False
    if position == "bank_admin":
        authorized = True
    elif position == "account_owner" and withdraw_acc["owner_id"] == initiator_id:
        authorized = True
    elif position == "customer_service":
        # Customer service can transfer only within the same bank if
        # both accounts belong to the same system (here we assume all are)
        authorized = True

    if not authorized:
        raise PermissionError("Unauthorized access for transfer")

    # Perform the transfer atomically
    with db_lock:
        if withdraw_acc["balance"] < transfer_value:
            raise ValueError("Insufficient funds in the withdrawal account")

        # Update balances
        withdraw_acc["balance"] -= transfer_value
        deposit_acc["balance"] += transfer_value

    return (
        f"Transfer of ${transfer_value:,.2f} from {withdraw_account} "
        f"to {deposit_account} completed successfully."
    )


# Example usage (uncomment to test):
# try:
#     msg = initiate_transfer(
#         initiator_id="user123",
#         position="account_owner",
#         withdraw_account="ACC1001",
#         deposit_account="ACC1002",
#         transfer_value=200.0
#     )
#     print(msg)
# except Exception as e:
#     print(f"Error: {e}")