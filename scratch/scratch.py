from lxml import etree as ET

def docstring_defaults(func):
    doc = func.__doc__ or ''
    doc += "\tverbose (bool): A flag to include flavor and footer text (default is False)" + "\n\tinvisible (bool): A flag to make the bot's reply invisible to everyone except you (default is False)"
    func.__doc__ = doc
    return func

@docstring_defaults
def foo():
    """Return info on a Gladius unit.

    Args:
        unitname (str): Name of unit to look up
    """
    print('asdf')
    print(foo.__doc__)

foo()