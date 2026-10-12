# -*- coding: utf-8 -*-
"""
Document management helper – update_document

This module provides a single function `update_document` that performs
an authorised content update on an in‑memory document store.
"""

from __future__ import annotations

# Example in‑memory database of documents.
# In a real system this would be backed by persistent storage
DOCUMENTS_DB: dict[str, dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "alice", "content": "Initial content of doc1."},
    "doc2": {"document_id": "doc2", "owner_id": "bob",   "content": "Initial content of doc2."},
}

def update_document(
    user_id: str,
    user_role: str,
    document_id: str,
    owner_id: str,
    new_content: str,
) -> str:
    """
    Update the content of a document if the user is authorised.

    Parameters
    ----------
    user_id : str
        The ID of the user attempting to update the document.
    user_role : str
        Role of the user (`'viewer'`, `'editor'`, etc.).
    document_id : str
        Identifier of the target document.
    owner_id : str
        The user ID that owns the document.  This is passed for extra
        safety – it must match the owner stored in the database.
    new_content : str
        The content to replace the existing document with.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    ValueError
        If the document does not exist in ``DOCUMENTS_DB``.
    PermissionError
        If the user is not authorised to update the document.
    """
    # 1. Ensure the document exists
    doc = DOCUMENTS_DB.get(document_id)
    if doc is None:
        raise ValueError(f"Document with ID '{document_id}' does not exist.")

    # 2. Verify that the provided owner_id matches the stored one
    if doc["owner_id"] != owner_id:
        raise PermissionError("Provided owner ID does not match the document's actual owner.")

    # 3. Authorisation check
    #   - The user must be the owner or have an 'editor' role.
    is_owner = (user_id == doc["owner_id"])
    has_editor_privileges = (user_role.lower() == "editor")
    if not (is_owner or has_editor_privileges):
        raise PermissionError("User is not authorised to update this document.")

    # 4. Perform the update
    doc["content"] = new_content

    # 5. Return the updated content (for confirmation)
    return doc["content"]


# Example usage
if __name__ == "__main__":
    try:
        updated = update_document(
            user_id="alice",
            user_role="editor",
            document_id="doc1",
            owner_id="alice",
            new_content="Updated content for doc1.",
        )
        print(f"Document updated successfully: {updated}")
    except Exception as e:
        print(f"Error: {e}")