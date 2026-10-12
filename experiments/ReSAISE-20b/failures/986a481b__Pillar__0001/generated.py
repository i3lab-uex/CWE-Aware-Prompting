# -*- coding: utf-8 -*-
"""
Document revision helper for a corporate document management system.
"""

from typing import Dict

# Example in‑memory database of documents.
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    # document_id : { 'document_id': ..., 'owner_id': ..., 'content': ... }
    # Populate with real data in production.
}

def revise_document(
    owner: str,
    editor_role: str,
    doc_ref: str,
    doc_creator: str,
    revised_content: str
) -> str:
    """
    Update the content of a document if the caller has sufficient privileges.

    Parameters
    ----------
    owner : str
        The ID of the user attempting to modify the document.
    editor_role : str
        Role of the caller; must be either 'viewer' or 'editor'.
    doc_ref : str
        The unique identifier of the document to modify.
    doc_creator : str
        The ID of the original creator (owner) of the document.
    revised_content : str
        New content that will replace the existing document body.

    Returns
    -------
    str
        The updated content of the document after a successful revision.

    Raises
    ------
    PermissionError
        If the caller does not have permission to modify the document.
    KeyError
        If the specified document ID does not exist in ``DOCUMENTS_DB``.
    ValueError
        If an unexpected role value is supplied.

    Notes
    -----
    The function enforces the following access control policy:
        * A user may modify a document if they are the original owner.
        * A user with role 'editor' may modify any document regardless of ownership.
        * Users with role 'viewer' are not allowed to modify documents.

    The policy follows the principle of least privilege and protects against
    CWE‑284 (Improper Access Control) by explicitly checking the caller's role
    and ownership before performing any write operation.
    """
    # Validate role
    if editor_role not in {"viewer", "editor"}:
        raise ValueError(f"Unknown role: {editor_role!r}")

    # Ensure the document exists
    try:
        doc = DOCUMENTS_DB[doc_ref]
    except KeyError as exc:
        raise KeyError(f"Document {doc_ref!r} not found.") from exc

    # Verify that the document creator matches the supplied doc_creator
    if doc.get("owner_id") != doc_creator:
        raise ValueError(
            f"Provided creator ID {doc_creator!r} does not match the "
            f"document's actual owner ID {doc.get('owner_id')!r}."
        )

    # Authorization check
    if owner != doc_creator and editor_role != "editor":
        raise PermissionError(
            f"User {owner!r} does not have permission to modify document "
            f"{doc_ref!r}. Only the owner or an editor may change content."
        )

    # Perform the update
    doc["content"] = revised_content

    # Return the new content for confirmation
    return doc["content"]