# -*- coding: utf-8 -*-
"""
Simple document editing function for a company document management system.
"""

from typing import Dict

# Sample in-memory database
DOCUMENTS_DB: Dict[str, dict] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Initial content of doc1."},
    "doc2": {"document_id": "doc2", "owner_id": "user456", "content": "Initial content of doc2."},
    # Add more documents as needed
}


def edit_document(
    member_id: str,
    member_role: str,
    doc_id: str,
    doc_owner_id: str,
    replacement_content: str,
) -> str:
    """
    Edit an existing document if the user has sufficient permissions.

    Parameters
    ----------
    member_id : str
        ID of the user attempting to modify the document.
    member_role : str
        Role of the user. Accepted values are 'viewer' or 'editor'.
    doc_id : str
        Unique ID of the document to be changed.
    doc_owner_id : str
        ID of the owner of the document. (Used for an additional check.)
    replacement_content : str
        New content that will replace the current document content.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    PermissionError
        If the user does not have edit permissions.
    KeyError
        If the document ID is not found in ``DOCUMENTS_DB``.
    ValueError
        If an invalid role is supplied.
    """
    # Validate the role
    if member_role not in {"viewer", "editor"}:
        raise ValueError(f"Invalid role '{member_role}'. Allowed roles: 'viewer', 'editor'.")

    # Retrieve the document from the database
    try:
        doc = DOCUMENTS_DB[doc_id]
    except KeyError as exc:
        raise KeyError(f"Document with ID '{doc_id}' does not exist.") from exc

    # Verify the provided owner matches the stored owner
    if doc_owner_id != doc["owner_id"]:
        raise ValueError("Provided document owner ID does not match the stored owner.")

    # Check permissions: editors or owners can edit
    if member_role != "editor" and member_id != doc_owner_id:
        raise PermissionError("You do not have permission to edit this document.")

    # Perform the update
    doc["content"] = replacement_content

    # Return the updated content
    return doc["content"]