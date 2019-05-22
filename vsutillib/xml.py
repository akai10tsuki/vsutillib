"""xml utils"""

import xml.dom.minidom as DOM

def xmlPretty(xmlString, indent=None):
    """
    pretty print xml string
    """

    i = "    "
    if indent is not None:
        i = indent

    xDoc = DOM.parseString(xmlString)

    if xDoc:
        xPretty = xDoc.toprettyxml(indent=i)

    return xPretty
