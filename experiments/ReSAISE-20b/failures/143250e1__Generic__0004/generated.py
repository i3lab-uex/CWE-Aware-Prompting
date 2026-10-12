# -*- coding: utf-8 -*-

"""
A minimal document modification module for a corporate document‑management platform.
"""

from typing import Dict

# Example in‑memory database. In a real system this would be backed by persistent storage.
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    # document_id : { 'owner_id': ..., 'content': ... }
    "doc-001": {"owner_id": "user-alice", "content": "Initial content of Doc 1."},
    "doc-002": {"owner_id": "user-bob",   "content": "Initial content of Doc 2."},
    # ... other documents
}


def alter_document(
    modifier_id: str,
    user_role: str,
    doc_identifier: str,
    creator_id: str,
    updated_content: str
) -> str:
    """
    Update the content of a document after enforcing access control.

    Parameters
    ----------
    modifier_id : str
        The ID of the user attempting to modify the document.
    user_role : str
        Role of the user; must be either 'viewer' or 'editor'.
    doc_identifier : str
        The unique identifier of the document to modify.
    creator_id : str
        Expected owner ID for the document (used as a consistency check).
    updated_content : str
        The new content to store in the document.

    Returns
    -------
    str
        The updated document content if the operation succeeds.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the document.
    KeyError
        If the requested document does not exist in ``DOCUMENTS_DB``.
    ValueError
        If an invalid role is supplied or the creator ID does not match the stored owner.
    """
    # Validate user role
    if user_role not in {"viewer", "editor"}:
        raise ValueError(f"Invalid role '{user_role}'. Allowed roles: 'viewer', 'editor'.")

    # Retrieve the document record
    try:
        doc = DOCUMENTS_DB[doc_identifier]
    except KeyError as exc:
        raise KeyError(f"Document '{doc_identifier}' not found.") from exc

    # Ensure the provided creator_id matches the stored owner
    if doc["owner_id"] != creator_id:
        raise ValueError("Provided creator_id does not match the document's owner.")

    # Access control: only editors or the original owner can modify
    if user_role == "viewer" and modifier_id != doc["owner_id"]:
        raise PermissionError("Viewer role cannot modify documents they do not own.")

    if user_role == "editor" and modifier_id != doc["owner_id"]:
        # Editors must also be the owner
        raise PermissionError("Editor role can only modify documents they own.")

    # Perform the update
    doc["content"] = updated_content

    return doc["content"]