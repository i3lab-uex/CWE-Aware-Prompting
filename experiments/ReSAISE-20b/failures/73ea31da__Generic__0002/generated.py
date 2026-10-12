# -*- coding: utf-8 -*-
"""
Document Management System – Edit Document Utility

This module provides a single function `edit_document` that allows an
authorized user to replace the content of an existing document.
"""

from __future__ import annotations

# Example in‑memory database; in a real system this would be replaced by
# persistent storage (e.g., a relational database or NoSQL store).
DOCUMENTS_DB: dict[str, dict[str, str]] = {
    # document_id : { "document_id": ..., "owner_id": ..., "content": ... }
    # Example entry:
    # "doc-001": {"document_id": "doc-001", "owner_id": "user123", "content": "Initial content."}
}


def edit_document(
    member_id: str,
    member_role: str,
    doc_id: str,
    doc_owner_id: str,
    replacement_content: str,
) -> str:
    """
    Replace the content of a document if the caller is authorized.

    Parameters
    ----------
    member_id : str
        The ID of the user attempting to modify the document.
    member_role : str
        Role of the caller. Must be 'editor' or 'viewer'.
    doc_id : str
        The unique identifier of the document to edit.
    doc_owner_id : str
        The owner ID of the target document. (Used for extra safety checks.)
    replacement_content : str
        The new content that will replace the existing document.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    KeyError
        If the specified `doc_id` does not exist in the database.
    PermissionError
        If the caller is not authorized to edit the document.
    ValueError
        If `member_role` is not one of the expected values.
    """

    # Validate role
    if member_role not in {"viewer", "editor"}:
        raise ValueError(f"Invalid role '{member_role}'. Must be 'viewer' or 'editor'.")

    # Check that the document exists
    if doc_id not in DOCUMENTS_DB:
        raise KeyError(f"Document with id '{doc_id}' does not exist.")

    doc = DOCUMENTS_DB[doc_id]

    # Verify that the provided owner ID matches the stored one
    if doc_owner_id != doc["owner_id"]:
        raise PermissionError("Owner ID mismatch. Cannot proceed with edit.")

    # Authorization: only editors or the owner can modify
    if member_role != "editor" and member_id != doc["owner_id"]:
        raise PermissionError("Insufficient permissions to edit this document.")

    # Perform the update
    doc["content"] = replacement_content

    return doc["content"]