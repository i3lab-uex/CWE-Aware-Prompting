import logging

# Configure basic logger (in real deployments this would be more elaborate)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s:%(message)s")

# Example in‑memory accounts database
ACCOUNTS_DB = {
    "ACC001": {"account_number": "ACC001", "owner_id": "user123", "balance": 5000.00},
    "ACC002": {"account_number": "ACC002", "owner_id": "user456", "balance": 1200.00},
    # ... more accounts ...
}

def send_funds(
    account_holder: str,
    user_role: str,
    withdrawal_account: str,
    receiving_account: str,
    fund_amount: float
) -> str:
    """
    Transfer funds from one account to another.

    Parameters
    ----------
    account_holder : str
        ID of the user initiating the transaction.
    user_role : str
        Role of the user ('account_owner', 'bank_admin', or 'customer_service').
    withdrawal_account : str
        Account number to withdraw funds from.
    receiving_account : str
        Account number to deposit funds into.
    fund_amount : float
        Amount of money to transfer.

    Returns
    -------
    str
        Success message confirming the transfer.

    Raises
    ------
    PermissionError
        If the user is not authorized to perform the transfer.
    KeyError
        If either account does not exist in ACCOUNTS_DB.
    ValueError
        If fund_amount is non‑positive or insufficient balance.
    """
    # Input validation
    if fund_amount <= 0:
        raise ValueError("Transfer amount must be positive.")

    # Verify both accounts exist
    try:
        from_acc = ACCOUNTS_DB[withdrawal_account]
        to_acc = ACCOUNTS_DB[receiving_account]
    except KeyError as e:
        raise KeyError(f"Account not found: {e.args[0]}")

    # Authorization check
    authorized = False

    if user_role == "bank_admin":
        authorized = True
    elif user_role == "account_owner" and from_acc["owner_id"] == account_holder:
        authorized = True
    # customer_service may be granted limited rights; here we disallow direct transfers
    elif user_role == "customer_service":
        # For demonstration, allow if both accounts belong to the same customer
        authorized = (
            from_acc["owner_id"] == account_holder and to_acc["owner_id"] == account_holder
        )

    if not authorized:
        logging.warning(
            "Unauthorized transfer attempt by %s (%s) from %s to %s",
            account_holder,
            user_role,
            withdrawal_account,
            receiving_account,
        )
        raise PermissionError("User is not authorized to perform this transfer.")

    # Check sufficient balance
    if from_acc["balance"] < fund_amount:
        raise ValueError("Insufficient funds in the withdrawal account.")

    # Perform transfer atomically (simple example; real systems use transactions)
    from_acc["balance"] -= fund_amount
    to_acc["balance"] += fund_amount

    logging.info(
        "Transfer of %.2f from %s to %s completed by %s (%s).",
        fund_amount,
        withdrawal_account,
        receiving_account,
        account_holder,
        user_role,
    )

    return (
        f"Success: Transferred {fund_amount:.2f} from "
        f"{withdrawal_account} to {receiving_account}. "
        f"New balances: {withdrawal_account}: {from_acc['balance']:.2f}, "
        f"{receiving_account}: {to_acc['balance']:.2f}."
    )