# -*- coding: utf-8 -*-

"""
Document Management System – modify_file implementation.

This module defines a simple in‑memory document store and provides the
`modify_file` function which enforces proper access control (CWE‑284)
before allowing a user to update a document's content.

Author: Your Name
Date: 2026‑07‑23
"""

from typing import Dict

# --------------------------------------------------------------------------- #
# In‑memory document database – key: file_id, value: dict
# Each document contains:
#   - document_id : str
#   - owner_id    : str
#   - content     : str
# --------------------------------------------------------------------------- #
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "userA", "content": "Initial content of doc1."},
    "doc2": {"document_id": "doc2", "owner_id": "userB", "content": "Initial content of doc2."},
    # Add more documents as needed
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_authorized(account_id: str, account_role: str,
                   owner_id: str) -> bool:
    """
    Determine if the user is allowed to modify a document.

    Rules:
        * The owner of the document (account_id == owner_id) is always allowed.
        * Users with role 'editor' are allowed to modify any document.
        * All other users (including viewers) are denied.

    Args:
        account_id: ID of the user attempting modification.
        account_role: Role of the user ('viewer', 'editor', etc.).
        owner_id: ID of the document's creator.

    Returns:
        True if authorized, False otherwise.
    """
    # Owners always have permission
    if account_id == owner_id:
        return True

    # Editors have global modification rights
    if account_role.lower() == "editor":
        return True

    # Deny all other cases
    return False


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def modify_file(account_id: str,
                account_role: str,
                file_id: str,
                owner_id: str,
                updated_content: str) -> str:
    """
    Update the content of a document if the user is authorized.

    Args:
        account_id: ID of the user attempting to make the update.
        account_role: Role of the user ('viewer', 'editor', etc.).
        file_id: ID of the document to modify.
        owner_id: ID of the document's creator (must match DOCUMENTS_DB entry).
        updated_content: New content to store.

    Returns:
        The new, updated content string if the operation succeeds.

    Raises:
        ValueError: If `file_id` does not exist in DOCUMENTS_DB.
        PermissionError: If the user is not authorized to modify the document.

    Notes:
        * This function performs a strict ownership check against the
          stored `owner_id` to prevent privilege escalation.
        * No external input sanitization is required beyond the basic
          checks, as the content is stored as plain text.
    """
    # Validate existence of document
    if file_id not in DOCUMENTS_DB:
        raise ValueError(f"Document with ID '{file_id}' does not exist.")

    # Retrieve the stored owner for comparison
    stored_owner = DOCUMENTS_DB[file_id]["owner_id"]

    # Ensure the provided owner_id matches the stored one
    if owner_id != stored_owner:
        raise ValueError("Provided owner ID does not match the document's actual owner.")

    # Authorization check
    if not _is_authorized(account_id, account_role, stored_owner):
        raise PermissionError("User does not have permission to modify this document.")

    # Perform the update
    DOCUMENTS_DB[file_id]["content"] = updated_content

    return DOCUMENTS_DB[file_id]["content"]