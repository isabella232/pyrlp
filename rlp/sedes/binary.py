from ..exceptions import SerializationError, DeserializationError
from ..utils import Atomic, str_to_bytes, bytes_to_str
import sys, binascii

class Binary(object):
    """A sedes object for binary data of certain length.
    
    :param min_length: the minimal length in bytes or `None` for no lower limit
    :param max_length: the maximal length in bytes or `None` for no upper limit
    :param allow_empty: if true, empty strings are considered valid even if
                        a minimum length is required otherwise
    """

    def __init__(self, min_length=None, max_length=None, allow_empty=False):
        self.min_length = min_length or 0
        self.max_length = max_length or float('inf')
        self.allow_empty = allow_empty

    @classmethod
    def fixed_length(cls, l, allow_empty=False):
        """Create a sedes for binary data with exactly `l` bytes."""
        return cls(l, l, allow_empty=allow_empty)

    @classmethod
    def is_valid_type(cls, obj):
        if sys.version_info.major == 2:
            return isinstance(obj, (str, unicode, bytearray))
        else:
            return isinstance(obj, (str, bytes))

    def is_valid_length(self, l):
        return any((self.min_length <= l <= self.max_length,
                    self.allow_empty and l == 0))

    def serialize(self, obj):
        if not Binary.is_valid_type(obj):
            raise SerializationError('Object is not a serializable ({})'.format(type(obj)), obj)
        if not self.is_valid_length(len(obj)):
            raise SerializationError('Object has invalid length', obj)
        if isinstance(obj, str):
            return str_to_bytes(obj)
        return obj

    def deserialize(self, serial):
        if not isinstance(serial, Atomic):
            raise DeserializationError('String has invalid length', serial)
        
        if self.is_valid_length(len(serial)):
            return bytes_to_str(serial)
        else:
            raise DeserializationError('String has invalid length', serial)


binary = Binary()
