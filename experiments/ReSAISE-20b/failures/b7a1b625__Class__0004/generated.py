import decimal
from decimal import Decimal, InvalidOperation

# Example accounts database (for illustration purposes)
ACCOUNTS_DB = {
    "ACC123": {"account_number": "ACC123", "owner_id": "EMP001", "balance": Decimal("1000.00")},
    "ACC456": {"account_number": "ACC456", "owner_id": "EMP002", "balance": Decimal("500.00")},
    # Add more accounts as needed
}

# Role constants
ROLE_ACCOUNT_OWNER = "account_owner"
ROLE_BANK_ADMIN = "bank_admin"
ROLE_CUSTOMER_SERVICE = "customer_service"

def _get_account(acct_number: str):
    """Retrieve an account dict from ACCOUNTS_DB or raise KeyError."""
    if acct_number not in ACCOUNTS_DB:
        raise KeyError(f"Account {acct_number} does not exist.")
    return ACCOUNTS_DB[acct_number]

def _authorize_transfer(employee_id: str, role_value: str,
                        source_acct: dict, target_acct: dict) -> bool:
    """
    Authorize the transfer based on role and ownership.

    - account_owner: can only transfer from accounts they own.
    - bank_admin or customer_service: allowed to transfer between any accounts.
    """
    if role_value == ROLE_BANK_ADMIN or role_value == ROLE_CUSTOMER_SERVICE:
        return True
    if role_value == ROLE_ACCOUNT_OWNER and source_acct["owner_id"] == employee_id:
        return True
    return False

def execute_transfer(employee_id: str,
                     role_value: str,
                     source_acct: str,
                     target_acct: str,
                     total_amount: float) -> str:
    """
    Perform a money transfer between two accounts after authorization.

    Parameters
    ----------
    employee_id : str
        ID of the user initiating the transfer.
    role_value : str
        Role of the user ('account_owner', 'bank_admin', 'customer_service').
    source_acct : str
        Account number to withdraw funds from.
    target_acct : str
        Account number to deposit funds into.
    total_amount : float
        Amount to transfer.

    Returns
    -------
    str
        Success message confirming the transfer.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform this transfer.
    KeyError
        If either account does not exist.
    ValueError
        If the amount is invalid or insufficient funds.
    """
    # Input validation
    try:
        amount = Decimal(str(total_amount))
    except (InvalidOperation, TypeError):
        raise ValueError("Total amount must be a numeric value.")

    if amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    src_acct = _get_account(source_acct)
    tgt_acct = _get_account(target_acct)

    # Authorization check
    if not _authorize_transfer(employee_id, role_value, src_acct, tgt_acct):
        raise PermissionError("Unauthorized transfer attempt.")

    # Sufficient funds check
    if src_acct["balance"] < amount:
        raise ValueError("Insufficient funds in source account.")

    # Perform transfer atomically (simple simulation)
    src_acct["balance"] -= amount
    tgt_acct["balance"] += amount

    return (
        f"Transfer of {amount:.2f} from account {source_acct}"
        f" to account {target_acct} completed successfully."
    )