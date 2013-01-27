import math

class Encode( object ):

	def __init__( self, **kwargs ):
		self._id = 0

	def _set_id( self, _id ):
		self._id = _id

	def encode( self, value ):
		raise NotImplemented( "An Encode subclass must define a `encode` method." )

	def decode( self, value ):
		raise NotImplemented( "An Encode subclass must define a `decode` method." )


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

class Int( Encode ):
	
	_TYPE = 0
	
	def encode( self, value ):
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

class String( Encode ):

	_TYPE = 1
	_int = Int()

	def encode( self, value ):
		if value == "":
			return 0

		length = String._int.encode( len( value ) )

		ret = length
		for c in value:
			ret = ( ret << 8 ) | ord( c )

		return ret

	def decode( self, value ):
		ret = []

		while value > 0:
			group = value & 0xFF
			ret.append( chr( group ) )

			value = value >> 8

		ret.reverse()

		return "".join( ret )


class List( Encode ):
	
	_TYPE = 2
	_int = Int()

	def __init__( self, encoder ):
		self.encoder = encoder


	def encode( self, value ):
		length = List._int.encode( len( value ) )

		ret = length
		shift = 0
		for v in value:
			temp = self.encoder.encode( v )	

			#get number of bits rounded to the nearest 8
			bits = math.log( temp, 2 )
			shift_distance = int( math.ceil( bits / 8 ) * 8 )
			ret = ( ret << shift_distance ) | temp
		
		return ret


