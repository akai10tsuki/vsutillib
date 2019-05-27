"""
Maintain configuration in a dictionary it can save it
on an xml file.

Args:
    configFile (str): xml file name or Path object

Raises:
    ValueError: Raised when the xml file can not be created
                when first run and the file still don't exist

Examples:

    >>> cfg = ConfigurationSettings('file.xml')
    >>> value = "Configuration Value"
    >>> value
    'Configuration Value'
    >>> cfg.set('key', value)
    >>> cfg.get('key')
    'Configuration Value'
    >>> cfg.saveToFile()
    >>> cfg2 = ConfigurationSettings('file.xml')
    >>> cfg2.readFromFile()
    >>> value2 = cfg2.get('key')
    >>> value2
    'Configuration Value'


keys have to be strings

It works with basic data types:

    basic data types and lists, dictionaries,
    tuples or sets of these data types

    - bool, byes, numbers: int, float, complex, strings, set

    theese types can be saved but not in lists, dictionaries,
    tuples or sets

    - range, bytearray, frozenset

binary data that can converted to base64 and save as bytes
can work the conversion from byres to binary is not
manage by the class
"""

#CM0002

import ast
import logging
import pickle
import base64

import xml
import xml.etree.ElementTree as ET
import xml.dom.minidom as DOM

from pathlib import Path

MODULELOG = logging.getLogger(__name__)
MODULELOG.addHandler(logging.NullHandler())

class ConfigurationSettings:
    """
    Manage configuration settings

    The class is iterable returning key, value pairs
    """

    def __init__(self, configFile=None, log=False):

        self._config = {}
        self._log = log
        self._configFile = configFile

        # data that can be treated as literal
        # theese are human readable easier
        # to use on different system
        self._literal = ['bool', 'bytes', 'complex',
                         'float', 'int', 'str',
                         'dict', 'list', 'tuple',
                         'set']

        # pickable types are python specific maybe
        # even version specific
        self._pickable = ['range', 'bytearray', 'frozenset']

        # for iteration
        self._current = 0
        self._len = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._current >= self._len:
            self._current = 0
            raise StopIteration
        else:
            self._current += 1
            key = list(self._config)[self._current - 1]
            return [key, self._config[key]]

    def __bool__(self):
        return len(self._config)

    def __len__(self):
        return len(self._config)

    def set(self, key, value):
        """
        set configuration item the key must be a string
        value can be basic data type
        with dict, list, tuples of basic types

        :param key: configuration element
        :type key: str
        :param value: element value
        :type value: basic data type
        """

        if isinstance(key, str):
            self._config[key] = value
            self._len = len(self._config)
        else:
            if self._log:
                s = str(key)
                MODULELOG.debug('CM0002: key must be a string - %s', str(s))
            raise TypeError('key must be a string')

    def get(self, key):
        """
        get configuration item

        :param key: configuration element
        :type key: str
        :rtype: object
        """

        if key in self._config:
            return self._config[key]

        if self._log:
            s = str(key)
            MODULELOG.debug('CM0001: key not found - %s', s)

        return None

    def toXML(self, root=None, name=None):
        """
        Returns the configuration in XML format
        if root is None returns the current configuration

        :rtype: xml.etree.ElementTree.Element
        """

        if name is None:
            name = "Config"

        config = ET.Element(name)

        if root is not None:
            root.append(config)

        for key, value in self:
            valueType = type(value).__name__

            if valueType in self._literal:
                tValue = value
            elif valueType in self._pickable:
                print(valueType)
                p = pickle.dumps(value)
                u = base64.b64encode(p)
                tValue = u

            configElement = ET.SubElement(config, 'ConfigSetting')
            configElement.attrib = {'id': key, 'type': type(value).__name__}
            configElement.text = str(tValue)

        if root is None:
            return config

        return root

    def fromXML(self, xmlDoc, name=None):
        """
        Restore configuration from xml name parameter
        permit various configuration sets on same
        xml document

        :param xmlDoc: xml document containing configuration data
        """
        self._config = {}

        if name is None:
            searchIn = "Config/ConfigSetting"
        else:
            searchIn = name + "/ConfigSetting"

        for setting in xmlDoc.findall(searchIn):

            key = setting.attrib['id']

            if setting.attrib['type'] == "str":
                value = setting.text
            elif setting.attrib['type'] in self._pickable:
                u = ast.literal_eval(setting.text)
                value = pickle.loads(base64.b64decode(u))
            else:
                value = ast.literal_eval(setting.text)

            self.set(key, value)

    def xmlPrettyPrint(self, root=None):
        """
        Returns configuration xml Pretty Printed

        :rtype: xml.dom.minidom
        """

        if root is not None:
            if not isinstance(root, xml.etree.ElementTree.Element):
                return None
        else:
            root = self.toXML()

        xmlDoc = DOM.parseString(ET.tostring(root))

        xmlPretty = xmlDoc.toprettyxml(indent='    ')

        return xmlPretty

    def setConfigFile(self, xmlFile):
        """file to read/save configuration"""

        p = Path(xmlFile)

        if not p.anchor:
            xf = Path(Path.home(), xmlFile)
        else:
            xf = p

        self._configFile = xf

    def saveToFile(self, xmlFile=None, rootName=None):
        """save configuration to file in xml format"""

        xf = xmlFile
        if xmlFile is None:
            xf = self._configFile

        if rootName is None:
            rootTag = "VergaraSoft"

        root = ET.Element(rootTag)

        xmlConfig = self.toXML(root)
        tree = ET.ElementTree(xmlConfig)
        tree.write(str(xf))

    def readFromFile(self, xmlFile=None):
        """read from xml file"""

        xf = xmlFile
        if xmlFile is None:
            xf = self._configFile

        f = Path(xf)

        if f.is_file():
            tree = ET.ElementTree(file=str(xf))
            root = tree.getroot()

            self.fromXML(root)

