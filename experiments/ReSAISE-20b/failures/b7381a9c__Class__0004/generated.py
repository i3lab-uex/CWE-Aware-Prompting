# -*- coding: utf-8 -*-
"""
A simple in‑memory document management system with secure update logic.
"""

from typing import Dict

# In‑memory database of documents
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "alice", "content": "Initial content of doc1."},
    "doc2": {"document_id": "doc2", "owner_id": "bob",   "content": "Initial content of doc2."},
}

def update_document(
    user_id: str,
    user_role: str,
    document_id: str,
    owner_id: str,
    new_content: str
) -> str:
    """
    Update the content of a document after performing proper authorization checks.

    Args:
        user_id (str): The ID of the user attempting to update the document.
        user_role (str): Role of the user ('viewer', 'editor', etc.).
        document_id (str): ID of the target document.
        owner_id (str): Owner of the document. This should match the stored owner for consistency checks.
        new_content (str): New content to write into the document.

    Returns:
        str: The updated document content.

    Raises:
        ValueError: If the document does not exist in DOCUMENTS_DB.
        PermissionError: If the user is not authorized to perform the update.
    """
    # Verify document existence
    doc = DOCUMENTS_DB.get(document_id)
    if not doc:
        raise ValueError(f"Document '{document_id}' does not exist.")

    # Consistency check: ensure provided owner_id matches stored one
    if doc["owner_id"] != owner_id:
        raise ValueError("Owner ID mismatch for the specified document.")

    # Authorization logic (CWE‑863 protection)
    # Allow update if user is the owner or has an editor role
    if not (user_id == doc["owner_id"] or user_role.lower() == "editor"):
        raise PermissionError("User is not authorized to update this document.")

    # Perform the update
    doc["content"] = new_content

    return doc["content"]

# Example usage (uncomment to test)
# try:
#     updated = update_document("alice", "viewer", "doc1", "alice", "New content.")
#     print(updated)
# except Exception as e:
#     print(f"Error: {e}")