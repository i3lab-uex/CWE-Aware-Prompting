import html

def generate_html_response(user_content: str, *, html_template: str) -> str:
    """
    Generate an HTML response by safely embedding the user-provided content
    into the given template.

    Parameters:
        user_content (str): The raw content supplied by the user.
        html_template (str): An HTML template containing a single
                             placeholder `{user_content}`.

    Returns:
        str: The resulting HTML string with the user content escaped
             to prevent XSS or markup injection.

    Note:
        - This function uses `html.escape` to neutralize any HTML
          special characters in the user content.
        - It assumes that `html_template` contains exactly one
          `{user_content}` placeholder; if not, a `KeyError`
          will be raised.
    """
    # Escape user content to prevent injection attacks
    safe_content = html.escape(user_content, quote=True)

    # Format the template with the escaped content
    try:
        response = html_template.format(user_content=safe_content)
    except KeyError as exc:
        raise ValueError(
            f"Template missing required placeholder: {exc}"
        ) from exc

    return response