# Document management system – modification logic

DOCUMENTS_DB = {
    # Example entries (these would normally be loaded from a persistent store)
    "doc1": {"document_id": "doc1", "owner_id": "userA", "content": "Original content of doc1."},
    "doc2": {"document_id": "doc2", "owner_id": "userB", "content": "Original content of doc2."},
}

def modify_file(account_id: str,
                account_role: str,
                file_id: str,
                owner_id: str,
                updated_content: str) -> str:
    """
    Modify the content of a document if the user is authorized.

    Parameters
    ----------
    account_id : str
        The ID of the user attempting to make the update.
    account_role : str
        The role the user holds (e.g., 'viewer' or 'editor').
    file_id : str
        The ID of the document to modify.
    owner_id : str
        The ID of the document's creator.  This is included for
        additional validation but must match the stored owner_id.
    updated_content : str
        The revised content to be saved.

    Returns
    -------
    str
        The new, updated content if the user is authorized.

    Raises
    ------
    ValueError
        If `file_id` does not exist in the system.
    PermissionError
        If the user is not authorized to modify the document.
    """
    # 1. Verify that the document exists
    doc = DOCUMENTS_DB.get(file_id)
    if doc is None:
        raise ValueError(f"Document with ID '{file_id}' does not exist.")

    # 2. Ensure the provided owner_id matches the stored one
    if doc["owner_id"] != owner_id:
        raise PermissionError("Provided owner ID does not match the document's owner.")

    # 3. Authorisation check
    is_owner = account_id == doc["owner_id"]
    is_editor = account_role.lower() == "editor"

    if not (is_owner or is_editor):
        raise PermissionError("User does not have permission to modify this document.")

    # 4. Perform the update
    doc["content"] = updated_content

    # 5. Return the new content
    return doc["content"]