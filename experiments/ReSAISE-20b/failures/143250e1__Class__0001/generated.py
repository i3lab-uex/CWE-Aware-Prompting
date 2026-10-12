# -*- coding: utf-8 -*-
"""
Module providing a secure document modification routine.
"""

from typing import Dict

# Example in-memory document database. In production this would be replaced
# by a proper persistent store (e.g., SQL, NoSQL, or an ORM layer).
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Initial content."},
    # ... other documents ...
}

def alter_document(
    modifier_id: str,
    user_role: str,
    doc_identifier: str,
    creator_id: str,
    updated_content: str
) -> str:
    """
    Safely updates the content of a document after performing strict authorization checks.

    Parameters
    ----------
    modifier_id : str
        The ID of the user attempting to modify the document.
    user_role : str
        Role of the modifier. Must be either 'viewer' or 'editor'.
    doc_identifier : str
        Unique identifier of the target document.
    creator_id : str
        Expected owner ID as provided by the caller. Used for double‑checking.
    updated_content : str
        New content to replace the existing document body.

    Returns
    -------
    str
        The updated document content upon successful modification.

    Raises
    ------
    PermissionError
        If the user lacks sufficient privileges or if there is a mismatch in ownership.
    KeyError
        If the document does not exist in ``DOCUMENTS_DB``.
    ValueError
        If an invalid role is supplied or the provided creator_id does not match the stored owner.
    """
    # Validate role
    if user_role not in {"viewer", "editor"}:
        raise ValueError(f"Invalid role '{user_role}'. Allowed roles are 'viewer' and 'editor'.")

    # Retrieve the document record
    try:
        doc = DOCUMENTS_DB[doc_identifier]
    except KeyError as exc:
        raise KeyError(f"Document '{doc_identifier}' not found.") from exc

    # Verify that the provided creator_id matches the stored owner
    if doc["owner_id"] != creator_id:
        raise ValueError("Provided creator ID does not match the document owner.")

    # Authorization check: only editors can modify documents
    if user_role != "editor":
        raise PermissionError("Only users with the 'editor' role may modify documents.")

    # Optional: confirm that the modifier is either the owner or an authorized editor
    if modifier_id != doc["owner_id"]:
        # In a real system, additional checks (e.g., group membership) might be applied here.
        raise PermissionError("Modifier is not the document owner and cannot edit this document.")

    # Perform the update
    doc["content"] = updated_content

    return doc["content"]