# -*- coding: utf-8 -*-

"""
A minimal document modification module for a company DMS.
"""

from __future__ import annotations

import threading
from typing import Dict, Any

# Example in‑memory database. In a real system this would be replaced by
# a persistent storage layer (e.g., SQL, NoSQL).
DOCUMENTS_DB: Dict[str, Dict[str, Any]] = {
    # Example document
    "doc_001": {"document_id": "doc_001", "owner_id": "user123", "content": "Initial content."},
    # Add more documents as needed
}

# Global lock to protect concurrent access to DOCUMENTS_DB.
_db_lock = threading.RLock()


def modify_document(
    requester_id: str,
    requester_role: str,
    document_identifier: str,
    document_owner_id: str,
    modified_content: str,
) -> str:
    """
    Update the content of an existing document if the requester has proper
    authorization.

    Parameters
    ----------
    requester_id : str
        ID of the user attempting to modify the document.
    requester_role : str
        Role of the requester. Allowed values are 'viewer' and 'editor'.
    document_identifier : str
        Unique identifier of the target document.
    document_owner_id : str
        The owner ID stored in the database for comparison.
    modified_content : str
        New content that will replace the current version.

    Returns
    -------
    str
        The updated document content.

    Raises
    ------
    PermissionError
        If the requester is not authorized to modify the document.
    KeyError
        If the specified document does not exist in the database.
    ValueError
        If an invalid role is provided.

    Notes
    -----
    * Only users with the 'editor' role or the document owner can modify.
    * The function uses a re‑entrant lock to ensure thread safety.
    """
    # Validate role
    if requester_role not in {"viewer", "editor"}:
        raise ValueError(f"Invalid role '{requester_role}'. Expected 'viewer' or 'editor'.")

    with _db_lock:
        # Check that the document exists
        if document_identifier not in DOCUMENTS_DB:
            raise KeyError(f"Document '{document_identifier}' does not exist.")

        doc_record = DOCUMENTS_DB[document_identifier]

        # Enforce access control: editor role or owner
        if requester_role != "editor" and requester_id != doc_record["owner_id"]:
            raise PermissionError(
                f"User '{requester_id}' does not have permission to modify document "
                f"'{document_identifier}'."
            )

        # Optional: double‑check owner ID matches database (prevents spoofing)
        if document_owner_id != doc_record["owner_id"]:
            raise PermissionError(
                f"Provided owner ID '{document_owner_id}' does not match the record."
            )

        # Perform the update
        doc_record["content"] = modified_content

        return doc_record["content"]


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         updated = modify_document(
#             requester_id="user123",
#             requester_role="editor",
#             document_identifier="doc_001",
#             document_owner_id="user123",
#             modified_content="Updated content.",
#         )
#         print("Document updated:", updated)
#     except Exception as e:
#         print(e)