# -*- coding: utf-8 -*-

"""
Document Management System – File Modification Module

This module defines a single public function `modify_file` that allows
authorized users to update the content of an existing document.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# In‑memory document store (for demonstration purposes)
# --------------------------------------------------------------------------- #

DOCUMENTS_DB: Dict[str, Dict[str, Any]] = {
    "doc1": {"document_id": "doc1", "owner_id": "userA", "content": "Initial content of doc1."},
    "doc2": {"document_id": "doc2", "owner_id": "userB", "content": "Initial content of doc2."},
    # Add more documents as needed
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def modify_file(
    account_id: str,
    account_role: str,
    file_id: str,
    owner_id: str,
    updated_content: str,
) -> str:
    """
    Update the content of an existing document.

    Parameters
    ----------
    account_id : str
        The ID of the user attempting to make the update.
    account_role : str
        The role the user holds (e.g., 'viewer', 'editor').
    file_id : str
        The ID of the document the user wants to modify.
    owner_id : str
        The ID of the document's creator (redundant, but required by spec).
    updated_content : str
        The revised content to be saved.

    Returns
    -------
    str
        The new, updated content if the user is authorized.

    Raises
    ------
    ValueError
        If the document ID doesn't exist in the system.
    PermissionError
        If the user is not authorized to modify the document.
    """

    # --------------------------------------------------------------------- #
    # 1. Validate that the requested file exists
    # --------------------------------------------------------------------- #
    document = DOCUMENTS_DB.get(file_id)
    if document is None:
        raise ValueError(f"Document with ID '{file_id}' does not exist.")

    # --------------------------------------------------------------------- #
    # 2. Verify that the provided owner_id matches the stored owner
    # --------------------------------------------------------------------- #
    if document["owner_id"] != owner_id:
        raise ValueError(
            f"Provided owner_id '{owner_id}' does not match the actual owner "
            f"'{document['owner_id']}'."
        )

    # --------------------------------------------------------------------- #
    # 3. Authorisation check
    # --------------------------------------------------------------------- #
    # Only editors or the owner can modify a document.
    is_owner = account_id == document["owner_id"]
    has_edit_permission = account_role.lower() == "editor"

    if not (is_owner or has_edit_permission):
        raise PermissionError(
            f"User '{account_id}' with role '{account_role}' is not authorized "
            "to modify this document."
        )

    # --------------------------------------------------------------------- #
    # 4. Update the content safely
    # --------------------------------------------------------------------- #
    # We copy the document to avoid accidental mutation of references.
    updated_document = copy.deepcopy(document)
    updated_document["content"] = updated_content

    # Persist the change back to the database
    DOCUMENTS_DB[file_id] = updated_document

    # Return the new content as confirmation
    return updated_content


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        new_text = modify_file(
            account_id="userA",
            account_role="viewer",
            file_id="doc1",
            owner_id="userA",
            updated_content="Updated content for doc1.",
        )
        print("Modification successful:", new_text)
    except Exception as exc:
        print(f"Error: {exc}")