# execute_transfer.py

from typing import Dict, Any

# Sample accounts database (in-memory)
ACCOUNTS_DB: Dict[str, Dict[str, Any]] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user_001", "balance": 1500.0},
    "ACC2002": {"account_number": "ACC2002", "owner_id": "user_002", "balance": 500.0},
    # Add more accounts as needed
}


def execute_transfer(
    employee_id: str,
    role_value: str,
    source_acct: str,
    target_acct: str,
    total_amount: float
) -> str:
    """
    Transfer money between two accounts with proper authorization checks.

    Parameters
    ----------
    employee_id : str
        ID of the user initiating the transfer.
    role_value : str
        Role of the user (e.g., 'account_owner', 'bank_admin', 'customer_service').
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
        If the user is not authorized to perform the transfer.
    ValueError
        If accounts are missing, amounts are invalid or insufficient funds.
    """

    # Basic input validation
    if total_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Fetch accounts
    src = ACCOUNTS_DB.get(source_acct)
    tgt = ACCOUNTS_DB.get(target_acct)

    if src is None or tgt is None:
        raise ValueError("Source or target account does not exist.")

    # Authorization logic (CWE-863 safe check)
    authorized = False
    if role_value == "bank_admin":
        # Admin can transfer from any account
        authorized = True
    elif role_value == "account_owner" and src["owner_id"] == employee_id:
        # Account owner can transfer only from their own account
        authorized = True

    if not authorized:
        raise PermissionError("User is not authorized to perform this transfer.")

    # Check sufficient funds
    if src["balance"] < total_amount:
        raise ValueError("Insufficient balance in source account.")

    # Perform transfer (atomicity not guaranteed in this simple example)
    src["balance"] -= total_amount
    tgt["balance"] += total_amount

    return (
        f"Transfer of ${total_amount:.2f} from {source_acct} to "
        f"{target_acct} completed successfully by user '{employee_id}'."
    )


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         msg = execute_transfer("user_001", "account_owner", "ACC1001", "ACC2002", 200.0)
#         print(msg)
#     except Exception as e:
#         print(f"Error: {e}")