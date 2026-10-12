import datetime
from typing import Dict

# Example accounts database; in a real system this would be replaced by persistent storage
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC123": {"account_number": "ACC123", "owner_id": "user_1", "balance": 5000.0},
    "ACC456": {"account_number": "ACC456", "owner_id": "user_2", "balance": 3000.0},
    # ... other accounts ...
}

def initiate_transfer(
    initiator_id: str,
    position: str,
    withdraw_account: str,
    deposit_account: str,
    transfer_value: float
) -> str:
    """
    Transfer money from withdraw_account to deposit_account.

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
        Success message confirming the transfer.

    Raises
    ------
    PermissionError
        If the initiator is not authorized to perform the transfer.
    KeyError
        If either account does not exist in ACCOUNTS_DB.
    ValueError
        If the transfer_value is non‑positive or insufficient funds.
    """
    # Validate input amounts
    if transfer_value <= 0:
        raise ValueError("Transfer amount must be positive")

    # Retrieve account records
    try:
        withdraw_acc = ACCOUNTS_DB[withdraw_account]
        deposit_acc = ACCOUNTS_DB[deposit_account]
    except KeyError as exc:
        raise KeyError(f"Account not found: {exc.args[0]}") from None

    # Authorization check
    authorized = False
    if position == "bank_admin":
        authorized = True  # admins can transfer any account
    elif position == "account_owner" and withdraw_acc["owner_id"] == initiator_id:
        authorized = True  # owners can transfer from their own account
    elif position == "customer_service" and withdraw_acc["owner_id"] == initiator_id:
        # Allow customer service to transfer only from the customer's account
        authorized = True

    if not authorized:
        raise PermissionError(
            f"User '{initiator_id}' with role '{position}' is not authorized to transfer from account {withdraw_account}"
        )

    # Check sufficient funds
    if withdraw_acc["balance"] < transfer_value:
        raise ValueError("Insufficient funds in the withdrawal account")

    # Perform the transfer atomically (simplified for this example)
    withdraw_acc["balance"] -= transfer_value
    deposit_acc["balance"] += transfer_value

    # Record the transaction (in a real system this would be logged)
    timestamp = datetime.datetime.utcnow().isoformat()
    # For demonstration, we simply return a confirmation message
    return (
        f"Transfer of ${transfer_value:,.2f} from {withdraw_account} "
        f"to {deposit_account} completed successfully on {timestamp}."
    )