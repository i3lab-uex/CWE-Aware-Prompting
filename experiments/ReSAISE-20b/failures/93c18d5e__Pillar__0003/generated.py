from decimal import Decimal, InvalidOperation
from typing import Dict

# Sample accounts database structure
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user123", "balance": Decimal("1000.00")},
    "ACC002": {"account_number": "ACC002", "owner_id": "user456", "balance": Decimal("500.00")},
    # Add more accounts as needed
}


def shift_funds(
    initiator_id: str,
    initiator_role: str,
    withdraw_account: str,
    deposit_account: str,
    transfer_value: float,
) -> str:
    """
    Transfer money from one account to another.

    Parameters
    ----------
    initiator_id : str
        ID of the user initiating the transfer.
    initiator_role : str
        Role of the user: 'account_owner', 'bank_admin', or 'customer_service'.
    withdraw_account : str
        Account number to withdraw from.
    deposit_account : str
        Account number to deposit into.
    transfer_value : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message on successful transfer.

    Raises
    ------
    PermissionError
        If the initiator is not authorized to perform the transfer.
    ValueError
        For invalid accounts, insufficient funds, or other logical errors.
    """

    # Validate transfer amount
    try:
        amount = Decimal(str(transfer_value)).quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"Invalid transfer amount: {transfer_value}") from exc

    if amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Ensure both accounts exist
    if withdraw_account not in ACCOUNTS_DB:
        raise ValueError(f"Withdraw account {withdraw_account} does not exist.")
    if deposit_account not in ACCOUNTS_DB:
        raise ValueError(f"Deposit account {deposit_account} does not exist.")

    # Authorization check
    withdraw_info = ACCOUNTS_DB[withdraw_account]
    deposit_info = ACCOUNTS_DB[deposit_account]

    # Only account owners or bank admins can initiate transfers
    authorized = False
    if initiator_role == "bank_admin":
        authorized = True
    elif initiator_role == "account_owner" and initiator_id == withdraw_info["owner_id"]:
        authorized = True
    else:
        # Customer service and other roles are not allowed to transfer funds directly
        authorized = False

    if not authorized:
        raise PermissionError(
            f"User {initiator_id} with role '{initiator_role}' is not authorized "
            "to transfer funds from account {withdraw_account}."
        )

    # Ensure sufficient balance
    if withdraw_info["balance"] < amount:
        raise ValueError(
            f"Insufficient funds in account {withdraw_account}. "
            f"Available: {withdraw_info['balance']}, required: {amount}"
        )

    # Perform the transfer atomically
    withdraw_info["balance"] -= amount
    deposit_info["balance"] += amount

    return (
        f"Transfer of {amount} from account {withdraw_account} "
        f"to account {deposit_account} completed successfully."
    )