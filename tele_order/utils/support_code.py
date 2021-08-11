
def trim_string(value):
    """ method remove whitespaces in string, if string is not None """
    double_whitespace = "  "
    if isinstance(value, str):
        if double_whitespace in value:
            return " ".join([word for word in value.strip().split()])
        return value.strip()
    elif value is not None:
        value = str(value)
        if double_whitespace in value:
            return " ".join([word for word in value.strip().split()])
        return value.strip()
    return value



