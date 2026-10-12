# -*- coding: utf-8 -*-
"""
Document modification helper with robust authorization checks.
"""

from typing import Dict

# Sample in‑memory database. In a real system this would be replaced by
# persistent storage (e.g., SQL, NoSQL, or an external service).
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Initial content."},
    "doc2": {"document_id": "doc2", "owner_id": "user456", "content": "Another document."},
}


def alter_document(
    modifier_id: str,
    user_role: str,
    doc_identifier: str,
    creator_id: str,
    updated_content: str,
) -> str:
    """
    Update a document's content after performing strict authorization checks.

    Parameters
    ----------
    modifier_id : str
        The ID of the user attempting to modify the document.
    user_role : str
        Role of the user; expected values are 'viewer' or 'editor'.
    doc_identifier : str
        Unique identifier of the document to modify.
    creator_id : str
        ID of the original owner of the document (should match DOCUMENTS_DB entry).
    updated_content : str
        New content to replace the existing document content.

    Returns
    -------
    str
        The updated content of the document if modification succeeds.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the document.
    KeyError
        If the specified document does not exist in DOCUMENTS_DB.
    ValueError
        If an unsupported user role is supplied.
    """
    # Validate the document exists first; this also protects against
    # tampering with doc_identifier.
    if doc_identifier not in DOCUMENTS_DB:
        raise KeyError(f"Document '{doc_identifier}' does not exist.")

    # Fetch the actual owner ID from the database to guard against
    # potential tampering with the creator_id argument.
    actual_owner_id = DOCUMENTS_DB[doc_identifier]["owner_id"]

    # Enforce role-based access control.
    if user_role not in ("viewer", "editor"):
        raise ValueError(f"Unsupported role '{user_role}'. Allowed roles: viewer, editor.")

    # Viewers are never allowed to modify documents.
    if user_role == "viewer":
        raise PermissionError("Viewers are not permitted to modify documents.")

    # Editors must be the owner of the document.
    if modifier_id != actual_owner_id:
        raise PermissionError("Only the document owner can modify this document.")

    # All checks passed – perform the update.
    DOCUMENTS_DB[doc_identifier]["content"] = updated_content

    return DOCUMENTS_DB[doc_identifier]["content"]