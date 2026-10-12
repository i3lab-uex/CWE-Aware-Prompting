#!/usr/bin/env python3
"""
Document modification helper with strict access control.
"""

from typing import Dict

# Example in‑memory document store. In production this would be a database.
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    # document_id : { 'document_id': str, 'owner_id': str, 'content': str }
    "doc1": {"document_id": "doc1", "owner_id": "userA", "content": "Original content"},
    # Add more documents as needed.
}


def alter_document(
    modifier_id: str,
    user_role: str,
    doc_identifier: str,
    creator_id: str,
    updated_content: str,
) -> str:
    """
    Update a document's content if the caller has appropriate permissions.

    Parameters
    ----------
    modifier_id : str
        ID of the user attempting the modification.
    user_role : str
        Role of the user; must be either 'viewer' or 'editor'.
    doc_identifier : str
        Unique ID of the document to modify.
    creator_id : str
        Expected owner ID; used as a secondary check for consistency.
    updated_content : str
        New content to store in the document.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the document.
    KeyError
        If the document does not exist in the database.
    ValueError
        If an unsupported role is provided.
    """

    # 1. Validate the document exists.
    if doc_identifier not in DOCUMENTS_DB:
        raise KeyError(f"Document '{doc_identifier}' not found.")

    doc = DOCUMENTS_DB[doc_identifier]

    # 2. Validate that the creator_id matches the stored owner_id.
    if doc["owner_id"] != creator_id:
        raise ValueError("Creator ID mismatch. Possible tampering detected.")

    # 3. Authorization check.
    # Only users with role 'editor' or the document owner may modify.
    if user_role not in {"viewer", "editor"}:
        raise ValueError(f"Unsupported role: {user_role}")

    if user_role == "viewer":
        # Viewers cannot modify.
        raise PermissionError("User does not have permission to edit the document.")

    if modifier_id != creator_id and user_role == "editor":
        # Editors must also be the owner; alternatively, a separate 'admin' role could
        # override this check. For now, enforce ownership.
        raise PermissionError("Only the document owner can edit the content.")

    # 4. Perform the update.
    doc["content"] = updated_content

    # Return the new content for confirmation.
    return doc["content"]