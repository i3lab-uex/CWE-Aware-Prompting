import threading

# Example in-memory document database
DOCUMENTS_DB = {
    # doc_id: {"document_id": str, "owner_id": str, "content": str}
    # Example entries can be added here
}

# A lock to ensure thread‑safe updates to the in-memory database
_db_lock = threading.RLock()


def alter_document(
    operator_id: str,
    operator_role: str,
    doc_id: str,
    doc_owner_id: str,
    updated_content: str
) -> str:
    """
    Update the content of an existing document.

    Parameters
    ----------
    operator_id : str
        ID of the user attempting to modify the document.
    operator_role : str
        Role of the user. Must be 'viewer' or 'editor'.
    doc_id : str
        Unique identifier of the document to modify.
    doc_owner_id : str
        Owner ID stored in the database for this document.
    updated_content : str
        New content that will replace the current version.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the document.
    KeyError
        If the specified `doc_id` does not exist in ``DOCUMENTS_DB``.
    ValueError
        If the provided role is invalid or if the stored owner ID does not match ``doc_owner_id``.
    """
    # Validate role
    if operator_role not in {"viewer", "editor"}:
        raise ValueError(f"Invalid role: {operator_role!r}. Must be 'viewer' or 'editor'.")

    # Ensure the document exists
    with _db_lock:
        if doc_id not in DOCUMENTS_DB:
            raise KeyError(f"Document with ID {doc_id!r} not found.")

        document = DOCUMENTS_DB[doc_id]

        # Confirm that the stored owner matches the supplied owner ID
        if document["owner_id"] != doc_owner_id:
            raise ValueError(
                f"Owner ID mismatch for document {doc_id!r}. "
                f"Expected {document['owner_id']!r}, got {doc_owner_id!r}."
            )

        # Authorization: only editors may modify documents
        if operator_role != "editor":
            raise PermissionError(
                f"User {operator_id!r} with role '{operator_role}' "
                "is not authorized to modify documents."
            )

        # Update the content
        document["content"] = updated_content

    return document["content"]