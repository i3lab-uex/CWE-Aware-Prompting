# -*- coding: utf-8 -*-

"""
Document management system – file modification logic.
"""

from typing import Dict

# Example in‑memory database of documents.
# In a real system this would be replaced by persistent storage or an ORM.
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Original content of doc1."},
    "doc2": {"document_id": "doc2", "owner_id": "user456", "content": "Original content of doc2."},
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
    Modify the content of a document if the caller is authorized.

    Parameters
    ----------
    account_id : str
        The ID of the user attempting to modify the document.
    account_role : str
        Role of the caller (e.g., 'viewer', 'editor').
    file_id : str
        Identifier of the document to modify.
    owner_id : str
        The creator/owner ID stored in the document metadata.
    updated_content : str
        New content to replace the existing one.

    Returns
    -------
    str
        The updated document content if modification succeeded,
        otherwise an error message.

    Raises
    ------
    ValueError
        If `file_id` does not exist in the database.
    """

    # 1. Verify that the document exists
    if file_id not in DOCUMENTS_DB:
        raise ValueError(f"Document with ID '{file_id}' does not exist.")

    doc = DOCUMENTS_DB[file_id]

    # 2. Validate that the supplied owner_id matches the document's actual owner.
    # This double‑check guards against tampering with the function arguments.
    if doc["owner_id"] != owner_id:
        return "Error: Owner ID mismatch. Unauthorized operation."

    # 3. Enforce access control.
    # Only editors or the document owner can modify content.
    if account_role.lower() != "editor" and account_id != doc["owner_id"]:
        return (
            f"Error: User '{account_id}' does not have permission "
            "to modify this document."
        )

    # 4. Apply the update
    doc["content"] = updated_content

    # 5. Return the new content as confirmation
    return doc["content"]


# Example usage (for testing purposes only)
if __name__ == "__main__":
    try:
        result = modify_file(
            account_id="user123",
            account_role="editor",
            file_id="doc1",
            owner_id="user123",
            updated_content="Updated content for doc1.",
        )
        print("Modification succeeded. New content:")
        print(result)
    except ValueError as e:
        print(f"Failed: {e}")