from decimal import Decimal, InvalidOperation
from typing import Dict

# Example accounts database – in a real system this would come from persistent storage
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user123", "balance": Decimal("1500.00")},
    "ACC2002": {"account_number": "ACC2002", "owner_id": "user456", "balance": Decimal("500.00")},
    # Add more accounts as needed
}

def shift_funds(
    initiator_id: str,
    initiator_role: str,
    withdraw_account: str,
    deposit_account: str,
    transfer_value: float
) -> str:
    """
    Move money from one account to another.

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
        Success message if the transfer is completed.

    Raises
    ------
    PermissionError
        If the user does not have permission to perform the transfer.
    ValueError
        For invalid input values (negative amount, nonexistent accounts, etc.).
    """

    # Convert transfer_value to Decimal for accurate arithmetic
    try:
        amount = Decimal(str(transfer_value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError("Transfer value must be a numeric type.") from exc

    if amount <= 0:
        raise ValueError("Transfer value must be positive.")

    # Retrieve account records
    src = ACCOUNTS_DB.get(withdraw_account)
    dst = ACCOUNTS_DB.get(deposit_account)

    if src is None or dst is None:
        raise ValueError("One or both accounts do not exist.")

    # Authorization logic
    authorized = False

    if initiator_role == "bank_admin":
        # Admin can transfer any accounts
        authorized = True

    elif initiator_role == "customer_service":
        # Customer service can transfer only if both accounts exist
        authorized = True

    elif initiator_role == "account_owner":
        # Owner can transfer only from their own account
        authorized = initiator_id == src["owner_id"]

    if not authorized:
        raise PermissionError("Unauthorized access: insufficient permissions to perform this transfer.")

    # Ensure sufficient funds
    if src["balance"] < amount:
        raise ValueError("Insufficient funds in the withdraw account.")

    # Perform transfer atomically
    src["balance"] -= amount
    dst["balance"] += amount

    return (
        f"Transfer of {amount:.2f} from account {withdraw_account}"
        f" to {deposit_account} completed successfully."
    )