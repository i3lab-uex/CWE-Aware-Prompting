import xml.sax.saxutils

# Predefined XML template with a placeholder for user input.
xml_design = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <message>{input_data}</message>
</response>"""

def process_xml_reply(input_data: str) -> str:
    """
    Insert user-supplied content into the XML template.

    Parameters
    ----------
    input_data : str
        The raw text submitted by the user.  This value is escaped before
        being inserted into the XML to prevent injection of malformed tags.

    Returns
    -------
    str
        A well‑formed XML string with the escaped user content in place of
        the `{input_data}` placeholder.
    """
    # Escape XML special characters to avoid breaking the structure
    escaped_input = xml.sax.saxutils.escape(input_data, entities={"'": "&apos;", "\"": "&quot;"})
    # Perform the substitution
    return xml_design.format(input_data=escaped_input)