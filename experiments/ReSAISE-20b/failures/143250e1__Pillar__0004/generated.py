#!/usr/bin/env python3
"""
Corporate document modification utility.

This module implements a single function `alter_document` that updates the content
of a document in an in‑memory database while enforcing strict access control.
The function raises `PermissionError` if the caller is not allowed to modify
the document.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# In‑memory mock database – in a real system this would be backed by
# persistent storage (e.g., SQL, NoSQL, or a file system).
DOCUMENTS_DB = {
    "doc1": {"document_id": "doc1", "owner_id": "alice", "content": "Initial content"},
    "doc2": {"document_id": "doc2", "owner_id": "bob",   "content": "Another file"},
    # Add more documents as needed
}

# --------------------------------------------------------------------------- #
def alter_document(
    modifier_id: str,
    user_role: str,
    doc_identifier: str,
    creator_id: str,
    updated_content: str,
) -> str:
    """
    Update the content of a document if the caller is authorized.

    Parameters
    ----------
    modifier_id : str
        The ID of the user attempting to modify the document.
    user_role : str
        The role of the user. Must be either 'viewer' or 'editor'.
    doc_identifier : str
        The unique identifier of the document to modify.
    creator_id : str
        The ID of the original owner/creator of the document.
    updated_content : str
        New content that will replace the existing document content.

    Returns
    -------
    str
        The updated content of the document after a successful modification.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the document.
    KeyError
        If the specified document does not exist in `DOCUMENTS_DB`.
    ValueError
        If `user_role` is not one of the expected values.
    """

    # Validate role
    if user_role not in {"viewer", "editor"}:
        raise ValueError(f"Invalid role '{user_role}'. Expected 'viewer' or 'editor'.")

    # Ensure the document exists
    if doc_identifier not in DOCUMENTS_DB:
        raise KeyError(f"Document '{doc_identifier}' not found.")

    doc = DOCUMENTS_DB[doc_identifier]

    # Check that the creator_id matches the stored owner
    if doc["owner_id"] != creator_id:
        raise PermissionError("Provided creator ID does not match the document owner.")

    # Enforce access control: only editors may modify
    if user_role != "editor":
        raise PermissionError("User does not have permission to modify the document.")

    # Enforce that the modifier is either the owner or has an editor role
    if modifier_id != doc["owner_id"]:
        # For added safety, you could also maintain an explicit list of editors.
        raise PermissionError("Only the document owner can modify this document.")

    # All checks passed – perform the update
    doc["content"] = updated_content

    return doc["content"]

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Example usage – this block is for demonstration and testing only.
    try:
        new_text = alter_document(
            modifier_id="alice",
            user_role="editor",
            doc_identifier="doc1",
            creator_id="alice",
            updated_content="Updated content from Alice."
        )
        print(f"Document updated successfully: {new_text}")
    except Exception as exc:
        print(f"Error: {exc}")