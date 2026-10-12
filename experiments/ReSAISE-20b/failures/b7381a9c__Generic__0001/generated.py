# -*- coding: utf-8 -*-
"""
Document management helper – update_document

The module defines a global in‑memory database `DOCUMENTS_DB` and the
function `update_document`.  The function checks that the target document
exists, verifies that the caller is authorised (either an editor or the
document owner), updates the document's content, and returns the new
content.  A `ValueError` is raised when the document cannot be found.
"""

from __future__ import annotations

# A very small, in‑memory representation of a document database.
# In practice this would be backed by a real database or persistence layer.
DOCUMENTS_DB: dict[str, dict[str, str]] = {
    "doc-001": {"document_id": "doc-001", "owner_id": "alice", "content": "Initial content."},
    "doc-002": {"document_id": "doc-002", "owner_id": "bob",   "content": "Another document."},
    # Add more documents as needed.
}


def update_document(
    user_id: str,
    user_role: str,
    document_id: str,
    owner_id: str,
    new_content: str,
) -> str:
    """
    Update the content of a document in the system.

    Parameters
    ----------
    user_id : str
        The ID of the user attempting to perform the update.
    user_role : str
        Role of the user (e.g., 'viewer', 'editor').
    document_id : str
        The identifier of the document to update.
    owner_id : str
        The ID of the user who owns the document.  This should match the
        'owner_id' stored in `DOCUMENTS_DB` for consistency.
    new_content : str
        The new text to replace the current document content.

    Returns
    -------
    str
        The updated content of the document if the operation succeeded.

    Raises
    ------
    ValueError
        If the document does not exist in `DOCUMENTS_DB`.
    PermissionError
        If the user is not authorised to update the document.
    """
    # 1. Verify that the document exists
    doc = DOCUMENTS_DB.get(document_id)
    if doc is None:
        raise ValueError(f"Document '{document_id}' does not exist.")

    # 2. Verify that the provided owner_id matches the stored owner
    if doc["owner_id"] != owner_id:
        raise ValueError(
            f"Provided owner ID '{owner_id}' does not match the document's stored owner."
        )

    # 3. Authorization check
    # Allow update if the user is an editor or the owner of the document.
    if not (user_role == "editor" or user_id == doc["owner_id"]):
        raise PermissionError(
            f"User '{user_id}' with role '{user_role}' is not authorised to update document '{document_id}'."
        )

    # 4. Update the content safely
    # In a real system, you would also handle concurrency (locking),
    # validation of the content format, and logging.
    doc["content"] = new_content

    return doc["content"]