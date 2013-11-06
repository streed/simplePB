from .converter import Converter
from .integer import Integer

class String( Converter ):

	_int = Integer()

	def encode( self, value ):
		"""This will take the string `value` and encode it into the following
		format: <length><string bytes>"""
		if value == "":
			return 0

		length = String._int.encode( len( value ) )

		ret = length
		for c in value:
			ret = ( ret << 8 ) | ord( c )

		return ret

	def decode( self, value ):
		"""This will take the encoded string and convert it back to its
		proper string value."""
		ret = []

		while value > 0:
			group = value & 0xFF
			ret.append( chr( group ) )

			value = value >> 8

		ret.reverse()

		return "".join( ret )
