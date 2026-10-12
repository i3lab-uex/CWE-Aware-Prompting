# DOCUMENTS_DB simulates a simple in-memory document store.
# Each key is a document_id, and the value is a dict containing
# 'document_id', 'owner_id', and 'content'.
DOCUMENTS_DB = {
    "doc1": {"document_id": "doc1", "owner_id": "userA", "content": "Initial content of doc1."},
    "doc2": {"document_id": "doc2", "owner_id": "userB", "content": "Initial content of doc2."},
    # Add more documents as needed
}


def modify_file(account_id: str, account_role: str,
                file_id: str, owner_id: str,
                updated_content: str) -> str:
    """
    Update the content of a document if the user is authorized.

    Parameters
    ----------
    account_id : str
        The ID of the user attempting to modify the document.
    account_role : str
        The role of the user, e.g. 'viewer' or 'editor'.
    file_id : str
        The ID of the document to modify.
    owner_id : str
        The creator/owner ID of the document (redundant check for safety).
    updated_content : str
        The new content to be stored.

    Returns
    -------
    str
        The updated document content if the operation succeeds,
        or an error message string if authorization fails.

    Raises
    ------
    ValueError
        If the specified `file_id` does not exist in DOCUMENTS_DB.
    """
    # 1. Validate that the document exists
    if file_id not in DOCUMENTS_DB:
        raise ValueError(f"Document with ID '{file_id}' does not exist.")

    # 2. Retrieve the document record
    doc = DOCUMENTS_DB[file_id]

    # 3. Double‑check ownership (in case caller provided a mismatched owner_id)
    if doc["owner_id"] != owner_id:
        return "Error: Provided owner ID does not match document's actual owner."

    # 4. Authorization logic
    # - Owner always has edit rights.
    # - Users with role 'editor' also have edit rights.
    if account_id == owner_id or account_role.lower() == "editor":
        # 5. Perform the update
        doc["content"] = updated_content

        # Optionally, you could log the change or record a timestamp here.

        return doc["content"]
    else:
        # 6. Unauthorized attempt
        return "Error: User lacks permission to modify this document."


# Example usage:
if __name__ == "__main__":
    try:
        new_content = modify_file(
            account_id="userA",
            account_role="viewer",
            file_id="doc1",
            owner_id="userA",
            updated_content="This is the new content for doc1."
        )
        print(new_content)
    except ValueError as e:
        print(e)