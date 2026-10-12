from decimal import Decimal, getcontext
from typing import Dict

# Set precision high enough for money operations
getcontext().prec = 28

# Example in‑memory database of accounts
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user123", "balance": Decimal("1000.00")},
    "ACC002": {"account_number": "ACC002", "owner_id": "user456", "balance": Decimal("500.00")},
    # ... add more accounts as needed
}

def initiate_transfer(
    initiator_id: str,
    position: str,
    withdraw_account: str,
    deposit_account: str,
    transfer_value: float
) -> str:
    """
    Transfer funds between two accounts after proper authorization.

    Parameters
    ----------
    initiator_id : str
        ID of the user initiating the transfer.
    position : str
        Role of the initiator (e.g., 'account_owner', 'bank_admin', 'customer_service').
    withdraw_account : str
        Account number from which funds will be withdrawn.
    deposit_account : str
        Target account where funds will be deposited.
    transfer_value : float
        Amount to transfer.

    Returns
    -------
    str
        Success message upon completion.

    Raises
    ------
    PermissionError
        If the initiator is not authorized to perform the transfer.
    ValueError
        If accounts are missing or insufficient funds.
    """
    # Convert to Decimal for accurate arithmetic
    amount = Decimal(str(transfer_value))

    # Basic validation of accounts
    if withdraw_account not in ACCOUNTS_DB:
        raise ValueError(f"Withdraw account '{withdraw_account}' does not exist.")
    if deposit_account not in ACCOUNTS_DB:
        raise ValueError(f"Deposit account '{deposit_account}' does not exist.")

    withdraw_acct = ACCOUNTS_DB[withdraw_account]
    deposit_acct = ACCOUNTS_DB[deposit_account]

    # Authorization logic
    is_owner = initiator_id == withdraw_acct["owner_id"]
    is_admin = position.lower() == "bank_admin"

    if not (is_owner or is_admin):
        raise PermissionError(
            f"User '{initiator_id}' with role '{position}' is not authorized to transfer from account {withdraw_account}."
        )

    # Sufficient funds check
    if withdraw_acct["balance"] < amount:
        raise ValueError(f"Insufficient funds in account {withdraw_account}.")

    # Perform the transfer atomically
    withdraw_acct["balance"] -= amount
    deposit_acct["balance"] += amount

    return (
        f"Transfer of {amount:.2f} from account {withdraw_account} to "
        f"{deposit_account} completed successfully."
    )