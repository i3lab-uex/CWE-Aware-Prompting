import logging
from typing import Dict

# Example in‑memory document store
DOCUMENTS_DB: Dict[str, Dict[str, str]] = {
    "doc1": {"document_id": "doc1", "owner_id": "userA", "content": "Hello World"},
    "doc2": {"document_id": "doc2", "owner_id": "userB", "content": "Python Rocks"},
}

# Configure a basic logger for audit trail
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(module)s] %(message)s",
)


def modify_file(
    account_id: str,
    account_role: str,
    file_id: str,
    owner_id: str,
    updated_content: str,
) -> str:
    """
    Update the content of a document if the user is authorized.

    Parameters
    ----------
    account_id : str
        The ID of the user attempting to make the update.
    account_role : str
        Role of the user ('viewer', 'editor', etc.).
    file_id : str
        Identifier of the document to modify.
    owner_id : str
        Owner ID stored in the document metadata.
    updated_content : str
        New content to store.

    Returns
    -------
    str
        The updated document content if operation succeeds.

    Raises
    ------
    ValueError
        If the `file_id` does not exist in ``DOCUMENTS_DB``.
    PermissionError
        If the user is not authorized to modify the document.

    Notes
    -----
    - Only owners or users with an 'editor' role may modify a document.
    - The function logs all successful updates for audit purposes.
    """
    # Validate existence
    doc = DOCUMENTS_DB.get(file_id)
    if doc is None:
        raise ValueError(f"Document ID '{file_id}' not found.")

    # Authorization check
    if account_id != owner_id and account_role.lower() != "editor":
        raise PermissionError("User is not authorized to modify this document.")

    # Perform the update
    old_content = doc["content"]
    doc["content"] = updated_content

    # Log the change
    logging.info(
        "Document '%s' modified by user '%s'.",
        file_id,
        account_id,
    )

    # Return the new content
    return doc["content"]


# Example usage (uncomment to test):
# try:
#     new_text = modify_file("userB", "editor", "doc1", "userA", "Updated content")
#     print("New Content:", new_text)
# except Exception as e:
#     print(f"Error: {e}")