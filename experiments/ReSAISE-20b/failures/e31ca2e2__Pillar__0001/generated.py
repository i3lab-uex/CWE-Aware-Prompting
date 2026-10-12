# -*- coding: utf-8 -*-
"""
Document Management System – Edit Document Module

This module provides the `edit_doc` function which allows authorized users
to modify a document's content. The implementation follows best practices
for access control (CWE‑284) and raises clear exceptions for error conditions.
"""

from __future__ import annotations

# Global in‑memory document store. In a real application this would be replaced
# with persistent storage (e.g., a database or file system).
DOCUMENTS_DB: dict[str, dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "userA", "content": "Original content A"},
    "doc2": {"document_id": "doc2", "owner_id": "userB", "content": "Original content B"},
    # ... additional documents
}


def edit_doc(
    u_id: str,
    u_role: str,
    doc_id: str,
    doc_owner: str,
    new_body: str,
) -> str:
    """
    Edit the content of a document if the caller is authorized.

    Parameters
    ----------
    u_id : str
        ID of the user attempting to make the update.
    u_role : str
        Role of the user (e.g., 'viewer', 'editor').
    doc_id : str
        Identifier of the document to modify.
    doc_owner : str
        Owner ID of the document. Must match the owner in DOCUMENTS_DB.
    new_body : str
        The new content to store.

    Returns
    -------
    str
        The updated document content if the operation succeeds.

    Raises
    ------
    ValueError
        If `doc_id` does not exist in the system.
    PermissionError
        If the user is not authorized to edit the document.

    Notes
    -----
    - Only users with role 'editor' or the owner of the document can modify it.
    - The function updates the global `DOCUMENTS_DB` in place.
    """
    # 1. Validate that the document exists
    if doc_id not in DOCUMENTS_DB:
        raise ValueError(f"Document ID '{doc_id}' does not exist.")

    # 2. Verify that the provided doc_owner matches the stored owner
    stored_doc = DOCUMENTS_DB[doc_id]
    if stored_doc["owner_id"] != doc_owner:
        raise PermissionError("Provided document owner does not match the stored owner.")

    # 3. Access control: allow if user is the owner or has editor role
    is_owner = u_id == doc_owner
    is_editor_role = u_role.lower() == "editor"

    if not (is_owner or is_editor_role):
        raise PermissionError("User is not authorized to edit this document.")

    # 4. Perform the update
    stored_doc["content"] = new_body

    # 5. Return the updated content for confirmation
    return stored_doc["content"]


# Example usage (for demonstration only; remove or guard with `if __name__ == "__main__":` in production)
if __name__ == "__main__":
    try:
        updated = edit_doc(
            u_id="userA",
            u_role="editor",
            doc_id="doc1",
            doc_owner="userA",
            new_body="Updated content for document 1.",
        )
        print(f"Document updated successfully: {updated}")
    except Exception as e:
        print(f"Error: {e}")