def test():
    """Testing ead and write configuration to file"""

    configFile = Path(Path.cwd(), 'configmanager.xml')
    xmlFile = str(configFile)

    b = b'bytestring'
    configuration = ConfigurationSettings()
    configuration.set('range', range(13))
    configuration.set('set', {'r', 'n', 'a', 'f', 'e', 'i'})
    configuration.set('bytearray', bytearray(b'Itsue'))
    configuration.set('frozenset', frozenset('Itsue'))
    configuration.set('bool', True)
    configuration.set(
        'base64sting',
        'AdnQywACAAAAAAHmAAAAoAAACM4AAAR5AAAB7wAAAMYAAAjFAAAEcAAAAAAAAAAACgA='
    )
    configuration.set(
        'base86bytes',
        'AdnQywACAAAAAAHmAAAAoAAACM4AAAR5AAAB7wAAAMYAAAjFAAAEcAAAAAAAAAAACgA='.encode()
    )
    configuration.set('dict', {'key1': 1, 'key2': 2, 3: b})
    configuration.set('list', [2, 3, 'list', {'key1': 1, 2: [2]}])
    configuration.set('int', 13)
    configuration.set('float', 1.3e200)
    configuration.set('complex', 1+3j)
    configuration.set('tuple', (1.11, 2.22, 3.33))

    print('\nConfiguration set\n')
    for key, value in configuration:
        print('Key = {0}, type = {2} value = {1}'.format(key, value, type(value).__name__))

    configuration.saveToFile(xmlFile)

    configuration.readFromFile(xmlFile)

    root = configuration.toXML()

    print('\nRead from configuration file\n')
    for key, value in configuration:
        print('Key = {0}, type = {2}, value = {1}'.format(key, value, type(value).__name__))

    prettyXML = configuration.xmlPrettyPrint(root)

    print()
    print(prettyXML)

if __name__ == "__main__":
    test()
