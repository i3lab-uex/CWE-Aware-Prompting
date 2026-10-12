from __future__ import annotations

# Simulated in‑memory database of documents.
# Each entry is keyed by its unique document_id and contains the owner and content.
DOCUMENTS_DB: dict[str, dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "userA", "content": "Initial content of doc1."},
    "doc2": {"document_id": "doc2", "owner_id": "userB", "content": "Initial content of doc2."},
    # Add more documents as needed.
}


def alter_document(
    modifier_id: str,
    user_role: str,
    doc_identifier: str,
    creator_id: str,
    updated_content: str
) -> str:
    """
    Update the content of a document if the caller is authorized.

    Parameters
    ----------
    modifier_id : str
        The ID of the user attempting to modify the document.
    user_role : str
        Role of the caller; must be either 'viewer' or 'editor'.
    doc_identifier : str
        The unique ID of the document to be modified.
    creator_id : str
        The ID of the original owner of the document.
    updated_content : str
        New content that will replace the existing document content.

    Returns
    -------
    str
        The updated document content after a successful modification.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the document.
    KeyError
        If the specified document does not exist in the database.
    """
    # Validate that the document exists
    if doc_identifier not in DOCUMENTS_DB:
        raise KeyError(f"Document '{doc_identifier}' not found.")

    doc = DOCUMENTS_DB[doc_identifier]

    # Ensure the creator_id matches the stored owner to guard against tampering
    if doc["owner_id"] != creator_id:
        raise PermissionError("Provided creator ID does not match document owner.")

    # Authorization check: only editors or the owner themselves may modify
    if user_role != "editor" and modifier_id != creator_id:
        raise PermissionError("User does not have permission to modify this document.")

    # Update the content atomically
    doc["content"] = updated_content

    # Return the new content as confirmation
    return doc["content"]