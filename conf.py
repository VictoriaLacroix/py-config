import sys
# Configparser was renamed between versions, so let's import the right one.
if sys.version_info[0] == 2:
    from ConfigParser import ConfigParser
elif sys.version_info[0] == 3:
    from configparser import ConfigParser
import re

class ConfigFile():
    """
    Adapted from a helper method from Python Wiki.
    This class will hold a config file, and attempt to
    automatically convert values to ints or booleans.

    With example.ini as a test file:
    >>> c = ConfigFile('tests/example.ini')
    >>> c.get('Section One', 'Key')
    'Value'
    >>> c.get('Section One', 'Luggage_Combination')
    12345
    >>> c.getsection('Section Two')
    {'LOCATION': 'Hyrule', 'KEY': 'Value'}
    """
    def __init__(self, path):
        self.conf = ConfigParser()
        self.conf.read(path)

    def getsection(self, section):
        """
        Returns an entire section in a dict.
        The dict's keys will be uppercase, for convenience. 
        """
        keys = {}
        try:
            options = self.conf.options(section)
        except:
            return {}

        for opt in options:
            key = opt.upper()
            try:
                keys[key] = self.get(section, opt)
            except:
                keys[key] = None
        return keys

    def get(self, section, opt):
        """
        Gets a config value. This value will automatically
        be converted to a boolean, float or int.
        """
        try:
            key = self.conf.get(section, opt)
            if key == 'True':
                return True
            elif key == 'False':
                return False
            elif re.match('^[0-9]+$', key):
                return self.conf.getint(section, opt)
            elif re.match('^[0-9]+\.[0-9]+$', key):
                return self.conf.getfloat(section, opt)
            else:
                return key
        except:
            return None

if __name__ == '__main__':
    import doctest
    doctest.testmod()
