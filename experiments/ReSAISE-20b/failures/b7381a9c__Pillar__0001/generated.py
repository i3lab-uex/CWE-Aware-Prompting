# -*- coding: utf-8 -*-
"""
Document management utilities.
"""

from typing import Dict

# Example in‑memory database; in a real system this would be replaced
# by persistent storage (e.g., a database or external service).
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc-001": {"document_id": "doc-001", "owner_id": "user-a", "content": "Initial content of doc 1."},
    "doc-002": {"document_id": "doc-002", "owner_id": "user-b", "content": "Initial content of doc 2."},
}


def update_document(
    user_id: str,
    user_role: str,
    document_id: str,
    owner_id: str,
    new_content: str
) -> str:
    """
    Update the content of a document after performing authorization checks.

    Parameters
    ----------
    user_id : str
        The ID of the user attempting to update the document.
    user_role : str
        The role of the user (e.g., 'viewer', 'editor').
    document_id : str
        The ID of the target document.
    owner_id : str
        The owner of the document (redundant check; can be derived from the DB).
    new_content : str
        The new content to write into the document.

    Returns
    -------
    str
        The updated content of the document if the operation succeeds.

    Raises
    ------
    ValueError
        If the specified document does not exist in ``DOCUMENTS_DB``.
    PermissionError
        If the user is not authorized to update the document.
    """
    # 1. Ensure the document exists
    doc = DOCUMENTS_DB.get(document_id)
    if not doc:
        raise ValueError(f"Document with ID '{document_id}' does not exist.")

    # 2. Verify that the owner_id matches the stored owner
    if doc["owner_id"] != owner_id:
        raise ValueError("Provided owner_id does not match the document's actual owner.")

    # 3. Authorization logic
    #   - An 'editor' role can update any document.
    #   - The owner (regardless of role) is allowed to edit their own documents.
    if user_role.lower() != "editor" and user_id != owner_id:
        raise PermissionError("User is not authorized to update this document.")

    # 4. Perform the update
    doc["content"] = new_content

    # 5. Return the updated content for confirmation
    return doc["content"]


# Example usage (would normally be in a separate test module or main guard)
if __name__ == "__main__":
    try:
        updated = update_document(
            user_id="user-a",
            user_role="editor",
            document_id="doc-001",
            owner_id="user-a",
            new_content="Updated content for doc 1."
        )
        print(f"Update successful: {updated}")
    except Exception as exc:
        print(f"Error: {exc}")