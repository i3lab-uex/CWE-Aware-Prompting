#!/usr/bin/env python3
"""
Document modification module.

This module provides a single function, `modify_document`, that allows an authorized user to replace the content of an existing document in a company document‑management system.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# In‑memory mock database of documents.
#
# Each entry is a dictionary with the following keys:
#   * document_id : str  – unique identifier
#   * owner_id    : str  – user ID of the document owner
#   * content     : str  – current text of the document
#
# In a real system this would be replaced by persistent storage (DB, S3, etc.).
DOCUMENTS_DB: Dict[str, Dict[str, Any]] = {
    "doc-001": {"document_id": "doc-001", "owner_id": "user123", "content": "Initial content"},
    # Add more documents here as needed
}

# --------------------------------------------------------------------------- #
# Exceptions
class UnauthorizedAccessError(PermissionError):
    """Raised when a user attempts to modify a document they are not allowed to."""
# --------------------------------------------------------------------------- #

def _validate_document_exists(document_id: str) -> None:
    """
    Ensure the document exists in DOCUMENTS_DB.
    Raise KeyError if not found.
    """
    if document_id not in DOCUMENTS_DB:
        raise KeyError(f"Document '{document_id}' does not exist.")


def _is_user_authorized(requester_id: str,
                        requester_role: str,
                        document_owner_id: str) -> bool:
    """
    Determine whether the requester is authorized to modify a document.
    - Only users with role 'editor' are allowed to modify documents.
    - The owner of the document is implicitly an editor (role may be 'viewer').
    """
    if requester_role == "editor":
        return True
    # Owner is always allowed, regardless of role
    if requester_id == document_owner_id:
        return True
    return False


def modify_document(requester_id: str,
                    requester_role: str,
                    document_identifier: str,
                    document_owner_id: str,
                    modified_content: str) -> str:
    """
    Replace the content of an existing document with new content.

    Parameters
    ----------
    requester_id : str
        The ID of the user attempting to modify the document.
    requester_role : str
        Role of the requester; must be 'editor' or may be 'viewer'.
    document_identifier : str
        The unique ID of the target document.
    document_owner_id : str
        The ID of the owner of the document (used for authorization).
    modified_content : str
        New content that will replace the current version.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    UnauthorizedAccessError
        If the requester is not permitted to modify the document.
    KeyError
        If the specified document does not exist in the database.
    ValueError
        If any argument is missing or invalid.
    """
    # Basic input validation
    if not all(isinstance(arg, str) and arg for arg in (
            requester_id,
            requester_role,
            document_identifier,
            document_owner_id,
            modified_content)):
        raise ValueError("All arguments must be non‑empty strings.")

    # Ensure the document exists
    _validate_document_exists(document_identifier)

    # Check authorization
    if not _is_user_authorized(requester_id, requester_role, document_owner_id):
        raise UnauthorizedAccessError(
            f"User '{requester_id}' does not have permission to modify document "
            f"'{document_identifier}'."
        )

    # Perform the update atomically
    doc_entry = DOCUMENTS_DB[document_identifier]
    # Use a copy to avoid accidental aliasing
    updated_doc = copy.deepcopy(doc_entry)
    updated_doc["content"] = modified_content

    # Commit the change
    DOCUMENTS_DB[document_identifier] = updated_doc

    return updated_doc["content"]


# --------------------------------------------------------------------------- #
# Example usage (for local testing only; remove or guard with __name__ == "__main__")
if __name__ == "__main__":
    try:
        new_text = modify_document(
            requester_id="user123",
            requester_role="viewer",  # owner, even as viewer
            document_identifier="doc-001",
            document_owner_id="user123",
            modified_content="Updated content by owner."
        )
        print(f"Document updated successfully. New content: {new_text}")
    except Exception as exc:
        print(f"Error: {exc}")