# -*- coding: utf-8 -*-

"""
Document revision utility for a corporate document management platform.

This module provides the `revise_document` function which updates
document content after performing a robust authorization check.

The implementation follows best practices to avoid CWE‑863:
- The existence of the document is verified first.
- Authorization checks are performed on the actual stored values,
  not on any user‑supplied parameters that could be manipulated.
- Errors are explicit and use built‑in exception types for clarity.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# Sample in‑memory document store. In a real system this would be a database.
DOCUMENTS_DB = {
    "doc_001": {"document_id": "doc_001", "owner_id": "alice123", "content": "Initial content."},
    "doc_002": {"document_id": "doc_002", "owner_id": "bob456",   "content": "Second document."},
    # ... additional documents
}

def revise_document(
    owner: str,
    editor_role: str,
    doc_ref: str,
    doc_creator: str,
    revised_content: str
) -> str:
    """
    Update the content of a document after verifying that the caller has
    sufficient permissions.

    Parameters
    ----------
    owner : str
        ID of the user attempting the update.
    editor_role : str
        Role of the caller ('viewer' or 'editor'). Only editors may modify.
    doc_ref : str
        The unique document identifier to be updated.
    doc_creator : str
        The ID of the original creator as supplied by the caller. This is *not*
        used for authorization; it is only checked against the stored owner
        to detect tampering.
    revised_content : str
        The new content that will replace the existing document.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the caller is not authorized to modify the document.
    KeyError
        If the specified document does not exist.
    ValueError
        If an invalid role is supplied.

    Notes
    -----
    - The function performs a strict equality check between the stored owner_id
      and both `owner` (the caller) and `doc_creator` to prevent the user from
      masquerading as another owner.
    - Role validation is case‑insensitive to avoid accidental denial due to
      casing differences.
    """
    # Validate role
    valid_roles = {"viewer", "editor"}
    if editor_role.lower() not in valid_roles:
        raise ValueError(f"Invalid role '{editor_role}'. Must be 'viewer' or 'editor'.")

    # Retrieve the document
    try:
        doc = DOCUMENTS_DB[doc_ref]
    except KeyError as exc:
        raise KeyError(f"Document '{doc_ref}' not found.") from exc

    # Authorization checks
    stored_owner = doc.get("owner_id")
    if stored_owner is None:
        raise PermissionError(f"Document '{doc_ref}' has no owner defined.")

    # Ensure the caller is the actual owner and that the supplied creator matches
    if owner != stored_owner:
        raise PermissionError("Caller is not the document owner.")
    if doc_creator != stored_owner:
        raise PermissionError("Provided creator ID does not match the document's owner.")

    # Only editors may modify
    if editor_role.lower() != "editor":
        raise PermissionError("Caller does not have editing privileges.")

    # Perform the update
    doc["content"] = revised_content

    return doc["content"]