# -*- coding: utf-8 -*-
"""
A minimal in‑memory document management helper.
"""

from typing import Dict

# Example in-memory database; in a real system this would be replaced by
# persistent storage or an ORM layer.
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    # doc_id : { 'document_id': ..., 'owner_id': ..., 'content': ... }
    "doc_001": {"document_id": "doc_001", "owner_id": "user_a", "content": "Initial content"},
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
    Update the content of a document if the caller has sufficient permissions.

    Parameters
    ----------
    member_id : str
        ID of the user attempting to modify the document.
    member_role : str
        Role of the user; accepted values are 'viewer' or 'editor'.
    doc_id : str
        Unique identifier of the target document.
    doc_owner_id : str
        Owner ID recorded in the database for the document.
    replacement_content : str
        New content to replace the current version.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the user is not authorized to edit the document.
    KeyError
        If the specified document does not exist in the database.
    ValueError
        If an unsupported role is supplied.
    """
    # Validate role
    if member_role not in {"viewer", "editor"}:
        raise ValueError(f"Unsupported role '{member_role}'. Expected 'viewer' or 'editor'.")

    # Retrieve the document
    try:
        doc = DOCUMENTS_DB[doc_id]
    except KeyError as exc:
        raise KeyError(f"Document with ID '{doc_id}' not found.") from exc

    # Verify owner consistency (redundant but defensive)
    if doc["owner_id"] != doc_owner_id:
        raise ValueError("Provided owner ID does not match the document's recorded owner.")

    # Permission check: only editors or owners may modify
    if member_role != "editor" and member_id != doc_owner_id:
        raise PermissionError(
            f"User '{member_id}' does not have permission to edit document '{doc_id}'."
        )

    # Perform the update
    doc["content"] = replacement_content

    return doc["content"]