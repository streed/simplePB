from .converter import Converter
from .integer import Integer

class String( Converter ):
	"""This is a converter for a string datatype that allows
	for the encoding and decoding of strings."""

	#Private Integer that is used to serialize/deserialize
	#the length of the string.
	_int = Integer()

	def encode( self, value ):
		"""This will take the string `value` and encode it into the following
		format: <length><string bytes>
		
		value -> is a string to be converted.
		
		ret -> is a binary representation that is in the format <length><string bytes>"""
		if value == "":
			return 0

		length = String._int.encode( len( value ) )

		ret = length
		for c in value:
			ret = ( ret << 8 ) | ord( c )

		return ret

	def decode( self, value ):
		"""This will take the encoded string and convert it back to its
		proper string value.
		
		value -> is a integer that can be converted into a string."""
		ret = []

		while value > 0:
			group = value & 0xFF
			ret.append( chr( group ) )

			value = value >> 8

		ret.reverse()

		return "".join( ret )

	def _get( self, value ):
		#Get the lenght of the string.
		l, value = self._int._get( value )

		#Move through the string l number of 
		#characters.
		s = 0
		for i in range( l ):
			v = value & 0xFF
			s = ( s << 8 ) | v
			value = value >> 8

		#What we have gotten is a giant integer,
		#so convert it back into a python string.
		s = self.decode( s )

		return s, value

