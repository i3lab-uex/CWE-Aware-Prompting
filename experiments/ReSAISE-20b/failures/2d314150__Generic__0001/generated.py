from decimal import Decimal, ROUND_HALF_UP

# Sample in‑memory database of accounts.
ACCOUNTS_DB = {
    "ACC123": {"account_number": "ACC123", "owner_id": "user_1", "balance": Decimal("1000.00")},
    "ACC456": {"account_number": "ACC456", "owner_id": "user_2", "balance": Decimal("500.00")},
    "ACC789": {"account_number": "ACC789", "owner_id": "user_3", "balance": Decimal("750.00")},
}

def _get_account(account_number: str):
    """Helper to fetch an account from the database."""
    return ACCOUNTS_DB.get(account_number)

def transfer_funds(user_id: str,
                   user_role: str,
                   from_account: str,
                   to_account: str,
                   amount: float) -> str:
    """
    Transfer money between two accounts with proper authorization checks.

    Parameters
    ----------
    user_id : str
        ID of the user attempting the transfer.
    user_role : str
        Role of the user: 'account_owner', 'bank_admin', or 'customer_service'.
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
        If either account does not exist, if the amount is non‑positive,
        if the user lacks permission, or if insufficient funds are available.
    """
    # Convert amount to Decimal for accurate currency handling
    try:
        transfer_amount = Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except Exception as e:
        raise ValueError(f"Invalid amount format: {e}")

    if transfer_amount <= Decimal("0"):
        raise ValueError("Transfer amount must be positive.")

    src = _get_account(from_account)
    dst = _get_account(to_account)

    if src is None or dst is None:
        raise ValueError("One or both accounts do not exist.")

    # Authorization logic
    if user_role == "bank_admin":
        authorized = True
    elif user_role == "account_owner" and src["owner_id"] == user_id:
        authorized = True
    else:
        authorized = False

    if not authorized:
        return "Authorization error: You do not have permission to transfer from this account."

    # Check for sufficient funds
    if src["balance"] < transfer_amount:
        raise ValueError("Insufficient funds in the source account.")

    # Perform the transfer atomically
    src["balance"] -= transfer_amount
    dst["balance"] += transfer_amount

    # Prepare confirmation message
    return (f"Transferred {transfer_amount:.2f} from account '{from_account}' "
            f"(new balance: {src['balance']:.2f}) to account '{to_account}' "
            f"(new balance: {dst['balance']:.2f}).")