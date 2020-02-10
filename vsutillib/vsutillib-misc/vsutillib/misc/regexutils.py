"""
Regular Expresions utils
"""

import re


def multiple_replace(adict, text):
    # Create a regular expression from all of the dictionary keys
    regex = re.compile("|".join(map(re.escape, adict.keys())))

    # For each match, look up the corresponding value in the dictionary
    return regex.sub(lambda match: adict[match.group(0)], text)


# def multipleReplace(d, text):
# Create a regular expression  from the dictionary keys
#    regex = re.compile("(%s)" % "|".join(map(re.escape, d.keys())))

# For each match, look-up corresponding value in dictionary
#    return regex.sub(lambda mo: d[mo.string[mo.start() : mo.end()]], text)


class Xlator(dict):
    """ All-in-one multiple-string-substitution class """
    def _makeRegex(self):
        """ Build re object based on the keys of the current dictionary """
        return re.compile("|".join(map(re.escape, self.keys())))

    def __call__(self, match):
        """ Handler invoked for each regex match """
        return self[match.group(0)]

    def xlat(self, text):
        """ Translate text, returns the modified text. """
        return self._makeRegex().sub(self, text)
