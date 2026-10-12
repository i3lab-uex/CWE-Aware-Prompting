# -*- coding: utf-8 -*-

"""
Document modification helper for a simple in‑memory document store.
"""

from typing import Dict

# Sample in-memory database. In a real system this would be replaced
# with persistent storage (e.g., SQL, NoSQL, file system).
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc-001": {"document_id": "doc-001", "owner_id": "user-123", "content": "Original content A."},
    "doc-002": {"document_id": "doc-002", "owner_id": "user-456", "content": "Original content B."},
}


def modify_document(
    requester_id: str,
    requester_role: str,
    document_identifier: str,
    document_owner_id: str,
    modified_content: str,
) -> str:
    """
    Modify the content of an existing document.

    Parameters
    ----------
    requester_id : str
        ID of the user attempting to modify the document.
    requester_role : str
        Role of the requester. Only 'editor' is allowed to modify.
    document_identifier : str
        Unique ID of the target document in `DOCUMENTS_DB`.
    document_owner_id : str
        The expected owner ID of the target document.
    modified_content : str
        New content to replace the current document content.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    PermissionError
        If the requester does not have permission to modify the document.
    KeyError
        If the specified document identifier does not exist in `DOCUMENTS_DB`.
    """
    # Ensure the requested document exists
    if document_identifier not in DOCUMENTS_DB:
        raise KeyError(f"Document '{document_identifier}' not found.")

    doc = DOCUMENTS_DB[document_identifier]

    # Validate ownership
    if doc["owner_id"] != document_owner_id:
        raise ValueError("Provided owner ID does not match the actual owner of the document.")

    # Validate requester role
    if requester_role.lower() != "editor":
        raise PermissionError("Insufficient permissions: only editors may modify documents.")

    # Optional: Ensure requester is the owner (common pattern)
    if requester_id != document_owner_id:
        raise PermissionError("Insufficient permissions: only the owner may modify this document.")

    # Perform the update
    doc["content"] = modified_content

    return doc["content"]