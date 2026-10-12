#!/usr/bin/env python3
"""
Document modification utility for a corporate document management platform.
"""

from typing import Dict

# Example in‑memory database. In production this would be replaced by a real DB.
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Initial content."},
    "doc2": {"document_id": "doc2", "owner_id": "user456", "content": "Another document."},
}


def modify_document(
    user_id: str,
    role: str,
    doc_id: str,
    doc_owner: str,
    new_data: str,
) -> str:
    """
    Update the content of a document if the caller is authorized.

    Parameters
    ----------
    user_id : str
        ID of the user attempting the update.
    role : str
        Role of the user. Expected values are 'viewer' or 'editor'.
    doc_id : str
        Identifier of the document to be updated.
    doc_owner : str
        Owner ID of the target document. This should match the 'owner_id'
        stored in the database for consistency checks.
    new_data : str
        New content that will replace the existing document body.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the user is not an editor or does not own the document.
    KeyError
        If `doc_id` is not present in :data:`DOCUMENTS_DB`.
    ValueError
        If `role` is neither 'viewer' nor 'editor'.
    """

    # Validate role
    if role not in {"viewer", "editor"}:
        raise ValueError(f"Invalid role: {role!r}. Expected 'viewer' or 'editor'.")

    # Fetch the document from the database
    try:
        doc = DOCUMENTS_DB[doc_id]
    except KeyError as exc:
        raise KeyError(f"Document with ID {doc_id!r} does not exist.") from exc

    # Ensure the provided doc_owner matches the stored owner for integrity
    if doc["owner_id"] != doc_owner:
        raise PermissionError(
            f"Provided owner ID {doc_owner!r} does not match the actual owner "
            f"{doc['owner_id']!r} for document {doc_id!r}."
        )

    # Authorization: only editors who own the doc can modify
    if role != "editor" or user_id != doc_owner:
        raise PermissionError(
            f"User {user_id!r} with role '{role}' is not authorized to modify "
            f"document {doc_id!r}."
        )

    # Perform the update
    doc["content"] = new_data

    return doc["content"]