from __future__ import annotations

# Simulated database of documents.
DOCUMENTS_DB: dict[str, dict[str, str]] = {
    # Example entries
    "doc_001": {"document_id": "doc_001", "owner_id": "user_a", "content": "Initial content."},
    "doc_002": {"document_id": "doc_002", "owner_id": "user_b", "content": "Another document."},
}


def modify_document(
    user_id: str,
    role: str,
    doc_id: str,
    doc_owner: str,
    new_data: str,
) -> str:
    """
    Update the content of a document if the caller has sufficient permissions.

    Parameters
    ----------
    user_id : str
        The ID of the user attempting to modify the document.
    role : str
        The role of the caller. Only 'editor' is allowed to modify.
    doc_id : str
        The unique identifier of the document to be updated.
    doc_owner : str
        The ID of the original owner of the document. Must match the actual
        owner stored in ``DOCUMENTS_DB``.
    new_data : str
        The new content to replace the current document content.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the document.
    KeyError
        If the specified ``doc_id`` does not exist in the database.
    """
    # Ensure the document exists
    if doc_id not in DOCUMENTS_DB:
        raise KeyError(f"Document {doc_id} does not exist.")

    doc_record = DOCUMENTS_DB[doc_id]

    # Validate that the provided owner matches the actual owner
    if doc_owner != doc_record["owner_id"]:
        raise PermissionError("Provided document owner does not match the actual owner.")

    # Check that the user has editor privileges
    if role.lower() != "editor":
        raise PermissionError("Only users with the 'editor' role can modify documents.")

    # Check that the user is indeed the owner of the document
    if user_id != doc_record["owner_id"]:
        raise PermissionError("Only the owner can modify this document.")

    # All checks passed – perform the update
    doc_record["content"] = new_data

    return doc_record["content"]