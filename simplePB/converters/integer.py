from .converter import Converter

class ZigZag( object ):
	@classmethod
	def encode( cls, v ):
		if v >= 0:
			return v << 1
		return ( v << 1 ) ^ ( ~0 )

	@classmethod
	def decode( cls, v ):
		if not v & 0x01:
			return v >> 1
		return ( v >> 1 ) ^ ( ~0 )

class Integer( Converter ):

	def encode( self, value ):
		"""This will encode a integer into a ZigZag encoding
		and produce a properly encoded integer."""
		if value == 0 :
			return 0

		value = ZigZag.encode( value )

		overflow = 0
		ret = 0
		while value > 0:
			group = value & 0x7F
			cont_bit = 1 if value > 0x7F else 0
			overflow = 1 if value & 0x80 == 0x80 else 0

			group = ( cont_bit << 7 ) | group
			ret = ( ret << 8 ) | group
			value = value >> 7
		
		if overflow == 1:
			ret = ( ret << 8 ) | overflow

		return ret
	
	def decode( self, value ):
		ret = 0
		shift = 0
		while value > 0:
			group = value & 0x7F
			ret = ( ret << 7 ) | group
			value = value >> 8
		return ZigZag.decode( ret )

