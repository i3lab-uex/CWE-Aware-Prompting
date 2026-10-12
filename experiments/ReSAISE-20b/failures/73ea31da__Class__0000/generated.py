# -*- coding: utf-8 -*-
"""
A simple in‑memory document management helper.
"""

from typing import Dict

# Example in‑memory database of documents
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Original content of doc1."},
    "doc2": {"document_id": "doc2", "owner_id": "user456", "content": "Original content of doc2."},
}


def edit_document(
    member_id: str,
    member_role: str,
    doc_id: str,
    doc_owner_id: str,
    replacement_content: str,
) -> str:
    """
    Edit the content of an existing document.

    Parameters
    ----------
    member_id : str
        The ID of the user attempting to modify the document.
    member_role : str
        The role of the user. Must be either 'viewer' or 'editor'.
    doc_id : str
        The unique ID of the document to be changed.
    doc_owner_id : str
        The owner ID supplied by the caller (used for an extra consistency check).
    replacement_content : str
        The new content that will replace the current version.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    PermissionError
        If the user does not have permission to edit the document.
    KeyError
        If the document ID is not found in the database.
    ValueError
        If an unexpected role value is supplied.
    """
    # Validate role
    if member_role not in {"viewer", "editor"}:
        raise ValueError(f"Unknown role: {member_role!r}")

    # Fetch the document from the database
    try:
        doc = DOCUMENTS_DB[doc_id]
    except KeyError as exc:
        raise KeyError(f"Document {doc_id!r} does not exist.") from exc

    # Ensure the supplied owner ID matches the stored one
    if doc_owner_id != doc["owner_id"]:
        raise PermissionError("Provided owner ID does not match the document's actual owner.")

    # Authorization check: only editors are allowed to modify
    if member_role != "editor":
        raise PermissionError("User does not have permission to edit documents.")

    # Optionally, enforce that only the owner or an editor can modify
    if member_id != doc["owner_id"] and member_role == "editor":
        # In this simplified model, editors can edit any document regardless of ownership.
        pass

    # Perform the update
    doc["content"] = replacement_content

    return doc["content"]