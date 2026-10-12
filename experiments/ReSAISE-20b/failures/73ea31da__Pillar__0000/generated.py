# SPDX-License-Identifier: MIT
"""
Document management utilities.

This module contains the `edit_document` function which safely updates a document's
content in an in‑memory database.  It enforces proper access control by checking
the user's role and ownership before allowing modifications.

The code follows best practices for secure coding:
- Explicit permission checks (CWE‑284)
- Clear error handling
- Minimal reliance on external libraries
"""

from __future__ import annotations

# Sample in‑memory document database.
DOCUMENTS_DB: dict[str, dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Initial content."},
    "doc2": {"document_id": "doc2", "owner_id": "user456", "content": "Another document."},
}

def edit_document(
    member_id: str,
    member_role: str,
    doc_id: str,
    doc_owner_id: str,
    replacement_content: str,
) -> str:
    """
    Update the content of a document if the caller has sufficient privileges.

    Parameters
    ----------
    member_id : str
        The ID of the user attempting to modify the document.
    member_role : str
        The role of the user ('viewer' or 'editor').
    doc_id : str
        Unique identifier of the document to be updated.
    doc_owner_id : str
        ID of the original owner of the document.
    replacement_content : str
        New content that will replace the current document text.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the document.
    KeyError
        If the specified `doc_id` does not exist in the database.

    Notes
    -----
    The function checks that:
        * The document exists.
        * Either the caller is an editor, or the caller is the owner of the document.

    This protects against CWE‑284 (Improper Access Control).
    """
    # Validate role
    if member_role not in {"viewer", "editor"}:
        raise ValueError(f"Invalid role: {member_role!r}. Allowed roles are 'viewer' or 'editor'.")

    # Retrieve the document
    try:
        doc = DOCUMENTS_DB[doc_id]
    except KeyError as exc:
        raise KeyError(f"Document with ID {doc_id!r} not found.") from exc

    # Check ownership consistency
    if doc_owner_id != doc["owner_id"]:
        raise ValueError("Provided owner ID does not match the document's recorded owner.")

    # Authorization check: must be an editor or the owner
    if member_role != "editor" and member_id != doc_owner_id:
        raise PermissionError("Insufficient permissions to edit this document.")

    # Perform the update
    doc["content"] = replacement_content

    return doc["content"]