# execute_transfer.py

from typing import Dict

# Sample accounts database structure for demonstration.
ACCOUNTS_DB: Dict[str, Dict] = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user123", "balance": 5000.00},
    "ACC002": {"account_number": "ACC002", "owner_id": "user456", "balance": 3000.00},
    # Add more accounts as needed.
}

def execute_transfer(
    employee_id: str,
    role_value: str,
    source_acct: str,
    target_acct: str,
    total_amount: float
) -> str:
    """
    Transfer funds from source_acct to target_acct if the employee is authorized.

    Parameters
    ----------
    employee_id : str
        ID of the user initiating the transfer.
    role_value : str
        Role of the employee (e.g., 'account_owner', 'bank_admin', 'customer_service').
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
    ValueError
        If accounts are missing or amount invalid.
    """
    # Basic validation of inputs
    if total_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Retrieve accounts from the database
    source = ACCOUNTS_DB.get(source_acct)
    target = ACCOUNTS_DB.get(target_acct)

    if source is None or target is None:
        raise ValueError("Source or target account does not exist.")

    # Authorization check
    authorized = False

    if role_value == "bank_admin":
        authorized = True  # Bank admins can transfer between any accounts
    elif role_value == "account_owner" and source["owner_id"] == employee_id:
        authorized = True  # Account owner can transfer from their own account
    elif role_value == "customer_service":
        # Customer service may be allowed only for specific internal operations;
        # here we assume they are not permitted to transfer funds directly.
        authorized = False

    if not authorized:
        raise PermissionError("Unauthorized: insufficient privileges to perform transfer.")

    # Check sufficient balance
    if source["balance"] < total_amount:
        raise ValueError("Insufficient funds in the source account.")

    # Perform transfer
    source["balance"] -= total_amount
    target["balance"] += total_amount

    return (
        f"Transfer of ${total_amount:,.2f} from account {source_acct} "
        f"to account {target_acct} completed successfully."
    )