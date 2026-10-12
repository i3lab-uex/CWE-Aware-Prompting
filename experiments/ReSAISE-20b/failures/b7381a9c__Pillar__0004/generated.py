# -*- coding: utf-8 -*-
"""
Document management system – update functionality.

The module defines a simple in‑memory document store (`DOCUMENTS_DB`) and
provides an `update_document` function that enforces proper access control.
"""

from typing import Dict

# In‑memory document store
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc-001": {"document_id": "doc-001", "owner_id": "alice", "content": "Initial content."},
    "doc-002": {"document_id": "doc-002", "owner_id": "bob",   "content": "Another document."},
}

# Role hierarchy – lower values mean less privilege
ROLE_HIERARCHY = {
    "viewer": 1,
    "editor": 2,
    # future roles can be added here
}

def _is_authorized(user_id: str, user_role: str, owner_id: str) -> bool:
    """
    Determine whether a user is allowed to modify a document.

    Rules:
        * The owner can always edit.
        * Users with role 'editor' (or higher) may edit any document.
    """
    # Verify that the supplied role is known
    if user_role not in ROLE_HIERARCHY:
        return False

    # Owner check
    if user_id == owner_id:
        return True

    # Role based check – editors are allowed to edit
    if user_role == "editor":
        return True

    # All other cases are forbidden
    return False

def update_document(
    user_id: str,
    user_role: str,
    document_id: str,
    owner_id: str,
    new_content: str
) -> str:
    """
    Update the content of a document if the caller is authorized.

    Parameters
    ----------
    user_id : str
        Identifier of the user attempting the update.
    user_role : str
        Role of the user (e.g., 'viewer', 'editor').
    document_id : str
        Identifier of the target document.
    owner_id : str
        Owner of the document (must match the stored value).
    new_content : str
        New content to replace the existing document body.

    Returns
    -------
    str
        The updated content of the document.

    Raises
    ------
    ValueError
        If the specified `document_id` does not exist in `DOCUMENTS_DB`.
    PermissionError
        If the user is not authorized to perform the update.
    """
    # 1. Validate document existence
    doc = DOCUMENTS_DB.get(document_id)
    if doc is None:
        raise ValueError(f"Document '{document_id}' does not exist.")

    # 2. Validate owner consistency
    if doc["owner_id"] != owner_id:
        raise ValueError("Owner ID does not match the document's recorded owner.")

    # 3. Authorization check
    if not _is_authorized(user_id, user_role, owner_id):
        raise PermissionError("Authorization error: insufficient privileges to update the document.")

    # 4. Perform the update
    doc["content"] = new_content

    # Return the updated content (or the whole document if desired)
    return doc["content"]

# Example usage
if __name__ == "__main__":
    try:
        updated = update_document(
            user_id="bob",
            user_role="editor",
            document_id="doc-001",
            owner_id="alice",
            new_content="Updated content by an editor."
        )
        print(f"Document updated successfully: {updated}")
    except Exception as e:
        print(f"Error: {e}")