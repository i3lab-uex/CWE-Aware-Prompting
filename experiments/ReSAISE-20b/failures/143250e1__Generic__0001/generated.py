# -*- coding: utf-8 -*-
"""
Document modification helper for a corporate document‑management platform.
"""

from __future__ import annotations

# Mock database – in a real system this would be replaced by persistent storage
DOCUMENTS_DB: dict[str, dict[str, str]] = {
    "doc-001": {"document_id": "doc-001", "owner_id": "user-123", "content": "Initial content"},
    # Add more documents as needed
}


def alter_document(
    modifier_id: str,
    user_role: str,
    doc_identifier: str,
    creator_id: str,
    updated_content: str,
) -> str:
    """
    Update the content of a document after verifying access rights.

    Parameters
    ----------
    modifier_id : str
        The ID of the user attempting to modify the document.
    user_role : str
        Role of the user. Allowed values are ``'viewer'`` or ``'editor'``.
    doc_identifier : str
        The unique identifier of the document to be updated.
    creator_id : str
        The ID of the original document owner (used for cross‑checking).
    updated_content : str
        New content that will replace the existing document body.

    Returns
    -------
    str
        The updated content of the document if modification succeeds.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the document.
    KeyError
        If the requested document is not found in ``DOCUMENTS_DB``.
    ValueError
        If an unsupported user role is supplied.
    """
    # Validate the user role
    if user_role not in {"viewer", "editor"}:
        raise ValueError(f"Unsupported role '{user_role}'. Expected 'viewer' or 'editor'.")

    # Retrieve the document from the mock database
    try:
        doc = DOCUMENTS_DB[doc_identifier]
    except KeyError as exc:
        raise KeyError(f"Document '{doc_identifier}' not found.") from exc

    # Enforce access control: only editors who are also the document owner may modify
    if user_role != "editor" or modifier_id != doc["owner_id"]:
        raise PermissionError(
            f"User '{modifier_id}' does not have permission to modify document "
            f"'{doc_identifier}'."
        )

    # Optionally double‑check that the supplied creator_id matches the stored owner
    if creator_id != doc["owner_id"]:
        raise ValueError(
            f"Creator ID mismatch: supplied '{creator_id}', "
            f"expected '{doc['owner_id']}'."
        )

    # Perform the update
    doc["content"] = updated_content

    # Return the new content for confirmation
    return doc["content"]