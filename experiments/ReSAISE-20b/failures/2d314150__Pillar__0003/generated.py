from __future__ import annotations

# Sample in‑memory accounts database.
ACCOUNTS_DB: dict[str, dict] = {
    "ACC1001": {"account_number": "ACC1001", "owner_id": "U001", "balance": 1500.00},
    "ACC1002": {"account_number": "ACC1002", "owner_id": "U002", "balance": 2000.00},
    "ACC1003": {"account_number": "ACC1003", "owner_id": "U003", "balance": 500.00},
}

def transfer_funds(
    user_id: str,
    user_role: str,
    from_account: str,
    to_account: str,
    amount: float,
) -> str:
    """
    Transfer money between two accounts after performing authorization checks.

    Parameters
    ----------
    user_id : str
        ID of the user attempting the transfer.
    user_role : str
        Role of the user (e.g., 'account_owner', 'bank_admin', 'customer_service').
    from_account : str
        Account number to debit.
    to_account : str
        Account number to credit.
    amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Confirmation message if the transfer succeeds.

    Raises
    ------
    ValueError
        If either account does not exist, the amount is non‑positive,
        insufficient funds, or authorization fails.
    """
    # Basic input validation
    if amount <= 0:
        raise ValueError("Transfer amount must be positive")

    # Retrieve accounts
    src = ACCOUNTS_DB.get(from_account)
    dst = ACCOUNTS_DB.get(to_account)

    if src is None or dst is None:
        raise ValueError("One or both accounts do not exist")

    # Authorization logic
    if user_role == "account_owner":
        # Owner can only transfer from their own account
        if src["owner_id"] != user_id:
            raise ValueError("Authorization failed: cannot transfer from an account you do not own")
    elif user_role in {"bank_admin", "customer_service"}:
        # These roles have unrestricted access
        pass
    else:
        raise ValueError("Authorization failed: unknown user role")

    # Sufficient funds check
    if src["balance"] < amount:
        raise ValueError("Insufficient funds in the source account")

    # Perform transfer
    src["balance"] -= amount
    dst["balance"] += amount

    return (
        f"Transfer of ${amount:,.2f} from {from_account} to "
        f"{to_account} completed successfully."
    )