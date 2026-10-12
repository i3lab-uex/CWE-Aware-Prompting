# -*- coding: utf-8 -*-
"""
Document modification module.

This module contains a single public function `modify_file` which updates
the content of a document in the `DOCUMENTS_DB` dictionary.  The function
ensures that only users with proper authorization (document owner or an
editor) can modify a document.  It raises a `ValueError` if the supplied
document ID does not exist.

The implementation follows the principle of *least privilege* and
explicitly checks the caller's role and ownership before performing any
modification, thereby mitigating CWE‑863 (Incorrect Authorization).
"""

from typing import Dict

# Sample in-memory document database.
# Each entry maps a document_id to a dictionary containing:
#   - 'document_id': str
#   - 'owner_id': str
#   - 'content': str
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Original content of doc1."},
    "doc2": {"document_id": "doc2", "owner_id": "user456", "content": "Original content of doc2."},
    # Additional documents can be added here.
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
        ID of the user attempting to modify the document.
    account_role : str
        Role of the caller (e.g., 'viewer', 'editor').
    file_id : str
        ID of the document to be modified.
    owner_id : str
        Owner ID claimed for the document.  This is used to verify that
        the supplied `file_id` matches its stored owner.
    updated_content : str
        New content to replace the existing document content.

    Returns
    -------
    str
        The updated content if modification succeeds.
        If the caller is not authorized, returns the string
        "Unauthorized access".

    Raises
    ------
    ValueError
        If `file_id` does not exist in the system.
    """

    # 1. Verify that the document exists
    if file_id not in DOCUMENTS_DB:
        raise ValueError(f"Document ID '{file_id}' does not exist.")

    document = DOCUMENTS_DB[file_id]

    # 2. Verify that the supplied owner_id matches the stored one
    if document["owner_id"] != owner_id:
        # The caller supplied a mismatched owner; treat as unauthorized.
        return "Unauthorized access"

    # 3. Authorization check: only editors or the owner can modify
    if account_role == "editor" or account_id == document["owner_id"]:
        # Perform the update
        document["content"] = updated_content
        return document["content"]
    else:
        # Unauthorized: viewer or other roles cannot modify
        return "Unauthorized access"

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         result = modify_file("user123", "viewer", "doc1", "user123", "New content")
#         print(result)  # Should print "Unauthorized access"
#     except ValueError as e:
#         print(e)