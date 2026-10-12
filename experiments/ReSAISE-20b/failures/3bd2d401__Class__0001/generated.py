import xml.sax.saxutils

# Example XML design template with a placeholder for user content.
xml_design = """
<response>
    <data>{input_data}</data>
</response>
"""

def process_xml_reply(input_data: str) -> str:
    """
    Insert user-provided content into the XML template safely.

    Parameters
    ----------
    input_data : str
        The raw user input that will be embedded in the XML response.

    Returns
    -------
    str
        A well‑formed XML string with the user content escaped to avoid injection.

    Notes
    -----
    - The function uses :func:`xml.sax.saxutils.escape` to neutralize
      special XML characters (<, >, &, ', ") so that the downstream consumer
      receives valid XML and cannot inject additional markup.
    - No exceptions are raised by this function; it simply returns the escaped
      content.  Caller code should handle any downstream errors if needed.
    """
    # Escape user input to prevent XML injection (CWE-74).
    safe_input = xml.sax.saxutils.escape(input_data, entities={"'": "&apos;", '"': "&quot;"})
    # Format the template with the escaped content.
    return xml_design.format(input_data=safe_input)

# Example usage
if __name__ == "__main__":
    user_input = "<script>alert('XSS');</script>"
    print(process_xml_reply(user_input))