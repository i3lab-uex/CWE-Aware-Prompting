# -*- coding: utf-8 -*-

"""
Document Management System – Modification Function

This module provides a single function, `modify_document`, which safely updates the
content of an existing document.  It performs strict authorization checks to
prevent CWE‑863 (Incorrect Authorization) and other security weaknesses.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Mock database – in a real system this would be replaced by a persistent store
DOCUMENTS_DB: dict[str, dict[str, str]] = {
    # Example entries:
    "doc-001": {"document_id": "doc-001", "owner_id": "user-123", "content": "Original content."},
    "doc-002": {"document_id": "doc-002", "owner_id": "user-456", "content": "Another document."},
}


def modify_document(
    requester_id: str,
    requester_role: str,
    document_identifier: str,
    document_owner_id: str,
    modified_content: str,
) -> str:
    """
    Update the content of an existing document after verifying authorization.

    Parameters
    ----------
    requester_id : str
        The ID of the user attempting to modify the document.
    requester_role : str
        Role of the user – must be either 'viewer' or 'editor'.
    document_identifier : str
        Unique ID of the target document.
    document_owner_id : str
        The expected owner ID for the document.  This is used to validate that
        the supplied `document_identifier` matches an existing entry.
    modified_content : str
        New content that will replace the current document text.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    KeyError
        If the specified document does not exist in ``DOCUMENTS_DB``.
    PermissionError
        If the requester is not authorized to modify the document.
    ValueError
        If an unsupported role is supplied or if the owner ID does not match.
    """

    # ----------------------------------------------------------------------- #
    # 1. Validate role
    if requester_role not in {"viewer", "editor"}:
        raise ValueError(f"Unsupported role '{requester_role}'. Only 'viewer' and 'editor' are allowed.")

    # ----------------------------------------------------------------------- #
    # 2. Fetch the document from the database
    try:
        doc = DOCUMENTS_DB[document_identifier]
    except KeyError as exc:
        raise KeyError(f"Document '{document_identifier}' not found.") from exc

    # ----------------------------------------------------------------------- #
    # 3. Ensure the owner ID matches
    if doc["owner_id"] != document_owner_id:
        raise ValueError("Provided owner ID does not match the stored owner of the document.")

    # ----------------------------------------------------------------------- #
    # 4. Authorization check – only editors who own the doc may modify
    if requester_role != "editor" or requester_id != document_owner_id:
        raise PermissionError("You do not have permission to modify this document.")

    # ----------------------------------------------------------------------- #
    # 5. Perform the update
    doc["content"] = modified_content

    return doc["content"]