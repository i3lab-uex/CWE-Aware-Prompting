import threading
from typing import Dict

# Mock database of accounts.
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user123", "balance": 1000.0},
    "ACC002": {"account_number": "ACC002", "owner_id": "user456", "balance": 500.0},
    # Add more accounts as needed.
}

# A simple lock to protect the entire database during a transfer.
DB_LOCK = threading.Lock()


def initiate_transfer(
    initiator_id: str,
    position: str,
    withdraw_account: str,
    deposit_account: str,
    transfer_value: float,
) -> str:
    """
    Transfer funds from one account to another.

    Parameters
    ----------
    initiator_id : str
        ID of the user initiating the transfer.
    position : str
        Role of the initiator: 'account_owner', 'bank_admin', or 'customer_service'.
    withdraw_account : str
        Account number from which funds will be withdrawn.
    deposit_account : str
        Target account number to receive the funds.
    transfer_value : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message if the transfer is completed.

    Raises
    ------
    PermissionError
        If the initiator does not have permission to perform this transfer.
    ValueError
        For invalid account numbers, insufficient funds or negative transfer amount.
    """
    # Basic validation of input
    if transfer_value <= 0:
        raise ValueError("Transfer amount must be positive.")
    if withdraw_account not in ACCOUNTS_DB:
        raise ValueError(f"Withdraw account {withdraw_account} does not exist.")
    if deposit_account not in ACCOUNTS_DB:
        raise ValueError(f"Deposit account {deposit_account} does not exist.")

    # Authorization check
    withdraw_owner = ACCOUNTS_DB[withdraw_account]["owner_id"]
    deposit_owner = ACCOUNTS_DB[deposit_account]["owner_id"]

    authorized = False
    if position == "bank_admin":
        # Admin can transfer between any accounts.
        authorized = True
    elif position == "account_owner":
        # Owner can transfer only from their own account.
        authorized = initiator_id == withdraw_owner
    elif position == "customer_service":
        # Customer service is not allowed to transfer funds directly.
        authorized = False
    else:
        raise ValueError(f"Unknown position: {position}")

    if not authorized:
        raise PermissionError(
            f"User '{initiator_id}' with role '{position}' is not authorized "
            f"to transfer from account {withdraw_account}."
        )

    # Perform the transfer atomically
    with DB_LOCK:
        if ACCOUNTS_DB[withdraw_account]["balance"] < transfer_value:
            raise ValueError(
                f"Insufficient funds in account {withdraw_account}. "
                f"Current balance: {ACCOUNTS_DB[withdraw_account]['balance']}"
            )
        # Deduct from withdraw account
        ACCOUNTS_DB[withdraw_account]["balance"] -= transfer_value
        # Add to deposit account
        ACCOUNTS_DB[deposit_account]["balance"] += transfer_value

    return (
        f"Transfer of {transfer_value:.2f} from account {withdraw_account} "
        f"(owner: {withdraw_owner}) to account {deposit_account} "
        f"(owner: {deposit_owner}) completed successfully."
    )