from typing import Dict

# Example accounts database
ACCOUNTS_DB: Dict[str, Dict[str, object]] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "user_001", "balance": 5000.0},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "user_002", "balance": 3000.0},
    # Add more accounts as needed
}

def transfer_funds(
    user_id: str,
    user_role: str,
    from_account: str,
    to_account: str,
    amount: float
) -> str:
    """
    Transfer money between two accounts with proper authorization checks.

    Parameters
    ----------
    user_id : str
        ID of the user attempting the transfer.
    user_role : str
        Role of the user ('account_owner', 'bank_admin', or 'customer_service').
    from_account : str
        Account number to transfer funds from.
    to_account : str
        Account number to transfer funds to.
    amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Confirmation message if the transfer succeeded.

    Raises
    ------
    ValueError
        If either account does not exist, if the user is not authorized,
        or if there are insufficient funds.
    """
    # Validate amount
    if amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Retrieve accounts
    src = ACCOUNTS_DB.get(from_account)
    dst = ACCOUNTS_DB.get(to_account)

    if src is None or dst is None:
        raise ValueError("One or both accounts do not exist.")

    # Authorization logic
    authorized = False

    if user_role == "bank_admin":
        authorized = True  # Admin can transfer between any accounts
    elif user_role == "account_owner":
        if src["owner_id"] == user_id and dst["owner_id"] == user_id:
            authorized = True  # Owner transferring between own accounts
    elif user_role == "customer_service":
        # Customer service is not allowed to transfer funds directly
        authorized = False

    if not authorized:
        raise ValueError("User is not authorized to perform this transfer.")

    # Check sufficient funds
    if src["balance"] < amount:
        raise ValueError("Insufficient funds in the source account.")

    # Perform transfer
    src["balance"] -= amount
    dst["balance"] += amount

    return (
        f"Transfer of ${amount:.2f} from {from_account} to "
        f"{to_account} completed successfully."
    )