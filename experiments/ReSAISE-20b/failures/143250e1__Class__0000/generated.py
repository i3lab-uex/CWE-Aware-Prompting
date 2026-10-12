import copy

# Sample in‑memory database – in a real system this would be replaced by a persistent store.
DOCUMENTS_DB = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Original content."},
    "doc2": {"document_id": "doc2", "owner_id": "user456", "content": "Another document."},
}


def alter_document(
    modifier_id: str,
    user_role: str,
    doc_identifier: str,
    creator_id: str,
    updated_content: str,
) -> str:
    """
    Update the content of a document if the user is authorized.

    Parameters
    ----------
    modifier_id : str
        ID of the user attempting the modification.
    user_role : str
        Role of the user, must be 'editor' to modify documents.
    doc_identifier : str
        The unique identifier of the target document.
    creator_id : str
        The ID of the original owner of the document (for double‑check).
    updated_content : str
        The new content that will replace the existing document text.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the user is not an editor or if ownership does not match.
    KeyError
        If the document identifier does not exist in the database.
    """
    # 1. Verify that the document exists
    if doc_identifier not in DOCUMENTS_DB:
        raise KeyError(f"Document '{doc_identifier}' does not exist.")

    # 2. Retrieve the stored document
    doc = DOCUMENTS_DB[doc_identifier]

    # 3. Perform a robust authorization check
    #   - The user must have the 'editor' role.
    #   - The stored owner_id must match the provided creator_id to guard against tampering.
    if user_role.lower() != "editor":
        raise PermissionError("Only users with the 'editor' role may modify documents.")
    if doc["owner_id"] != creator_id:
        raise PermissionError("Provided creator ID does not match the document owner.")
    if doc["owner_id"] != modifier_id:
        raise PermissionError("Only the document owner may modify this document.")

    # 4. Apply the update safely
    #   We make a shallow copy to avoid accidental mutation of other references.
    updated_doc = copy.deepcopy(doc)
    updated_doc["content"] = updated_content

    # 5. Persist the change back to the database
    DOCUMENTS_DB[doc_identifier] = updated_doc

    # 6. Return the new content
    return updated_doc["content"]


# Example usage (uncomment to test)
# try:
#     new_content = alter_document(
#         modifier_id="user123",
#         user_role="editor",
#         doc_identifier="doc1",
#         creator_id="user123",
#         updated_content="Updated content here."
#     )
#     print("Document updated successfully:", new_content)
# except Exception as e:
#     print(f"Error: {e}")