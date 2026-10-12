# Document management system – edit functionality

DOCUMENTS_DB = {
    # Example structure; in a real system this would be populated elsewhere
    "doc123": {"document_id": "doc123", "owner_id": "user1", "content": "Original text."},
    # Add more documents as needed
}


def edit_doc(u_id: str, u_role: str, doc_id: str, doc_owner: str, new_body: str) -> str:
    """
    Modify the content of a document if the user is authorized.

    Parameters
    ----------
    u_id : str
        ID of the user attempting to edit.
    u_role : str
        Role of the user ('viewer', 'editor', etc.).
    doc_id : str
        ID of the document to edit.
    doc_owner : str
        Owner ID of the document (redundant with DOCUMENTS_DB entry but passed for convenience).
    new_body : str
        New content to replace the existing document body.

    Returns
    -------
    str
        The updated content if the edit was successful, or an error message if unauthorized.

    Raises
    ------
    ValueError
        If the document ID does not exist in DOCUMENTS_DB.
    """
    # 1. Validate that the document exists
    if doc_id not in DOCUMENTS_DB:
        raise ValueError(f"Document ID '{doc_id}' does not exist.")

    doc = DOCUMENTS_DB[doc_id]

    # 2. Ensure the passed owner matches the stored owner (consistency check)
    if doc_owner != doc["owner_id"]:
        raise ValueError("Provided document owner does not match the stored owner.")

    # 3. Authorization check
    is_owner = (u_id == doc["owner_id"])
    has_editor_privilege = (u_role.lower() == "editor")

    if not (is_owner or has_editor_privilege):
        return "Error: Unauthorized user."

    # 4. Perform the update
    doc["content"] = new_body

    return new_body


# Example usage (for testing purposes; remove or comment out in production)
if __name__ == "__main__":
    try:
        updated = edit_doc(
            u_id="user1",
            u_role="viewer",
            doc_id="doc123",
            doc_owner="user1",
            new_body="Updated text."
        )
        print(f"Update result: {updated}")
    except ValueError as e:
        print(e)