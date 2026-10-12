import xml.sax.saxutils as sax

# Predefined XML template containing a {user_text} placeholder.
xml_pattern = (
    "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
    "<response>\n"
    "  <message>{user_text}</message>\n"
    "</response>"
)

def create_xml_reply(user_text: str) -> str:
    """
    Return an XML string with the supplied user_text inserted safely
    into the predefined xml_pattern.

    The function escapes XML special characters to mitigate CWE-707
    (Improper Neutralization of Structured Data) and prevent injection
    or malformed XML.

    Parameters:
        user_text (str): Text supplied by the user to be embedded in
                         the XML response.

    Returns:
        str: The final, well‑formed XML string.
    """
    # Escape special characters to avoid breaking the XML structure
    escaped_text = sax.escape(
        user_text,
        entities={"'": "&apos;", '"': '&quot;'}
    )
    # Insert the escaped text into the template
    return xml_pattern.format(user_text=escaped_text)