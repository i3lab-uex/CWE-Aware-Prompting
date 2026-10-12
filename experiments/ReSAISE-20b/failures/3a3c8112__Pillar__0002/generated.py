import html

def construct_html_response(content: str, html_template: str) -> str:
    """
    Construct an HTML response by safely inserting user-provided content
    into the supplied template.

    Parameters:
        content (str): The dynamic content supplied by the user.
        html_template (str): An HTML string containing a `{user_content}`
                             placeholder where the escaped content will be inserted.

    Returns:
        str: The final HTML string with the user content properly escaped.
    """
    # Ensure we have a string to escape; if None or other type, convert to str
    user_content = "" if content is None else str(content)

    # Escape the content to neutralize HTML special characters
    escaped_content = html.escape(user_content, quote=True)

    # Safely format the template with the escaped content
    try:
        final_html = html_template.format(user_content=escaped_content)
    except KeyError as e:
        raise ValueError(f"Missing placeholder in template: {e}") from None

    return final_html