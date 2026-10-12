#!/usr/bin/env python3
"""
Document revision utility for a corporate document management platform.
"""

from __future__ import annotations

# Sample in‑memory database. In production this would be replaced by a real DB.
DOCUMENTS_DB: dict[str, dict[str, str]] = {
    # Example entry:
    # "doc123": {"document_id": "doc123", "owner_id": "userA", "content": "Original text"},
}

# Allowed editor roles
ALLOWED_ROLES = {"editor", "viewer"}


def revise_document(
    owner: str,
    editor_role: str,
    doc_ref: str,
    doc_creator: str,
    revised_content: str,
) -> str:
    """
    Update the content of a document if the caller is authorized.

    Parameters
    ----------
    owner : str
        The ID of the user attempting the update.
    editor_role : str
        Role of the caller. Must be either 'viewer' or 'editor'.
    doc_ref : str
        Unique identifier of the document to modify.
    doc_creator : str
        The ID that originally created the document (owner_id in DB).
    revised_content : str
        New content to replace the existing document.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the document.
    KeyError
        If the document does not exist in the database.
    ValueError
        If an unsupported role is provided.

    Notes
    -----
    The function performs strict ownership and role checks to mitigate CWE‑284
    (Improper Access Control). It does not rely on any external authentication
    mechanism; the caller must provide correct identifiers.
    """
    # Validate role
    if editor_role not in ALLOWED_ROLES:
        raise ValueError(f"Unsupported role: {editor_role!r}")

    # Fetch the document from the database
    try:
        doc = DOCUMENTS_DB[doc_ref]
    except KeyError as exc:
        raise KeyError(f"Document {doc_ref!r} not found") from exc

    # Verify that the provided creator matches the stored owner_id
    if doc_creator != doc["owner_id"]:
        raise PermissionError("Provided creator ID does not match document owner.")

    # Authorization check: allow if caller is the owner or has editor role
    if not (owner == doc_creator or editor_role == "editor"):
        raise PermissionError("User does not have permission to modify this document.")

    # Perform the update
    doc["content"] = revised_content

    # Return the updated content
    return doc["content"]