# -*- coding: utf-8 -*-
"""
Document Management System – Update Document

This module provides a single function `update_document` that safely updates
the contents of a document while enforcing role‑based access control.

Author: OpenAI ChatGPT
"""

from typing import Dict

# Example in‑memory database of documents.
# Each document is a dict with keys: 'document_id', 'owner_id', 'content'.
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Initial content of doc1."},
    "doc2": {"document_id": "doc2", "owner_id": "user456", "content": "Initial content of doc2."},
    # Add more documents as needed.
}


def update_document(
    user_id: str,
    user_role: str,
    document_id: str,
    owner_id: str,
    new_content: str,
) -> str:
    """
    Update the content of a document in the DOCUMENTS_DB.

    Parameters
    ----------
    user_id : str
        The ID of the user attempting to update the document.
    user_role : str
        The role of the user (e.g., 'viewer', 'editor').
    document_id : str
        The ID of the document to be updated.
    owner_id : str
        The expected owner ID of the document.
    new_content : str
        The new content to write into the document.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    ValueError
        If the specified document does not exist in DOCUMENTS_DB.
    PermissionError
        If the user is not authorized to modify the document.
    """
    # 1. Check that the document exists
    doc = DOCUMENTS_DB.get(document_id)
    if not doc:
        raise ValueError(f"Document with ID '{document_id}' does not exist.")

    # 2. Verify that the owner_id matches the stored document's owner
    if doc["owner_id"] != owner_id:
        raise ValueError(
            f"Owner ID mismatch for document '{document_id}'. "
            f"Expected {doc['owner_id']}, got {owner_id}."
        )

    # 3. Authorization logic
    # - Owners can always edit regardless of role.
    # - Users with the 'editor' role can edit any document (optionally enforce owner check).
    # - All other roles are denied.
    if user_id != doc["owner_id"] and user_role.lower() != "editor":
        raise PermissionError(
            f"User '{user_id}' with role '{user_role}' is not authorized to update "
            f"document '{document_id}'."
        )

    # 4. Perform the update
    doc["content"] = new_content

    # 5. Return the updated content for confirmation
    return doc["content"]


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        updated = update_document(
            user_id="user123",
            user_role="viewer",
            document_id="doc1",
            owner_id="user123",
            new_content="Updated content for doc1."
        )
        print("Document updated successfully:", updated)
    except Exception as e:
        print(f"Error: {e}")