# -*- coding: utf-8 -*-
"""
Document Management System – File Modification

This module provides a single function, `modify_file`, that allows
authenticated users to update the content of an existing document.
The function enforces proper authorization checks and raises
exceptions for invalid input or unauthorized access.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# Example in‑memory database of documents.
# In a real system this would be replaced by persistent storage.
DOCUMENTS_DB: dict[str, dict] = {
    "doc-001": {"document_id": "doc-001", "owner_id": "user-123", "content": "Hello, world!"},
    # Add more documents as needed.
}


def modify_file(
    account_id: str,
    account_role: str,
    file_id: str,
    owner_id: str,
    updated_content: str,
) -> str:
    """
    Update the content of a document if the caller is authorized.

    Parameters
    ----------
    account_id : str
        ID of the user attempting to modify the document.
    account_role : str
        Role of the user (e.g., 'viewer', 'editor').
    file_id : str
        Identifier of the document to modify.
    owner_id : str
        ID of the original creator/owner of the document.
    updated_content : str
        New content to store in the document.

    Returns
    -------
    str
        The updated content if modification succeeded.

    Raises
    ------
    ValueError
        If the document does not exist in ``DOCUMENTS_DB``.
    PermissionError
        If the caller is not authorized to modify the document.
    """
    # 1. Ensure the document exists
    if file_id not in DOCUMENTS_DB:
        raise ValueError(f"Document with ID '{file_id}' does not exist.")

    # 2. Verify ownership (owner can modify regardless of role)
    if account_id == owner_id:
        authorized = True
    # 3. Verify role-based permissions (only 'editor' may modify)
    elif account_role.lower() == "editor":
        authorized = True
    else:
        authorized = False

    if not authorized:
        raise PermissionError(
            f"User '{account_id}' with role '{account_role}' is not authorized "
            f"to modify document '{file_id}'."
        )

    # 4. Perform the update
    DOCUMENTS_DB[file_id]["content"] = updated_content

    # 5. Return the new content for confirmation
    return DOCUMENTS_DB[file_id]["content"]


# ------------------------------------------------------------------
# Example usage (for demonstration only; remove or guard with __main__ in production)
# ------------------------------------------------------------------
if __name__ == "__main__":
    try:
        new_text = modify_file(
            account_id="user-123",
            account_role="viewer",  # owner, so allowed
            file_id="doc-001",
            owner_id="user-123",
            updated_content="Updated content goes here.",
        )
        print("Modification succeeded. New content:")
        print(new_text)
    except Exception as exc:
        print(f"Error: {exc}")