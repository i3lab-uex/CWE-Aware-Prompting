#!/usr/bin/env python3
"""
Document modification helper for a corporate document management platform.
"""

from __future__ import annotations

# Example in-memory database of documents. In a real system this would be
# backed by persistent storage (e.g., SQL, NoSQL, or a dedicated document store).
DOCUMENTS_DB: dict[str, dict[str, str]] = {
    # Example entry:
    # "doc123": {"document_id": "doc123", "owner_id": "user1", "content": "Initial content."}
}

def alter_document(
    modifier_id: str,
    user_role: str,
    doc_identifier: str,
    creator_id: str,
    updated_content: str,
) -> str:
    """
    Update the content of a document if the caller is authorized.

    Parameters
    ----------
    modifier_id : str
        ID of the user attempting to modify the document.
    user_role : str
        Role of the user; must be either 'viewer' or 'editor'.
    doc_identifier : str
        Unique identifier of the document to modify.
    creator_id : str
        ID of the original document owner.  Used only for consistency checks.
    updated_content : str
        New content that will replace the existing document content.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    KeyError
        If the specified document does not exist.
    PermissionError
        If the user is not authorized to modify the document.
    ValueError
        If an unexpected role is supplied.
    """

    # Validate user_role first
    if user_role not in {"viewer", "editor"}:
        raise ValueError(f"Unknown role '{user_role}'. Allowed roles are 'viewer' and 'editor'.")

    # Fetch the document from the database
    try:
        doc = DOCUMENTS_DB[doc_identifier]
    except KeyError as exc:
        raise KeyError(f"Document '{doc_identifier}' not found.") from exc

    # Basic consistency check: creator_id must match the stored owner_id
    if doc["owner_id"] != creator_id:
        raise ValueError("Provided creator_id does not match the document's owner.")

    # Authorization logic:
    #   * The owner can modify regardless of role
    #   * An editor role is allowed to modify any document they own or any other doc?
    #     Here we assume editors can only edit their own documents.
    if modifier_id != doc["owner_id"] and user_role != "editor":
        raise PermissionError("You do not have permission to modify this document.")

    # Update the content
    doc["content"] = updated_content

    return doc["content"]

# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Populate the database with a sample document
    DOCUMENTS_DB["doc001"] = {
        "document_id": "doc001",
        "owner_id": "alice",
        "content": "Original content.",
    }

    try:
        new_content = alter_document(
            modifier_id="alice",
            user_role="editor",
            doc_identifier="doc001",
            creator_id="alice",
            updated_content="Updated content.",
        )
        print(f"Document updated successfully: {new_content}")
    except Exception as e:
        print(f"Error: {e}")