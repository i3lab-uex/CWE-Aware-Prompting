import json
from typing import Dict

# Sample in‑memory document database. In a real system this would be a
# persistent store such as a relational or NoSQL database.
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Initial content of doc1."},
    "doc2": {"document_id": "doc2", "owner_id": "user456", "content": "Initial content of doc2."},
    # Add more documents as needed
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
        The role of the user ('viewer', 'editor', etc.).
    document_id : str
        The ID of the document to update.
    owner_id : str
        The expected owner of the document. This is checked against the
        stored document's owner to prevent tampering.
    new_content : str
        The new content for the document.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    ValueError
        If the document does not exist.
    PermissionError
        If the user is not authorized to update the document.
    """
    # 1. Verify that the document exists
    if document_id not in DOCUMENTS_DB:
        raise ValueError(f"Document '{document_id}' does not exist.")

    document = DOCUMENTS_DB[document_id]

    # 2. Verify that the provided owner_id matches the stored one
    if document["owner_id"] != owner_id:
        raise PermissionError("Owner ID mismatch. Authorization denied.")

    # 3. Perform role‑based authorization
    # Only editors or the owner themselves can update the document.
    if user_role != "editor" and user_id != document["owner_id"]:
        raise PermissionError("User is not authorized to update this document.")

    # 4. Update the content
    document["content"] = new_content

    # 5. Return the updated content (or you could return the whole document)
    return document["content"]


# Example usage
if __name__ == "__main__":
    try:
        updated = update_document(
            user_id="user123",
            user_role="viewer",  # viewer cannot edit
            document_id="doc1",
            owner_id="user123",
            new_content="Updated content by the owner."
        )
        print("Document updated successfully:", updated)
    except Exception as e:
        print(f"Error: {e}")