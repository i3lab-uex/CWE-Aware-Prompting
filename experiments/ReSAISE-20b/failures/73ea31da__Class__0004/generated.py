# -*- coding: utf-8 -*-
"""
A minimal document management helper that safely edits documents.
The function performs strict authorization checks to avoid CWE‑863
(Incorrect Authorization) vulnerabilities.
"""

from typing import Dict

# Example in-memory document store. In a real system this would be a DB.
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "userA", "content": "Original content of doc1."},
    "doc2": {"document_id": "doc2", "owner_id": "userB", "content": "Original content of doc2."},
}

def edit_document(
    member_id: str,
    member_role: str,
    doc_id: str,
    replacement_content: str
) -> str:
    """
    Update the content of an existing document if the caller is authorized.

    Parameters
    ----------
    member_id : str
        ID of the user attempting the edit.
    member_role : str
        Role of the user; must be 'editor' or 'viewer'.
    doc_id : str
        Unique ID of the target document.
    replacement_content : str
        New content to replace the current document.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the user is not authorized to edit the document.
    KeyError
        If the document does not exist in ``DOCUMENTS_DB``.
    """
    # 1. Validate that the document exists
    try:
        doc = DOCUMENTS_DB[doc_id]
    except KeyError as exc:
        raise KeyError(f"Document with ID '{doc_id}' not found.") from exc

    # 2. Authorization logic
    is_owner = member_id == doc["owner_id"]
    has_edit_privileges = member_role.lower() == "editor"

    # The user must be an editor and either the owner or have explicit edit rights.
    if not (has_edit_privileges and is_owner):
        raise PermissionError(
            f"User '{member_id}' does not have permission to edit document '{doc_id}'."
        )

    # 3. Perform the update
    doc["content"] = replacement_content

    return doc["content"]

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         new_content = edit_document("userA", "editor", "doc1", "Updated content.")
#         print(f"Document updated successfully: {new_content}")
#     except Exception as e:
#         print(e)