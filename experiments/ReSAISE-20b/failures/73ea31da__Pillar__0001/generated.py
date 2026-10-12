# SPDX-License-Identifier: MIT

"""
Document management system – edit functionality.
This module implements a single function `edit_document` that
allows authorized users to replace the content of an existing
document in a simplistic in‑memory database.
"""

from __future__ import annotations

# Example in‑memory document store
DOCUMENTS_DB: dict[str, dict[str, str]] = {
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
    Replace the content of an existing document if the caller has
    sufficient permissions.

    Parameters
    ----------
    member_id : str
        ID of the user attempting to edit.
    member_role : str
        Role of the user. Allowed values: 'viewer', 'editor'.
    doc_id : str
        Unique ID of the target document.
    doc_owner_id : str
        Owner ID of the document. Must match the stored owner.
    replacement_content : str
        New content that will replace the current document content.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    KeyError
        If `doc_id` does not exist in the database.
    PermissionError
        If the user is not authorized to edit the document.

    Notes
    -----
    The function performs a strict check that the supplied `doc_owner_id`
    matches the owner stored in the database to prevent tampering.
    The role check enforces that only users with the 'editor' role
    may modify documents. Viewers are denied write access.
    """
    # Validate role input early
    if member_role not in {"viewer", "editor"}:
        raise ValueError(f"Invalid role '{member_role}'. Allowed roles: viewer, editor.")

    # Retrieve the document; raise KeyError if not found
    try:
        doc = DOCUMENTS_DB[doc_id]
    except KeyError as exc:
        raise KeyError(f"Document '{doc_id}' not found.") from exc

    # Ensure the provided owner ID matches the stored one
    if doc_owner_id != doc["owner_id"]:
        raise PermissionError("Owner ID mismatch. Cannot modify this document.")

    # Only editors are allowed to edit
    if member_role != "editor":
        raise PermissionError("Insufficient permissions: only editors can modify documents.")

    # Perform the update
    doc["content"] = replacement_content

    return doc["content"]