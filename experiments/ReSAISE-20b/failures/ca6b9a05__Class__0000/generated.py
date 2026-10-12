from __future__ import annotations

import typing as _t

# Example in‑memory accounts database
ACCOUNTS_DB: dict[str, dict[str, _t.Any]] = {
    "ACC123": {"account_number": "ACC123", "owner_id": "user1", "balance": 1000.0},
    "ACC456": {"account_number": "ACC456", "owner_id": "user2", "balance": 500.0},
    # Add more accounts as needed
}


def move_funds(
    u_id: str,
    u_role: str,
    source_account: str,
    destination_account: str,
    money: float,
) -> str:
    """
    Transfer funds between two accounts, performing authorization checks.

    Parameters
    ----------
    u_id : str
        Identifier of the individual requesting the transfer.
    u_role : str
        Role held by the individual (e.g., 'account_owner', 'bank_admin',
        'customer_service').
    source_account : str
        Account number from which funds will be deducted.
    destination_account : str
        Account number to which funds will be credited.
    money : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message confirming the transfer.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform this transfer.
    KeyError
        If either account does not exist in the database.
    ValueError
        If the source account has insufficient funds or if money <= 0.
    """

    # Validate input amount
    if money <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Ensure both accounts exist
    try:
        src = ACCOUNTS_DB[source_account]
        dst = ACCOUNTS_DB[destination_account]
    except KeyError as exc:
        raise KeyError(f"Account {exc.args[0]} does not exist.") from None

    # Authorization logic (CWE-863 prevention)
    authorized = False
    if u_role == "bank_admin":
        # Bank admins can transfer any funds
        authorized = True
    elif u_role == "account_owner":
        # Owners can only transfer from their own account
        if src["owner_id"] == u_id:
            authorized = True

    # Customer service and other roles are not allowed to transfer funds
    if not authorized:
        raise PermissionError(
            f"User '{u_id}' with role '{u_role}' is not authorized to transfer funds."
        )

    # Check sufficient balance
    if src["balance"] < money:
        raise ValueError(
            f"Insufficient funds in source account {source_account}. "
            f"Available: {src['balance']:.2f}, required: {money:.2f}."
        )

    # Perform the transfer atomically
    src["balance"] -= money
    dst["balance"] += money

    return (
        f"Transfer of {money:.2f} from account '{source_account}' "
        f"to account '{destination_account}' completed successfully."
    )