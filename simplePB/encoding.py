import math

class Encode( object ):

	def __init__( self ):
		pass

	def encode( self, value ):
		raise NotImplemented( "An Encode subclass must define a `encode` method." )

	def decode( self, value ):
		raise NotImplemented( "An Encode subclass must define a `decode` method." )


class Int( Encode ):
	
	def encode( self, value ):
		if value == 0 :
			return 0

		groups = []
		overflow = 0
		while value > 0:
			group = value & 0x7F
			cont_bit = 1 if value > 0x7F else 0
			overflow = 1 if value & 0x80 == 0x80 else 0

			group = ( cont_bit << 7 ) | group
			groups.append( group )
			value = value >> 7

		if overflow == 1:
			groups.append( overflow )

		ret = 0
		shift = 0
		for i in groups[::-1]:
			ret = ret | ( i << shift )	
			shift += 8

		return ret

	def decode( self, value ):
		ret = 0
		shift = 0
		while value > 0:
			group = value & 0x7F

			ret = ( ret << shift ) | group

			shift += 7

			value = value >> 8

		return ret

