from decimal import Decimal, getcontext
from typing import Dict

# Set decimal precision for monetary calculations
getcontext().prec = 28

# Example accounts database (should be replaced with real data in production)
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC123": {"account_number": "ACC123", "owner_id": "user1", "balance": Decimal("1000.00")},
    "ACC456": {"account_number": "ACC456", "owner_id": "user2", "balance": Decimal("500.00")},
    # Add more accounts as needed
}

def execute_transfer(
    identifier: str,
    role: str,
    source_acc: str,
    destination_acc: str,
    value: float
) -> str:
    """
    Transfer money from source_acc to destination_acc.

    Parameters
    ----------
    identifier : str
        The ID of the individual requesting the transfer.
    role : str
        Role of the requester (e.g., 'account_owner', 'bank_admin', etc.).
    source_acc : str
        Account number to debit.
    destination_acc : str
        Account number to credit.
    value : float
        Amount to transfer.

    Returns
    -------
    str
        Success message with new balances.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    KeyError
        If either account number does not exist in ACCOUNTS_DB.
    ValueError
        If the transfer amount is invalid or insufficient funds.
    """
    # Convert to Decimal for accurate calculations
    try:
        amount = Decimal(str(value))
    except Exception as exc:
        raise ValueError(f"Invalid transfer amount: {value}") from exc

    if amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Retrieve accounts from the database
    try:
        src = ACCOUNTS_DB[source_acc]
        dst = ACCOUNTS_DB[destination_acc]
    except KeyError as exc:
        raise KeyError(f"Account not found: {exc.args[0]}") from exc

    # Authorization logic
    if role == "bank_admin":
        authorized = True
    elif role == "account_owner" and src["owner_id"] == identifier:
        authorized = True
    else:
        authorized = False

    if not authorized:
        raise PermissionError("Unauthorized transfer attempt.")

    # Check sufficient funds
    if src["balance"] < amount:
        raise ValueError("Insufficient funds in source account.")

    # Perform the transfer atomically
    src["balance"] -= amount
    dst["balance"] += amount

    return (
        f"Transfer of {amount:.2f} from {source_acc} to "
        f"{destination_acc} completed successfully.\n"
        f"New balances: {source_acc}: {src['balance']:.2f}, "
        f"{destination_acc}: {dst['balance']:.2f}"
    )