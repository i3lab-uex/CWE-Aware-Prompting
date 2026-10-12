import xml.sax.saxutils as saxutils

# Example XML template with a placeholder for user text.
xml_pattern = (
    "<response>\n"
    "  <message>{user_text}</message>\n"
    "</response>"
)

def create_xml_reply(user_text: str) -> str:
    """
    Construct an XML reply by inserting user-supplied text into a predefined
    template. The function escapes special XML characters in the user text to
    mitigate injection risks (CWE‑74).

    Parameters:
        user_text: str
            The content supplied by the user that will be inserted into the XML.

    Returns:
        str: A well‑formed XML string with the escaped user content.
    """
    # Escape special XML characters to prevent injection or malformed XML.
    safe_text = saxutils.escape(user_text, entities={"'": "&apos;", "\"": "&quot;"})
    # Format the template with the escaped content.
    return xml_pattern.format(user_text=safe_text)