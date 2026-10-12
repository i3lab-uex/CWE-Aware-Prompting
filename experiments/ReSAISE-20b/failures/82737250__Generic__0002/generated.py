# -*- coding: utf-8 -*-

"""
Document Management System – modify_document

This module provides a simple in‑memory document store and the
`modify_document` function which updates an existing document.
"""

from __future__ import annotations

# In‑memory mock database of documents
DOCUMENTS_DB: dict[str, dict] = {
    # Example entries (these would normally be populated elsewhere)
    "doc-001": {"document_id": "doc-001", "owner_id": "user-123", "content": "Initial content."},
    "doc-002": {"document_id": "doc-002", "owner_id": "user-456", "content": "Another document."},
}


def modify_document(
    requester_id: str,
    requester_role: str,
    document_identifier: str,
    document_owner_id: str,
    modified_content: str,
) -> str:
    """
    Update the content of an existing document if the requester has sufficient
    permissions.

    Parameters
    ----------
    requester_id : str
        ID of the user attempting to modify the document.
    requester_role : str
        Role of the user; accepted values are 'viewer' or 'editor'.
    document_identifier : str
        Unique identifier of the target document.
    document_owner_id : str
        Owner ID supplied for an additional safety check. Must match the
        owner stored in the database.
    modified_content : str
        New content to replace the current document content.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    PermissionError
        If the requester does not have edit rights or if the supplied owner ID
        does not match the database record.
    KeyError
        If the document identifier is not found in ``DOCUMENTS_DB``.
    ValueError
        If an unsupported role is supplied.
    """
    # Validate that the document exists
    if document_identifier not in DOCUMENTS_DB:
        raise KeyError(f"Document '{document_identifier}' does not exist.")

    doc = DOCUMENTS_DB[document_identifier]

    # Ensure the owner ID supplied matches the stored owner
    if doc["owner_id"] != document_owner_id:
        raise PermissionError("Owner ID mismatch. Access denied.")

    # Enforce role-based access control
    if requester_role not in {"viewer", "editor"}:
        raise ValueError(f"Unsupported role '{requester_role}'. Must be 'viewer' or 'editor'.")

    # Only editors or the owner may modify
    if requester_role == "viewer":
        raise PermissionError("Viewers are not allowed to modify documents.")
    if requester_id != doc["owner_id"] and requester_role == "editor":
        # Editors can modify any document; adjust if you want stricter rules
        pass

    # Perform the update
    doc["content"] = modified_content

    # Return the new content for confirmation
    return doc["content"]