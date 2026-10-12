import typing

# Simulated in‑memory document database.
# Each entry maps a document_id to its record.
DOCUMENTS_DB: dict[str, dict[str, typing.Any]] = {
    # Example entries – in a real system this would be loaded from persistent storage.
    "doc_001": {"document_id": "doc_001", "owner_id": "user_a", "content": "Initial content A."},
    "doc_002": {"document_id": "doc_002", "owner_id": "user_b", "content": "Initial content B."},
}


def modify_document(user_id: str, role: str, doc_id: str, doc_owner: str, new_data: str) -> str:
    """
    Update the content of a document if the caller has proper authorization.

    Parameters
    ----------
    user_id : str
        ID of the user attempting to modify the document.
    role : str
        Role of the caller. Accepted values: 'viewer', 'editor'.
    doc_id : str
        Unique identifier of the target document.
    doc_owner : str
        Owner ID provided by the caller (used for quick checks; verified against DB).
    new_data : str
        New content that will replace the existing document data.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the caller does not have permission to modify the document.
    KeyError
        If `doc_id` is not found in :data:`DOCUMENTS_DB`.
    ValueError
        If `role` is not one of the accepted values.
    """
    # Validate role input
    if role not in {"viewer", "editor"}:
        raise ValueError(f"Invalid role '{role}'. Allowed roles: 'viewer', 'editor'.")

    # Retrieve the document record from the database
    try:
        doc_record = DOCUMENTS_DB[doc_id]
    except KeyError as exc:
        raise KeyError(f"Document with id '{doc_id}' not found.") from exc

    # Verify that the provided owner matches the stored owner
    if doc_owner != doc_record["owner_id"]:
        raise PermissionError("Provided document owner does not match record.")

    # Authorization check: only editors or the owner can modify
    if role != "editor" and user_id != doc_record["owner_id"]:
        raise PermissionError("User is not authorized to modify this document.")

    # Perform the update
    doc_record["content"] = new_data

    return doc_record["content"]