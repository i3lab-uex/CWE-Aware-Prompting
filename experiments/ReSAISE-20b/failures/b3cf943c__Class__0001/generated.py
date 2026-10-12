#!/usr/bin/env python3
"""
Document modification helper for a corporate document management platform.

The implementation follows best practices to prevent CWE‑863 (Incorrect
Authorization) by strictly verifying that the user has the right role and,
when necessary, is the owner of the document before allowing an update.
"""

from typing import Dict

# Sample in‑memory database. In a real system this would be replaced by
# persistent storage (e.g., SQL, NoSQL) and proper authentication.
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Initial content."},
    "doc2": {"document_id": "doc2", "owner_id": "user456", "content": "Another document."},
}


def modify_document(user_id: str, role: str, doc_id: str, doc_owner: str, new_data: str) -> str:
    """
    Update the content of a document if the caller is authorized.

    Parameters
    ----------
    user_id : str
        Identifier of the user attempting to modify the document.
    role : str
        Role of the caller. Expected values: 'viewer', 'editor'.
    doc_id : str
        Identifier of the target document.
    doc_owner : str
        Identifier of the owner declared by the caller. This is checked against
        the stored owner to guard against tampering.
    new_data : str
        New content that will replace the existing document data.

    Returns
    -------
    str
        The updated document content upon success.

    Raises
    ------
    PermissionError
        If the caller is not an editor or does not own the document.
    KeyError
        If the requested document ID is not present in the database.
    """
    # Validate role first to avoid unnecessary lookups
    if role not in {"viewer", "editor"}:
        raise ValueError(f"Invalid role: {role!r}")

    # Retrieve the document; KeyError will propagate if missing
    doc = DOCUMENTS_DB[doc_id]

    # Enforce that the caller's declared owner matches the stored owner
    if doc_owner != doc["owner_id"]:
        raise PermissionError("Document ownership mismatch detected.")

    # Authorization check: only editors may modify, and they must be the owner
    if role != "editor" or user_id != doc_owner:
        raise PermissionError("User is not authorized to modify this document.")

    # Perform the update
    doc["content"] = new_data

    return doc["content"]