# -*- coding: utf-8 -*-

"""
Document modification helper with proper access control.
"""

from typing import Dict

# Mock database of documents
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Original content of doc1."},
    "doc2": {"document_id": "doc2", "owner_id": "user456", "content": "Original content of doc2."},
    # Add more documents as needed
}


def alter_document(
    modifier_id: str,
    user_role: str,
    doc_identifier: str,
    creator_id: str,
    updated_content: str,
) -> str:
    """
    Update a document's content if the user is authorized.

    Parameters
    ----------
    modifier_id : str
        ID of the user attempting the modification.
    user_role : str
        Role of the user; must be either 'viewer' or 'editor'.
    doc_identifier : str
        Unique ID of the document to modify.
    creator_id : str
        Expected owner ID for verification (redundant but ensures consistency).
    updated_content : str
        New content that will replace the existing document content.

    Returns
    -------
    str
        The updated content of the document after a successful modification.

    Raises
    ------
    PermissionError
        If the user does not have sufficient permissions.
    KeyError
        If the specified document does not exist in the database.
    ValueError
        If an invalid role is provided.

    Notes
    -----
    - Only users with the 'editor' role or the document owner are allowed to modify.
    - The function performs a strict equality check on user IDs and roles to prevent
      accidental privilege escalation (CWE-284).
    """
    # Validate role
    if user_role not in {"viewer", "editor"}:
        raise ValueError(f"Invalid role '{user_role}'. Allowed roles: 'viewer', 'editor'.")

    # Fetch the document
    try:
        doc = DOCUMENTS_DB[doc_identifier]
    except KeyError as exc:
        raise KeyError(f"Document '{doc_identifier}' not found.") from exc

    # Verify ownership consistency
    if doc["owner_id"] != creator_id:
        raise ValueError("Creator ID does not match the document's owner.")

    # Access control: allow only editors or owners
    if user_role != "editor" and modifier_id != creator_id:
        raise PermissionError("User does not have permission to modify this document.")

    # Perform the update
    doc["content"] = updated_content

    return doc["content"]