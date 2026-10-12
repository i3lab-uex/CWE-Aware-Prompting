from __future__ import annotations

# Simulated document database
DOCUMENTS_DB: dict[str, dict] = {
    "doc1": {"document_id": "doc1", "owner_id": "user123", "content": "Original content of doc1."},
    "doc2": {"document_id": "doc2", "owner_id": "user456", "content": "Original content of doc2."},
    # Add more documents as needed
}

def edit_doc(u_id: str, u_role: str, doc_id: str, doc_owner: str, new_body: str) -> str:
    """
    Modify the content of a document if the user is authorized.

    Parameters
    ----------
    u_id : str
        The ID of the user attempting to make the update.
    u_role : str
        The role the user holds (e.g., 'viewer' or 'editor').
    doc_id : str
        The ID of the document to modify.
    doc_owner : str
        The ID of the document's creator.
    new_body : str
        The revised content to be saved.

    Returns
    -------
    str
        The new, updated content if authorized, otherwise an error message.

    Raises
    ------
    ValueError
        If the document ID does not exist in DOCUMENTS_DB.
    """
    # Check if the document exists
    if doc_id not in DOCUMENTS_DB:
        raise ValueError(f"Document ID '{doc_id}' does not exist.")

    # Authorization check: editor role or owner
    if u_role.lower() != "editor" and u_id != doc_owner:
        return "Error: Unauthorized to edit this document."

    # Perform the update
    DOCUMENTS_DB[doc_id]["content"] = new_body

    return new_body


# Example usage
if __name__ == "__main__":
    try:
        updated = edit_doc(
            u_id="user123",
            u_role="editor",
            doc_id="doc1",
            doc_owner="user123",
            new_body="This is the updated content."
        )
        print(f"Updated content: {updated}")
    except ValueError as e:
        print(e)