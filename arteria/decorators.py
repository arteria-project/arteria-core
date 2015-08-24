def undocumented(f):
    """
    Apply the undocumented decorator to handler methods if they should not turn up in the API help
    """
    f.undocumented = True
    return f

