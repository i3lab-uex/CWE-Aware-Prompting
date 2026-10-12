import xml.sax.saxutils

# Example XML template with a placeholder for user input.
xml_design = """<?xml version="1.0" encoding="UTF-8"?>
<response>
    <content>{input_data}</content>
</response>"""


def process_xml_reply(input_data: str) -> str:
    """
    Insert the supplied user content into an XML template safely.

    Parameters
    ----------
    input_data : str
        The raw user-provided content to be embedded in the XML.

    Returns
    -------
    str
        The fully formed XML document with the user content inserted.
    """
    # Escape special XML characters to avoid injection or malformed XML
    safe_input = xml.sax.saxutils.escape(input_data, entities={"'": "&apos;", '"': "&quot;"})
    # Format the template with the escaped content
    return xml_design.format(input_data=safe_input)