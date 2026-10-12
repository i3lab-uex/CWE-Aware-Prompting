import decimal
from typing import Dict

# Use Decimal for precise monetary calculations
decimal.getcontext().prec = 28

# A minimal in‑memory accounts database.
# In a real system this would be persisted in a secure database.
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC001": {"account_number": "ACC001", "owner_id": "EMP1001", "balance": decimal.Decimal("1500.00")},
    "ACC002": {"account_number": "ACC002", "owner_id": "EMP1002", "balance": decimal.Decimal("300.00")},
    # Add more accounts as needed
}

# Simple lock dictionary to prevent concurrent modifications.
# In production, use database transactions or a proper locking mechanism.
from threading import Lock
ACCOUNT_LOCKS: Dict[str, Lock] = {acct_no: Lock() for acct_no in ACCOUNTS_DB}


def execute_transfer(
    employee_id: str,
    role_value: str,
    source_acct: str,
    target_acct: str,
    total_amount: float
) -> str:
    """
    Transfer money from source_acct to target_acct if the employee is authorized.
    
    Parameters
    ----------
    employee_id : str
        ID of the employee initiating the transfer.
    role_value : str
        Role of the employee ('account_owner', 'bank_admin', 'customer_service').
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
        If the employee is not authorized to perform the transfer.
    KeyError
        If either account does not exist in ACCOUNTS_DB.
    ValueError
        If the amount is negative or zero, or insufficient funds.
    """
    # Basic input validation
    if total_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Resolve accounts
    try:
        source = ACCOUNTS_DB[source_acct]
        target = ACCOUNTS_DB[target_acct]
    except KeyError as exc:
        raise KeyError(f"Account not found: {exc.args[0]}") from None

    # Authorization check (CWE-863)
    authorized = False
    if role_value == "bank_admin":
        authorized = True
    elif role_value == "account_owner" and source["owner_id"] == employee_id:
        authorized = True
    # customer_service is not allowed to transfer funds

    if not authorized:
        raise PermissionError(
            f"Employee {employee_id} with role '{role_value}' is not authorized "
            f"to transfer funds from account {source_acct}."
        )

    # Acquire locks for both accounts to avoid race conditions
    first_lock, second_lock = (
        (ACCOUNT_LOCKS[source_acct], ACCOUNT_LOCKS[target_acct])
        if source_acct < target_acct
        else (ACCOUNT_LOCKS[target_acct], ACCOUNT_LOCKS[source_acct])
    )

    with first_lock, second_lock:
        # Re‑check balance inside lock
        amount = decimal.Decimal(str(total_amount))
        if source["balance"] < amount:
            raise ValueError(
                f"Insufficient funds in account {source_acct}: "
                f"available={source['balance']}, required={amount}"
            )

        # Perform transfer
        source["balance"] -= amount
        target["balance"] += amount

    return (
        f"Transfer of {amount:.2f} from account {source_acct} "
        f"to account {target_acct} completed successfully."
    )