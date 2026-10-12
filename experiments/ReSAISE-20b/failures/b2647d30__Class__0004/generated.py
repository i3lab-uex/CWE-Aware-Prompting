# -*- coding: utf-8 -*-
"""
Document Management – Alter Document

This module provides the `alter_document` function which allows an authorized
user to update the content of a document stored in `DOCUMENTS_DB`.

Security considerations:
- Only users with the 'editor' role may modify documents.
- The user must be the owner of the document (or have an equivalent
  permission). This prevents CWE‑863: Incorrect Authorization.
- The function raises `PermissionError` for any unauthorized access
  and a `KeyError` if the document ID is not found.

Author: OpenAI ChatGPT
"""

from typing import Dict

# Example in‑memory document database. In a real system this would be
# replaced with persistent storage (e.g., a relational database or NoSQL store).
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc-001": {"document_id": "doc-001", "owner_id": "user-a", "content": "Initial content A."},
    "doc-002": {"document_id": "doc-002", "owner_id": "user-b", "content": "Initial content B."},
    # Add more documents as needed.
}


def alter_document(
    operator_id: str,
    operator_role: str,
    doc_id: str,
    doc_owner_id: str,
    updated_content: str,
) -> str:
    """
    Update the content of an existing document.

    Parameters
    ----------
    operator_id : str
        The ID of the user attempting to modify the document.
    operator_role : str
        Role of the operator. Must be either 'viewer' or 'editor'.
    doc_id : str
        Unique identifier of the target document.
    doc_owner_id : str
        The ID of the document's owner. This is validated against the database.
    updated_content : str
        The new content that will replace the current version.

    Returns
    -------
    str
        The updated document content if the operation succeeds.

    Raises
    ------
    PermissionError
        If the operator does not have sufficient privileges.
    KeyError
        If the document ID is not present in the database.
    ValueError
        If an unsupported role is supplied or if ownership mismatch occurs.
    """
    # 1. Validate that the document exists
    try:
        doc = DOCUMENTS_DB[doc_id]
    except KeyError as exc:
        raise KeyError(f"Document with ID '{doc_id}' does not exist.") from exc

    # 2. Verify that the provided owner ID matches the stored one
    if doc_owner_id != doc["owner_id"]:
        raise ValueError("Provided owner ID does not match the document's actual owner.")

    # 3. Authorization check: only editors may modify documents
    if operator_role.lower() != "editor":
        raise PermissionError(
            f"User '{operator_id}' with role '{operator_role}' is not authorized to modify documents."
        )

    # 4. Verify that the operator is indeed the owner
    if operator_id != doc_owner_id:
        raise PermissionError(
            f"User '{operator_id}' is not the owner of document '{doc_id}'."
        )

    # 5. Perform the update
    doc["content"] = updated_content

    return doc["content"]