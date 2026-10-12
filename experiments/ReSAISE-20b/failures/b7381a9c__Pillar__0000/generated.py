# -*- coding: utf-8 -*-
"""
Document update module.

This module defines the `update_document` function that performs
authorization checks before allowing a user to modify a document.
The implementation protects against CWE-284 (Improper Access Control)
by ensuring that only the owner or a user with an editor role can
update a document. It also validates that the target document exists.
"""

from __future__ import annotations

# Example in‑memory document database
DOCUMENTS_DB: dict[str, dict] = {
    "doc-001": {"document_id": "doc-001", "owner_id": "user123", "content": "Initial content"},
    "doc-002": {"document_id": "doc-002", "owner_id": "user456", "content": "Another document"},
}

def update_document(
    user_id: str,
    user_role: str,
    document_id: str,
    owner_id: str,
    new_content: str
) -> str:
    """
    Update the content of a document if the user is authorized.

    Parameters
    ----------
    user_id : str
        The ID of the user attempting to update the document.
    user_role : str
        Role of the user (e.g., 'viewer', 'editor').
    document_id : str
        Identifier of the document to update.
    owner_id : str
        Owner ID provided by the caller (used for extra safety checks).
    new_content : str
        New content to replace the existing document content.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    ValueError
        If the specified `document_id` does not exist in `DOCUMENTS_DB`.
    PermissionError
        If the user is not authorized to update the document.
    """
    # 1. Ensure the document exists
    doc = DOCUMENTS_DB.get(document_id)
    if doc is None:
        raise ValueError(f"Document with ID '{document_id}' does not exist.")

    # 2. Verify ownership consistency
    if doc["owner_id"] != owner_id:
        raise ValueError("Owner ID mismatch for the requested document.")

    # 3. Authorization check
    if user_id != doc["owner_id"] and user_role.lower() != "editor":
        raise PermissionError("User is not authorized to update this document.")

    # 4. Perform the update
    doc["content"] = new_content

    return doc["content"]

# Example usage (commented out for safety)
# try:
#     updated = update_document(
#         user_id="user123",
#         user_role="viewer",
#         document_id="doc-001",
#         owner_id="user123",
#         new_content="Updated content"
#     )
#     print("Update successful:", updated)
# except Exception as e:
#     print("Error:", e)