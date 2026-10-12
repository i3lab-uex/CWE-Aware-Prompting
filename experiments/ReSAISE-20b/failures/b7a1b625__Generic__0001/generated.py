import logging
from typing import Dict

# Sample accounts database
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "EMP001", "balance": 5000.0},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "EMP002", "balance": 3000.0},
    # Add more accounts as needed
}

# Configure basic logging for audit purposes
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(user_id)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def _log_action(user_id: str, message: str) -> None:
    """Internal helper to log actions with user context."""
    logging.info(message, extra={"user_id": user_id})


def execute_transfer(
    employee_id: str,
    role_value: str,
    source_acct: str,
    target_acct: str,
    total_amount: float,
) -> str:
    """
    Transfer funds from source_acct to target_acct if authorized.

    Parameters
    ----------
    employee_id : str
        ID of the user initiating the transfer.
    role_value : str
        Role of the user ('account_owner', 'bank_admin', 'customer_service').
    source_acct : str
        Account number to debit.
    target_acct : str
        Account number to credit.
    total_amount : float
        Amount to transfer.

    Returns
    -------
    str
        Success message confirming the transfer.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    KeyError
        If either account does not exist.
    ValueError
        If insufficient funds or invalid amount.
    """
    # Basic validation
    if total_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Fetch accounts
    try:
        src = ACCOUNTS_DB[source_acct]
        tgt = ACCOUNTS_DB[target_acct]
    except KeyError as exc:
        raise KeyError(f"Account not found: {exc}") from None

    # Authorization logic
    authorized = False
    if role_value == "bank_admin":
        authorized = True  # Admins can transfer any account
    elif role_value == "account_owner" and src["owner_id"] == employee_id:
        authorized = True  # Owners can transfer from their own account
    elif role_value == "customer_service":
        # Customer service may only transfer if the employee has explicit approval.
        # For demo purposes, we restrict them to transfers under $1000
        if total_amount <= 1000:
            authorized = True

    if not authorized:
        _log_action(employee_id, f"Unauthorized transfer attempt from {source_acct} to {target_acct}")
        raise PermissionError("You do not have permission to perform this transfer.")

    # Check sufficient funds
    if src["balance"] < total_amount:
        raise ValueError("Insufficient funds in source account.")

    # Perform transfer atomically
    src["balance"] -= total_amount
    tgt["balance"] += total_amount

    # Log the successful transfer
    _log_action(
        employee_id,
        f"Transferred ${total_amount:.2f} from {source_acct} to {target_acct}. "
        f"New balances: src={src['balance']:.2f}, tgt={tgt['balance']:.2f}",
    )

    return (
        f"Transfer of ${total_amount:.2f} from {source_acct} to {target_acct} completed successfully."
    )