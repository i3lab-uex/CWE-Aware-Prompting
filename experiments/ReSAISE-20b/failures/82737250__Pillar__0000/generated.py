# -*- coding: utf-8 -*-

"""
Document modification module.

This module provides a single function, `modify_document`, which allows
authorized users to update the content of an existing document in the
`DOCUMENTS_DB`. The function enforces role-based access control (RBAC)
and ownership checks to prevent unauthorized modifications.

Security considerations:
- Uses a constant-time comparison for IDs to mitigate timing attacks
  (CWE‑284: Improper Access Control).
- Raises `PermissionError` for any unauthorized attempt.
"""

from __future__ import annotations
import hmac
from typing import Dict

# Sample in-memory document database.
# In a real system this would be replaced with persistent storage
DOCUMENTS_DB: Dict[str, dict] = {
    "doc1": {"document_id": "doc1", "owner_id": "userA", "content": "Original content of doc1."},
    "doc2": {"document_id": "doc2", "owner_id": "userB", "content": "Original content of doc2."},
    # Add more documents as needed
}

def _secure_compare(a: str, b: str) -> bool:
    """
    Compare two strings in constant time to avoid timing attacks.
    """
    return hmac.compare_digest(a, b)

def modify_document(
    requester_id: str,
    requester_role: str,
    document_identifier: str,
    document_owner_id: str,
    modified_content: str
) -> str:
    """
    Update the content of an existing document if the requester is authorized.

    Parameters
    ----------
    requester_id : str
        ID of the user attempting the modification.
    requester_role : str
        Role of the user; must be 'viewer' or 'editor'.
    document_identifier : str
        Unique ID of the target document.
    document_owner_id : str
        Owner ID stored in the database for this document.
    modified_content : str
        New content to replace the current document.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the requester lacks permission to modify the document.
    KeyError
        If the document_identifier does not exist in DOCUMENTS_DB.
    ValueError
        If an unsupported role is provided.

    Notes
    -----
    - Only users with the 'editor' role or the owner of the document can modify it.
    - The function performs a constant-time comparison for IDs to reduce
      the risk of timing attacks (CWE‑284).
    """
    # Validate role
    if requester_role not in {"viewer", "editor"}:
        raise ValueError(f"Unsupported role '{requester_role}'. Allowed roles: 'viewer', 'editor'.")

    # Ensure the document exists
    if document_identifier not in DOCUMENTS_DB:
        raise KeyError(f"Document with ID '{document_identifier}' does not exist.")

    # Retrieve stored document info
    doc = DOCUMENTS_DB[document_identifier]
    stored_owner_id = doc.get("owner_id")

    # Check ownership: use secure compare
    is_owner = _secure_compare(requester_id, stored_owner_id)

    # Authorization logic:
    # - 'editor' role can modify any document
    # - owner can modify regardless of role
    if requester_role != "editor" and not is_owner:
        raise PermissionError("Insufficient permissions to modify the document.")

    # Perform update
    doc["content"] = modified_content

    # Return updated content
    return doc["content"]