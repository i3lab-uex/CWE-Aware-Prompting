from decimal import Decimal, InvalidOperation
from typing import Dict

# Sample in‑memory accounts database
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user123", "balance": Decimal("1500.00")},
    "ACC002": {"account_number": "ACC002", "owner_id": "user456", "balance": Decimal("500.00")},
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
        User ID initiating the transaction.
    initiator_role : str
        Role of the user (e.g., 'account_owner', 'bank_admin',
        or 'customer_service').
    withdraw_account : str
        Account number to withdraw funds from.
    deposit_account : str
        Account number to deposit funds into.
    transfer_value : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message if the transfer is performed.
    
    Raises
    ------
    PermissionError
        If the initiator does not have permission to perform the transfer.
    KeyError
        If either account number is missing from ACCOUNTS_DB.
    ValueError
        If the transfer_value is not positive or insufficient funds.
    """
    # Validate accounts exist
    try:
        src = ACCOUNTS_DB[withdraw_account]
        dst = ACCOUNTS_DB[deposit_account]
    except KeyError as exc:
        raise KeyError(f"Account not found: {exc.args[0]}") from None

    # Authorization check
    authorized = False
    if initiator_role == "bank_admin":
        authorized = True
    elif initiator_role == "account_owner" and src["owner_id"] == initiator_id:
        authorized = True
    # Other roles are not permitted to move funds directly

    if not authorized:
        raise PermissionError("Unauthorized access: insufficient permissions for fund transfer.")

    # Convert to Decimal for accurate arithmetic
    try:
        amount = Decimal(str(transfer_value))
    except InvalidOperation:
        raise ValueError("Transfer value must be a numeric type.")

    if amount <= 0:
        raise ValueError("Transfer amount must be positive.")
    if src["balance"] < amount:
        raise ValueError("Insufficient funds in the source account.")

    # Perform transfer atomically
    src["balance"] -= amount
    dst["balance"] += amount

    return (
        f"Transfer of {amount:.2f} from {withdraw_account} to "
        f"{deposit_account} completed successfully."
    )