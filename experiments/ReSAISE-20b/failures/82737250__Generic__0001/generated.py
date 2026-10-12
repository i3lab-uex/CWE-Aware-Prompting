# -*- coding: utf-8 -*-
"""
Document Management – modify_document

This module contains the `modify_document` function which allows authorized users
to update existing documents in a simple in‑memory database.
"""

from __future__ import annotations

# Simulated in-memory document store
DOCUMENTS_DB: dict[str, dict] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Initial content."},
    # Add more documents as needed
}


def modify_document(
    requester_id: str,
    requester_role: str,
    document_identifier: str,
    document_owner_id: str,
    modified_content: str,
) -> str:
    """
    Update the content of an existing document if the requester is authorized.

    Parameters
    ----------
    requester_id : str
        The ID of the user attempting to modify the document.
    requester_role : str
        The role of the user. Must be 'editor' to modify documents.
    document_identifier : str
        The unique ID of the document to be changed.
    document_owner_id : str
        The owner ID that should match the stored owner of the document.
    modified_content : str
        New content to replace the current version.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the user does not have edit rights or the document owner mismatch.
    KeyError
        If the specified document does not exist in `DOCUMENTS_DB`.
    """
    # Validate that the requested document exists
    if document_identifier not in DOCUMENTS_DB:
        raise KeyError(f"Document '{document_identifier}' does not exist.")

    # Retrieve the stored document
    doc = DOCUMENTS_DB[document_identifier]

    # Verify that the provided owner ID matches the stored owner
    if doc["owner_id"] != document_owner_id:
        raise PermissionError("Document ownership mismatch.")

    # Only users with the 'editor' role may modify documents
    if requester_role.lower() != "editor":
        raise PermissionError("Insufficient permissions: only editors may modify documents.")

    # Perform the update
    doc["content"] = modified_content

    # Return the new content for confirmation
    return doc["content"]