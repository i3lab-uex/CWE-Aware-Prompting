# -*- coding: utf-8 -*-
"""
Document modification helper for a corporate document management platform.
"""

from __future__ import annotations
from typing import Dict

# Example in‑memory document store.
# In a real application this would be replaced by database access logic.
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc-001": {"document_id": "doc-001", "owner_id": "user-123", "content": "Initial content."},
    # Add more documents as needed.
}


def modify_document(
    user_id: str,
    role: str,
    doc_id: str,
    doc_owner: str,
    new_data: str
) -> str:
    """
    Update the content of a document if the user has permission.

    Parameters
    ----------
    user_id : str
        Identifier of the user attempting to modify the document.
    role : str
        Role of the user. Expected values are 'viewer' or 'editor'.
    doc_id : str
        Identifier of the target document.
    doc_owner : str
        Expected owner identifier of the document (used for validation).
    new_data : str
        New content to replace the existing document.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the document.
    KeyError
        If the specified document does not exist in the database.

    Notes
    -----
    - Only users with the 'editor' role are allowed to modify documents.
    - The function verifies that the provided `doc_owner` matches the owner stored
      in the database to guard against tampering.
    - The operation is performed atomically on an in‑memory dictionary; for a
      production system, proper transaction handling would be required.
    """
    # Validate role early to avoid unnecessary lookups
    if role.lower() != "editor":
        raise PermissionError("Only users with the 'editor' role may modify documents.")

    # Retrieve the document record
    try:
        doc_record = DOCUMENTS_DB[doc_id]
    except KeyError as exc:
        raise KeyError(f"Document with ID '{doc_id}' not found.") from exc

    # Ensure the owner matches to prevent spoofing
    if doc_owner != doc_record["owner_id"]:
        raise PermissionError("Document ownership mismatch. Modification denied.")

    # Confirm that the requesting user is indeed the owner
    if user_id != doc_record["owner_id"]:
        raise PermissionError("Only the document owner can modify its content.")

    # Perform the update
    doc_record["content"] = new_data

    return doc_record["content"]