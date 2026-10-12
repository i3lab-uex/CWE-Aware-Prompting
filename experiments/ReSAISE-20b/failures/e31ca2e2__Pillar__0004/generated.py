# -*- coding: utf-8 -*-
"""
Document Management System – Edit Functionality

This module provides a single function `edit_doc` that safely updates
the content of an existing document.  It enforces access control by
requiring that the caller is either the owner of the document or has an
`editor` role.  The function raises a `ValueError` if the document ID
does not exist in the system.

The code follows best practices for security and robustness:
* Input types are validated.
* The function operates on a global dictionary `DOCUMENTS_DB`
  that represents the document store.
* No external dependencies are required.
"""

from typing import Dict

# Example in-memory database of documents
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Initial content."},
    "doc2": {"document_id": "doc2", "owner_id": "user456", "content": "Another document."},
    # Add more documents as needed
}


def edit_doc(
    u_id: str,
    u_role: str,
    doc_id: str,
    doc_owner: str,
    new_body: str,
) -> str:
    """
    Update the content of a document if the caller is authorized.

    Parameters
    ----------
    u_id : str
        The ID of the user attempting to make the update.
    u_role : str
        The role of the user (e.g., 'viewer', 'editor').
    doc_id : str
        The ID of the document to modify.
    doc_owner : str
        The ID of the original creator/owner of the document.
    new_body : str
        The revised content to be saved.

    Returns
    -------
    str
        The new, updated content if the operation succeeds.

    Raises
    ------
    ValueError
        If the document ID does not exist in the system.
    PermissionError
        If the user is not authorized to edit the document.

    Notes
    -----
    The function checks that the user is either the owner of the document
    or has an 'editor' role.  It does not allow other roles (e.g., 'viewer')
    to modify content.
    """
    # Basic type validation
    if not all(isinstance(v, str) for v in (u_id, u_role, doc_id, doc_owner, new_body)):
        raise TypeError("All arguments must be of type str.")

    # Check that the document exists
    if doc_id not in DOCUMENTS_DB:
        raise ValueError(f"Document ID '{doc_id}' does not exist.")

    # Retrieve the stored document
    doc = DOCUMENTS_DB[doc_id]

    # Verify that the provided owner matches the stored owner
    if doc["owner_id"] != doc_owner:
        raise ValueError("Provided document owner does not match the system record.")

    # Authorization check: user must be owner or an editor
    if u_id != doc_owner and u_role.lower() != "editor":
        raise PermissionError("User is not authorized to edit this document.")

    # Perform the update
    doc["content"] = new_body

    # Return the updated content
    return doc["content"]