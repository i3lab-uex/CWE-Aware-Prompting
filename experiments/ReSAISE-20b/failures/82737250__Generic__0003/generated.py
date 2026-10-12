import datetime

# Example in‑memory document database.
DOCUMENTS_DB = {
    "doc001": {"document_id": "doc001", "owner_id": "user123", "content": "Initial content."},
    # Add more documents as needed.
}

def modify_document(
    requester_id: str,
    requester_role: str,
    document_identifier: str,
    document_owner_id: str,
    modified_content: str
) -> str:
    """
    Update the content of an existing document if the requester has sufficient privileges.

    Parameters
    ----------
    requester_id : str
        ID of the user attempting to modify the document.
    requester_role : str
        Role of the user ('viewer' or 'editor').
    document_identifier : str
        Unique ID of the target document.
    document_owner_id : str
        Owner ID provided for validation (must match the stored owner).
    modified_content : str
        New content to replace the current document content.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the requester is not an editor or does not own the document.
    KeyError
        If the document_identifier does not exist in DOCUMENTS_DB.
    ValueError
        If any required argument is missing or invalid.
    """
    # Basic validation of inputs
    if not all([requester_id, requester_role, document_identifier,
                document_owner_id, modified_content]):
        raise ValueError("All arguments must be provided and non-empty.")

    # Retrieve the document from the database
    try:
        doc = DOCUMENTS_DB[document_identifier]
    except KeyError as exc:
        raise KeyError(f"Document '{document_identifier}' not found.") from exc

    # Verify that the provided owner_id matches the stored one
    if doc["owner_id"] != document_owner_id:
        raise ValueError("Provided owner ID does not match the document's actual owner.")

    # Authorization check: only editors or the owner can modify
    if requester_role != "editor" and requester_id != doc["owner_id"]:
        raise PermissionError(
            f"User '{requester_id}' lacks permission to modify document "
            f"'{document_identifier}'."
        )

    # Perform the update
    doc["content"] = modified_content

    # Optionally, log the modification with a timestamp
    _log_modification(requester_id, document_identifier)

    return doc["content"]


def _log_modification(user_id: str, document_id: str) -> None:
    """
    Internal helper to log modifications. In a real system, this would write
    to a persistent audit trail; here we simply print for demonstration.
    """
    timestamp = datetime.datetime.utcnow().isoformat()
    print(f"[{timestamp}] User '{user_id}' modified document '{document_id}'.")