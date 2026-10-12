# -*- coding: utf-8 -*-
"""
Document modification utility for a corporate document management platform.
"""

from typing import Dict

# Sample in-memory database; in production this would be replaced by a persistent store.
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Initial content"},
    # Add more documents as needed.
}


def modify_document(user_id: str, role: str, doc_id: str, doc_owner: str, new_data: str) -> str:
    """
    Update the content of a document if the user has sufficient privileges.

    Parameters
    ----------
    user_id : str
        The ID of the user attempting the modification.
    role : str
        The user's role. Expected values: 'viewer' or 'editor'.
    doc_id : str
        The unique identifier of the target document.
    doc_owner : str
        The owner ID stored in the database for this document.
    new_data : str
        The content that should replace the current document body.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the document.
    KeyError
        If the specified `doc_id` does not exist in the database.
    ValueError
        If an unsupported role is supplied.

    Notes
    -----
    This function implements proper access control (CWE-284) by ensuring that only
    users with the 'editor' role and who are also the owner of the document may
    modify its content. All other users receive a PermissionError.
    """
    # Validate role input
    allowed_roles = {"viewer", "editor"}
    if role not in allowed_roles:
        raise ValueError(f"Unsupported role '{role}'. Allowed roles: {allowed_roles}")

    # Ensure the document exists
    if doc_id not in DOCUMENTS_DB:
        raise KeyError(f"Document with id '{doc_id}' does not exist.")

    # Check ownership
    if role == "editor" and user_id != doc_owner:
        raise PermissionError("Editors must be the owner of the document to modify it.")

    # Viewers are never allowed to edit
    if role == "viewer":
        raise PermissionError("Viewers do not have permission to modify documents.")

    # Perform the update
    DOCUMENTS_DB[doc_id]["content"] = new_data

    return DOCUMENTS_DB[doc_id]["content"]