# -*- coding: utf-8 -*-

"""
Document editing module for a company document management system.
"""

from __future__ import annotations

# Example in-memory database of documents
DOCUMENTS_DB = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Original content of doc1."},
    "doc2": {"document_id": "doc2", "owner_id": "user456", "content": "Original content of doc2."},
    # ... more documents
}


def edit_document(
    member_id: str,
    member_role: str,
    doc_id: str,
    doc_owner_id: str,
    replacement_content: str
) -> str:
    """
    Edit the content of an existing document.

    Parameters
    ----------
    member_id : str
        ID of the user attempting to modify the document.
    member_role : str
        Role of the user, expected values are 'viewer' or 'editor'.
    doc_id : str
        Unique identifier of the document to be edited.
    doc_owner_id : str
        ID of the owner of the document.
    replacement_content : str
        New content that will replace the current version.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the user does not have permission to edit the document.
    KeyError
        If the specified document ID is not found in the database.
    ValueError
        If `member_role` is neither 'viewer' nor 'editor'.
    """

    # Validate role
    if member_role not in {"viewer", "editor"}:
        raise ValueError(f"Invalid role '{member_role}'. Allowed roles: 'viewer', 'editor'.")

    # Retrieve the document from the database
    try:
        doc = DOCUMENTS_DB[doc_id]
    except KeyError as exc:
        raise KeyError(f"Document with ID '{doc_id}' not found.") from exc

    # Ensure the owner ID matches the one stored in the database
    if doc_owner_id != doc["owner_id"]:
        raise ValueError("Provided owner ID does not match the document's recorded owner.")

    # Authorization check: only editors who are also the owner can modify
    if member_role != "editor" or member_id != doc_owner_id:
        raise PermissionError("Insufficient permissions to edit this document.")

    # Perform the update
    doc["content"] = replacement_content

    return doc["content"]