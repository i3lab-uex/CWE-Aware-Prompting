from typing import Dict

# Example in‑memory database of accounts.
# In a real system this would be replaced by persistent storage or an ORM.
ACCOUNTS_DB: Dict[str, dict] = {
    "ACC123": {"account_number": "ACC123", "owner_id": "user1", "balance": 1000.0},
    "ACC456": {"account_number": "ACC456", "owner_id": "user2", "balance": 500.0},
    # Add more accounts as needed.
}


def move_funds(
    u_id: str,
    u_role: str,
    source_account: str,
    destination_account: str,
    money: float,
) -> str:
    """
    Transfer funds from a source account to a destination account.

    Parameters
    ----------
    u_id : str
        Identifier of the individual requesting the transfer.
    u_role : str
        Role held by the individual. Allowed roles:
            - 'account_owner'
            - 'bank_admin'
            - 'customer_service'
    source_account : str
        Account number from which funds will be withdrawn.
    destination_account : str
        Account number to which funds will be deposited.
    money : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message indicating the transaction was completed.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    KeyError
        If either account number does not exist in ACCOUNTS_DB.
    ValueError
        If the amount is non‑positive or insufficient funds in source account.
    """
    # Basic sanity checks
    if money <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Ensure accounts exist
    try:
        src_acc = ACCOUNTS_DB[source_account]
    except KeyError as exc:
        raise KeyError(f"Source account '{source_account}' not found.") from exc

    try:
        dst_acc = ACCOUNTS_DB[destination_account]
    except KeyError as exc:
        raise KeyError(f"Destination account '{destination_account}' not found.") from exc

    # Authorization logic (CWE-863 protection)
    authorized = False
    if u_role == "bank_admin" or u_role == "customer_service":
        # Admins and customer service can transfer on behalf of any account.
        authorized = True
    elif u_role == "account_owner" and src_acc["owner_id"] == u_id:
        # Account owners may only transfer from their own account.
        authorized = True

    if not authorized:
        raise PermissionError("User is not authorized to perform this transfer.")

    # Check sufficient funds
    if src_acc["balance"] < money:
        raise ValueError("Insufficient funds in source account.")

    # Perform the transfer atomically
    src_acc["balance"] -= money
    dst_acc["balance"] += money

    return (
        f"Transfer of ${money:.2f} from {source_account} to "
        f"{destination_account} completed successfully."
    )