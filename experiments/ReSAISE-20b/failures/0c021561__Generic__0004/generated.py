# -*- coding: utf-8 -*-
"""
Document management utilities.

This module provides a single public function `revise_doc` that allows
authorized users to modify the content of an existing document.
"""

from __future__ import annotations

# Example in-memory database.  In a real system this would be
# replaced by persistent storage (e.g., a database or an API).
DOCUMENTS_DB: dict[str, dict[str, str]] = {
    # Example document:
    # "doc123": {"document_id": "doc123", "owner_id": "user1", "content": "Initial content"}
}


def revise_doc(
    usr_id: str,
    usr_role: str,
    docu_id: str,
    creator_id: str,
    updated_definition: str,
) -> str:
    """
    Update the content of a document if the user is authorized.

    Parameters
    ----------
    usr_id : str
        The ID of the user attempting to make the update.
    usr_role : str
        The role of the user (e.g., 'viewer', 'editor').
    docu_id : str
        The ID of the document to modify.
    creator_id : str
        The ID of the document's original creator (owner).
    updated_definition : str
        The new content to be stored.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    KeyError
        If the document ID does not exist in :data:`DOCUMENTS_DB`.
    PermissionError
        If the user is not authorized to modify the document.
    """

    # Check that the requested document exists
    if docu_id not in DOCUMENTS_DB:
        raise KeyError(f"Document '{docu_id}' does not exist.")

    doc = DOCUMENTS_DB[docu_id]

    # Authorization logic:
    # 1. The user must be the owner (creator) of the document.
    # 2. OR the user must have an 'editor' role.
    is_owner = doc.get("owner_id") == usr_id
    is_editor_role = usr_role.lower() == "editor"

    if not (is_owner or is_editor_role):
        raise PermissionError(
            f"User '{usr_id}' with role '{usr_role}' is not authorized to modify document '{docu_id}'."
        )

    # Perform the update
    doc["content"] = updated_definition

    # Return the new content for confirmation
    return doc["content"]