# -*- coding: utf-8 -*-
"""
Simple in‑memory document management module.

The `modify_document` function checks that the requester has edit
permissions and then replaces the document's content.
"""

from __future__ import annotations

# Example in‑memory database
DOCUMENTS_DB: dict[str, dict] = {
    "doc_001": {"document_id": "doc_001", "owner_id": "user_a", "content": "Initial content."},
    "doc_002": {"document_id": "doc_002", "owner_id": "user_b", "content": "Another document."},
}

def modify_document(
    requester_id: str,
    requester_role: str,
    document_identifier: str,
    document_owner_id: str,
    modified_content: str,
) -> str:
    """
    Replace the content of an existing document if the requester is authorized.

    Parameters
    ----------
    requester_id : str
        The ID of the user attempting to modify the document.
    requester_role : str
        Role of the user ('viewer' or 'editor').
    document_identifier : str
        The unique ID of the target document.
    document_owner_id : str
        The owner ID stored in the database for comparison.
    modified_content : str
        New content to replace the current document content.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    PermissionError
        If the user does not have edit rights or is not the owner.
    KeyError
        If the document identifier is not present in the database.
    ValueError
        If `requester_role` is not a recognized role.
    """
    # Validate role
    if requester_role not in {"viewer", "editor"}:
        raise ValueError(f"Unrecognized role: {requester_role!r}")

    # Ensure document exists
    try:
        doc = DOCUMENTS_DB[document_identifier]
    except KeyError as exc:
        raise KeyError(f"Document {document_identifier!r} not found.") from exc

    # Check ownership
    if doc["owner_id"] != document_owner_id:
        raise ValueError("Provided owner ID does not match the database record.")

    # Permission check: only editors can modify, and they must be the owner
    if requester_role != "editor" or requester_id != document_owner_id:
        raise PermissionError("Insufficient permissions to modify the document.")

    # Perform modification
    doc["content"] = modified_content

    return doc["content"]