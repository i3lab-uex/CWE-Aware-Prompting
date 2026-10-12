import decimal
from typing import Dict

# Example in‑memory accounts database.
ACCOUNTS_DB: Dict[str, dict] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "USR001", "balance": decimal.Decimal("1500.00")},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "USR002", "balance": decimal.Decimal("3000.00")},
    # Add more accounts as needed
}

# Define which roles are allowed to initiate transfers.
ALLOWED_ROLES = {"account_owner", "bank_admin", "customer_service"}

def fund_transfer(
    u_identifier: str,
    u_role: str,
    account_from: str,
    account_to: str,
    transfer_amount: float
) -> str:
    """
    Transfer funds from one account to another after validating permissions and balances.

    Parameters
    ----------
    u_identifier : str
        Identifier of the individual requesting the transfer.
    u_role : str
        Role held by the individual (e.g., 'account_owner', 'bank_admin', 'customer_service').
    account_from : str
        Account number from which the funds will be removed.
    account_to : str
        Account number where the funds will be deposited.
    transfer_amount : float
        Monetary value to transfer.

    Returns
    -------
    str
        Success message upon completion of the transfer.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    KeyError
        If either account number does not exist in ACCOUNTS_DB.
    ValueError
        If the transfer amount is non‑positive or insufficient funds are available.
    """
    # Validate role
    if u_role not in ALLOWED_ROLES:
        raise PermissionError(f"Role '{u_role}' is not authorized to perform transfers.")

    # Ensure both accounts exist
    try:
        acct_from = ACCOUNTS_DB[account_from]
    except KeyError as e:
        raise KeyError(f"Source account '{account_from}' not found.") from e

    try:
        acct_to = ACCOUNTS_DB[account_to]
    except KeyError as e:
        raise KeyError(f"Destination account '{account_to}' not found.") from e

    # If role is 'account_owner', ensure the user owns the source account
    if u_role == "account_owner" and acct_from["owner_id"] != u_identifier:
        raise PermissionError("Account owner can only transfer from their own account.")

    # Convert amount to Decimal for precise arithmetic
    try:
        amount = decimal.Decimal(str(transfer_amount))
    except (decimal.InvalidOperation, ValueError) as e:
        raise ValueError("Transfer amount must be a valid number.") from e

    if amount <= decimal.Decimal("0"):
        raise ValueError("Transfer amount must be greater than zero.")

    # Check sufficient balance
    if acct_from["balance"] < amount:
        raise ValueError("Insufficient funds in the source account.")

    # Perform transfer atomically
    acct_from["balance"] -= amount
    acct_to["balance"] += amount

    return (
        f"Transfer of {amount:,.2f} from '{account_from}' to '{account_to}' "
        f"completed successfully. New balances: "
        f"{acct_from['balance']:,.2f} (source), {acct_to['balance']:,.2f} (destination)."
    )