# -*- coding: utf-8 -*-
"""
Document management helper functions.
"""

from typing import Dict

# Example in‑memory database of documents
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Initial content"},
    # Add more documents as needed
}


def modify_file(
    account_id: str,
    account_role: str,
    file_id: str,
    owner_id: str,
    updated_content: str
) -> str:
    """
    Modify the content of a document if the caller is authorized.

    Parameters
    ----------
    account_id : str
        The ID of the user attempting to modify the document.
    account_role : str
        Role of the caller (e.g., 'viewer', 'editor').
    file_id : str
        The ID of the document to modify.
    owner_id : str
        The creator's user ID for the target document.
    updated_content : str
        New content to store.

    Returns
    -------
    str
        The updated document content if the operation succeeds.

    Raises
    ------
    ValueError
        If the specified document does not exist.
    PermissionError
        If the caller is not authorized to modify the document.
    """

    # 1. Verify that the document exists
    doc = DOCUMENTS_DB.get(file_id)
    if doc is None:
        raise ValueError(f"Document with ID '{file_id}' does not exist.")

    # 2. Authorization check
    #   - Editors may modify any document.
    #   - Owners may also modify their own documents.
    #   - Viewers are not allowed to modify.
    role = account_role.strip().lower()
    if role == "editor" or (role == "owner" and account_id == owner_id):
        # 3. Perform the update
        doc["content"] = updated_content
        return doc["content"]

    # 4. If we reach here, the user is not authorized
    raise PermissionError(
        f"User '{account_id}' with role '{account_role}' is not authorized "
        f"to modify document '{file_id}'."
    )