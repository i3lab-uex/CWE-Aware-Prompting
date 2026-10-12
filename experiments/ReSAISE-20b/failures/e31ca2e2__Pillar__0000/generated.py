# -*- coding: utf-8 -*-
"""
Document editing module.

This module implements a simple in‑memory document management system
with proper access control.  The function `edit_doc` checks that the
document exists, verifies that the caller is authorized (either an
editor or the document owner), and updates the content.
"""

from __future__ import annotations

# Sample in‑memory database of documents
DOCUMENTS_DB: dict[str, dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "user_a", "content": "Initial content of doc1."},
    "doc2": {"document_id": "doc2", "owner_id": "user_b", "content": "Initial content of doc2."},
}


def edit_doc(u_id: str, u_role: str, doc_id: str, doc_owner: str, new_body: str) -> str:
    """
    Edit the content of a document if the caller is authorized.

    Parameters
    ----------
    u_id : str
        ID of the user attempting to make the update.
    u_role : str
        Role of the user (e.g., 'viewer', 'editor').
    doc_id : str
        ID of the document to modify.
    doc_owner : str
        Expected owner ID for verification purposes.  This is a safety check
        to prevent tampering with the `owner_id` field.
    new_body : str
        New content to be stored in the document.

    Returns
    -------
    str
        The updated content if the operation succeeds.

    Raises
    ------
    ValueError
        If `doc_id` does not exist in the system.
    PermissionError
        If the user is not authorized to edit the document.

    Notes
    -----
    The function enforces proper access control:
        * Only users with role 'editor' or the document owner can modify.
        * The `doc_owner` argument is verified against the stored value
          to guard against malicious input.
    """
    # 1. Verify that the document exists
    if doc_id not in DOCUMENTS_DB:
        raise ValueError(f"Document ID '{doc_id}' does not exist.")

    doc = DOCUMENTS_DB[doc_id]

    # 2. Validate the reported owner matches the stored owner
    if doc_owner != doc["owner_id"]:
        raise PermissionError("Document ownership mismatch. Edit denied.")

    # 3. Authorization check
    is_owner = u_id == doc["owner_id"]
    is_editor_role = u_role.lower() == "editor"

    if not (is_owner or is_editor_role):
        raise PermissionError(
            f"User '{u_id}' with role '{u_role}' is not authorized to edit document '{doc_id}'."
        )

    # 4. Perform the update
    doc["content"] = new_body

    return doc["content"]