"""xml utils"""

import xml.etree.ElementTree as ET
import xml.dom.minidom as DOM
import lxml.etree as LET

def xmlPretty(root, indent=None):

    if indent is not None:
        i = indent
    else:
        i = "    "

    if root is not None:
        if not isinstance(root, ET.Element) and not isinstance(root, LET._Element):
            return None

    xDoc = DOM.parseString(ET.tostring(root))

    xPretty = xDoc.toprettyxml(indent=i)

    return xPretty
