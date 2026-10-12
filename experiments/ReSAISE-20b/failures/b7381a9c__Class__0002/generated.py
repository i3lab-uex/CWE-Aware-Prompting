# -*- coding: utf-8 -*-

"""
Document Management System – Update Functionality

This module provides a single function `update_document` that updates the
content of a document in an in‑memory database after performing proper
authorization checks.  The implementation follows best practices for
access control and error handling to mitigate CWE‑863 (Incorrect
Authorization).

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Sample in‑memory document database.
# In a real system this would be replaced by persistent storage (DB, API, etc.).
# --------------------------------------------------------------------------- #
DOCUMENTS_DB: dict[str, dict[str, str]] = {
    "doc-001": {"document_id": "doc-001", "owner_id": "user-123", "content": "Initial content of doc 1."},
    "doc-002": {"document_id": "doc-002", "owner_id": "user-456", "content": "Initial content of doc 2."},
    # ... add more documents as needed
}

# --------------------------------------------------------------------------- #
# Exception hierarchy for clarity.
# --------------------------------------------------------------------------- #
class AuthorizationError(PermissionError):
    """Raised when a user is not authorized to perform an action."""
    pass


# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #
def update_document(
    user_id: str,
    user_role: str,
    document_id: str,
    owner_id: str,
    new_content: str,
) -> str:
    """
    Update the content of a document after performing authorization checks.

    Parameters
    ----------
    user_id : str
        Identifier of the user attempting the update.
    user_role : str
        Role of the user (e.g., 'viewer', 'editor').
    document_id : str
        Identifier of the target document.
    owner_id : str
        The expected owner identifier for the document.
    new_content : str
        New content to write into the document.

    Returns
    -------
    str
        The updated content of the document if the operation succeeded.

    Raises
    ------
    ValueError
        If the specified `document_id` does not exist in ``DOCUMENTS_DB``.
    AuthorizationError
        If the user is not authorized to update the document.

    Notes
    -----
    - The function first verifies that the document exists.
    - Authorization logic: a user is allowed to update if they are either
      the owner of the document or have an 'editor' role.
    - The `owner_id` argument is cross‑checked against the stored owner
      to guard against tampering or stale data (CWE‑863 mitigation).
    - All checks are performed before any state mutation.
    """
    # 1. Verify document existence
    if document_id not in DOCUMENTS_DB:
        raise ValueError(f"Document '{document_id}' does not exist.")

    doc = DOCUMENTS_DB[document_id]

    # 2. Cross‑check stored owner against provided owner_id
    if doc["owner_id"] != owner_id:
        raise AuthorizationError("Provided owner ID does not match the document's actual owner.")

    # 3. Authorization check
    if user_id != doc["owner_id"] and user_role.lower() != "editor":
        raise AuthorizationError("User is not authorized to update this document.")

    # 4. Perform the update
    doc["content"] = new_content

    return doc["content"]