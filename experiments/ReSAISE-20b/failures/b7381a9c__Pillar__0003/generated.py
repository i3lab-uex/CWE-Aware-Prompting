# -*- coding: utf-8 -*-
"""
Document management module with secure update functionality.
"""

from typing import Dict

# Example in-memory database of documents
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "alice", "content": "Initial content."},
    "doc2": {"document_id": "doc2", "owner_id": "bob",   "content": "Another document."},
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
        The ID of the user attempting the update.
    user_role : str
        Role of the user (e.g., 'viewer', 'editor').
    document_id : str
        Identifier of the target document.
    owner_id : str
        Owner ID declared in the request (must match DB).
    new_content : str
        New content to write into the document.

    Returns
    -------
    str
        The updated document content if authorized; otherwise, an authorization error message.

    Raises
    ------
    ValueError
        If the document does not exist in DOCUMENTS_DB.
    """
    # 1. Ensure the document exists
    if document_id not in DOCUMENTS_DB:
        raise ValueError(f"Document '{document_id}' does not exist.")

    doc = DOCUMENTS_DB[document_id]

    # 2. Verify that the provided owner_id matches the stored one
    if doc["owner_id"] != owner_id:
        # Potential tampering or mistake – treat as unauthorized
        return "Authorization Error: Owner mismatch."

    # 3. Authorization logic:
    #    - The owner can always edit.
    #    - Users with role 'editor' can edit any document (or you could limit to own docs).
    #    - All others are denied.
    if user_id == owner_id or user_role.lower() == "editor":
        # 4. Perform the update
        doc["content"] = new_content
        return doc["content"]
    else:
        # 5. Unauthorized attempt
        return "Authorization Error: Insufficient permissions."

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(update_document("alice", "editor", "doc1", "alice", "Updated by Alice"))
#     print(update_document("eve", "viewer", "doc1", "alice", "Malicious edit"))