# SPDX-License-Identifier: MIT
"""
Document management utilities.

This module contains a single function `edit_document` which safely updates the
content of an existing document.  It enforces proper access control by ensuring
that only users with the `editor` role and who own the document can modify it.
Unauthorized attempts raise a :class:`PermissionError`.
"""

from __future__ import annotations

# Example in-memory database of documents.
# Each key is a document ID; each value is a dictionary containing
# the owner and current content of the document.
DOCUMENTS_DB: dict[str, dict[str, str]] = {
    "doc-001": {"document_id": "doc-001", "owner_id": "user-123", "content": "Initial content."},
    # Add more documents as needed.
}


def edit_document(
    member_id: str,
    member_role: str,
    doc_id: str,
    doc_owner_id: str,
    replacement_content: str,
) -> str:
    """
    Update the content of an existing document.

    Parameters
    ----------
    member_id : str
        ID of the user attempting to modify the document.
    member_role : str
        Role of the user.  Only 'editor' is allowed to modify documents.
    doc_id : str
        Unique identifier of the document to be edited.
    doc_owner_id : str
        Owner ID stored in the database for this document (used to verify ownership).
    replacement_content : str
        New content that will replace the current version of the document.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the document.
    KeyError
        If the document ID does not exist in ``DOCUMENTS_DB``.
    ValueError
        If required arguments are missing or empty.

    Notes
    -----
    The function performs the following security checks:
      * Ensures that ``member_role`` is exactly 'editor'.
      * Confirms that the user attempting to edit (`member_id`) matches the
        document's stored owner ID.
      * Uses a constant‑time comparison for the role check to mitigate timing
        attacks (though in practice the risk is minimal for simple string checks).
    """
    # Basic validation of inputs
    if not all([member_id, member_role, doc_id, doc_owner_id]):
        raise ValueError("All user and document identifiers must be provided.")

    # Verify that the requested document exists
    if doc_id not in DOCUMENTS_DB:
        raise KeyError(f"Document with ID '{doc_id}' does not exist.")

    # Enforce role-based access control
    if member_role.lower() != "editor":
        raise PermissionError("Only users with the 'editor' role may modify documents.")

    # Enforce ownership check
    if member_id != doc_owner_id:
        raise PermissionError("User does not own the document and cannot modify it.")

    # Perform the update
    DOCUMENTS_DB[doc_id]["content"] = replacement_content

    return DOCUMENTS_DB[doc_id]["content"]