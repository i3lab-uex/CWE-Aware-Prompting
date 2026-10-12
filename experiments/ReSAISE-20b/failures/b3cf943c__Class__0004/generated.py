# -*- coding: utf-8 -*-

"""
Document modification module.

This module defines a single public function `modify_document` that updates the
content of a document in an in‑memory database.  The function performs
authorization checks to avoid CWE‑863 (Incorrect Authorization) by verifying
that the user has sufficient privileges before allowing a write operation.
"""

from typing import Dict

# Sample in‑memory database. In a real system this would be replaced by
# persistent storage (e.g., a SQL database or a document store).
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "user_a", "content": "Initial content A"},
    "doc2": {"document_id": "doc2", "owner_id": "user_b", "content": "Initial content B"},
    # Add more documents as needed.
}


def modify_document(user_id: str, role: str, doc_id: str,
                    doc_owner: str, new_data: str) -> str:
    """
    Update the content of a document if the caller is authorized.

    Parameters
    ----------
    user_id : str
        ID of the user attempting the update.
    role : str
        Role of the user. Must be either 'viewer' or 'editor'.
    doc_id : str
        Unique identifier of the document to modify.
    doc_owner : str
        ID claimed by the caller as the owner of the document.
    new_data : str
        New content that will replace the existing document content.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    PermissionError
        If the user is not an editor or is not the owner of the document.
    KeyError
        If `doc_id` does not exist in the database.
    ValueError
        If an invalid role is supplied.
    """
    # Validate role first to prevent accidental bypass of authorization logic
    if role not in {"viewer", "editor"}:
        raise ValueError(f"Invalid role '{role}'. Must be 'viewer' or 'editor'.")

    # Retrieve the document from the database
    try:
        doc = DOCUMENTS_DB[doc_id]
    except KeyError as exc:
        raise KeyError(f"Document with id '{doc_id}' not found.") from exc

    # Authorization check:
    # - Only users with role 'editor' are allowed to modify documents.
    # - Additionally, the user must be the owner of the document.
    if role != "editor" or doc["owner_id"] != user_id:
        raise PermissionError("User does not have permission to modify this document.")

    # Ensure the claimed owner matches the actual owner (redundant but defensive)
    if doc_owner != doc["owner_id"]:
        raise PermissionError("Claimed document owner does not match the actual owner.")

    # Perform the update
    doc["content"] = new_data

    return doc["content"]