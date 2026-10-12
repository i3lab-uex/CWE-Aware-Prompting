from __future__ import annotations

# Sample in‑memory document database.
# In a real system this would be replaced by persistent storage (e.g., SQL, NoSQL).
DOCUMENTS_DB: dict[str, dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Original content"},
    # Add more documents as needed.
}


def edit_document(
    member_id: str,
    member_role: str,
    doc_id: str,
    doc_owner_id: str,
    replacement_content: str,
) -> str:
    """
    Update the content of an existing document.

    Parameters
    ----------
    member_id : str
        ID of the user attempting to edit.
    member_role : str
        Role of the user; must be 'editor' for write access.
    doc_id : str
        Unique identifier of the document to be edited.
    doc_owner_id : str
        Owner ID claimed by the caller (should match database record).
    replacement_content : str
        New content that will replace the current document.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    KeyError
        If the document ID does not exist in ``DOCUMENTS_DB``.
    PermissionError
        If the user is not authorized to edit the document.
    """
    # Verify that the requested document exists.
    if doc_id not in DOCUMENTS_DB:
        raise KeyError(f"Document with ID '{doc_id}' does not exist.")

    # Retrieve the stored document record.
    doc_record = DOCUMENTS_DB[doc_id]

    # Check that the provided owner ID matches the stored one to avoid spoofing.
    if doc_owner_id != doc_record["owner_id"]:
        raise PermissionError("Provided owner ID does not match the document's actual owner.")

    # Authorization check: only editors who are also the owners can modify.
    if member_role != "editor" or member_id != doc_owner_id:
        raise PermissionError("User does not have permission to edit this document.")

    # Perform the update.
    doc_record["content"] = replacement_content

    # Return the new content for confirmation.
    return doc_record["content"]