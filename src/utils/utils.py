def truncate_sentences(text, char_limit=280):
    """
    Truncate the given text to a length that fits within the Twitter character limit.

    Args:
        text (str): The text to truncate.
        char_limit (int, optional): The maximum length of the text. Defaults to 280.

    Returns:
        str: The truncated text.
    """
    if len(text) <= char_limit:
        return text
    else:
        sentences = text.split('. ')
        truncated_text = ''
        for sentence in sentences:
            if len(truncated_text + sentence + '. ') <= char_limit:
                truncated_text += sentence + '. '
            else:
                break
        return truncated_text.rstrip()
