import xml.sax.saxutils

# Example XML template with a placeholder for user input.
xml_template = """
<response>
    <data>{user_input}</data>
</response>
"""

def create_xml_output(user_input: str) -> str:
    """
    Generate an XML response by safely inserting the provided user input into a
    predefined XML template.

    Parameters:
        user_input (str): The raw string supplied by the user. It may contain
                          characters that need to be escaped for XML.

    Returns:
        str: A fully-formed XML document with the user content embedded.
    """
    # Escape special XML characters to prevent injection or malformed XML
    safe_input = xml.sax.saxutils.escape(user_input, entities={"'": "&apos;", "\"": "&quot;"})
    # Insert the escaped input into the template
    return xml_template.format(user_input=safe_input)

# Example usage:
if __name__ == "__main__":
    raw = "<script>alert('XSS');</script>"
    print(create_xml_output(raw))