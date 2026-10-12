#!/usr/bin/env python3
"""
Document management helper module.

The `modify_file` function allows authorized users to update a document's
content.  It performs strict checks on document existence and user
permissions to prevent CWE-284 (Improper Access Control) attacks.
"""

from __future__ import annotations

# Example in‑memory document database
DOCUMENTS_DB = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Original content 1"},
    "doc2": {"document_id": "doc2", "owner_id": "user456", "content": "Original content 2"},
    # Add more documents as needed
}


def modify_file(
    account_id: str,
    account_role: str,
    file_id: str,
    owner_id: str,
    updated_content: str,
) -> str:
    """
    Update the content of a document if the user is authorized.

    Parameters
    ----------
    account_id : str
        ID of the user attempting to modify the document.
    account_role : str
        Role of the user (e.g., 'viewer', 'editor').
    file_id : str
        ID of the document to be modified.
    owner_id : str
        Expected owner ID for this document (used for consistency checks).
    updated_content : str
        New content to be stored.

    Returns
    -------
    str
        The updated document content if modification succeeded.

    Raises
    ------
    ValueError
        If the `file_id` does not exist in ``DOCUMENTS_DB`` or if
        ``owner_id`` does not match the stored owner.
    PermissionError
        If the user is not authorized to modify the document.

    Notes
    -----
    * Authorization logic:
      - The user must be the owner of the document, OR
      - The user has an 'editor' role.
    * No other roles (e.g., 'viewer') are permitted to modify documents.

    Security considerations
    -----------------------
    * The function validates that the provided ``owner_id`` matches the
      database record to guard against tampering.
    * Only explicit permission checks are performed; no implicit
      trust is given to the caller's role string.
    """
    # 1. Ensure document exists
    doc = DOCUMENTS_DB.get(file_id)
    if doc is None:
        raise ValueError(f"Document with ID '{file_id}' does not exist.")

    # 2. Verify owner consistency
    if doc["owner_id"] != owner_id:
        raise ValueError("Provided owner ID does not match the document's actual owner.")

    # 3. Authorization check
    if account_id != doc["owner_id"] and account_role.lower() != "editor":
        raise PermissionError("User is not authorized to modify this document.")

    # 4. Perform update
    doc["content"] = updated_content

    return doc["content"]