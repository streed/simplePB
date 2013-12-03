from .converter import Converter

class ZigZag( object ):
	"""This allows for integers to be represented without
	a sign. It does this by making all positive integers
	map to the even numbers and all negative integers
	map to the odd numbers. Because both of these sets
	are the same size they can map naturally."""
	
	@classmethod
	def encode( cls, v ):
		"""Given a value v the v will be encoded such that if 
		it is a positive number then it will be mapped to an
		even integer and if it is a negative number then it 
		will be mapped to an odd integer.
		
		v - Integer to convert."""
		if v >= 0:
			return v << 1
		return ( v << 1 ) ^ ( ~0 )

	@classmethod
	def decode( cls, v ):
		"""Given a value that is a integer that is either
		even or odd then the value v will be converted to
		the original representation.
		
		v - Integer to be converted to its original value."""
		if not v & 0x01:
			return v >> 1
		return ( v >> 1 ) ^ ( ~0 )

class Integer( Converter ):

	def encode( self, value ):
		"""This will encode a integer into a ZigZag encoding
		and produce a properly encoded integer."""
		if value == 0 :
			return 0

		#We only want to work with positive integers.
		value = ZigZag.encode( value )

		overflow = 0
		ret = 0
		#Convert the 
		while value > 0:
			#Use everything but the last bit.
			group = value & 0x7F
			#Do we have a larger value?
			cont_bit = 1 if value > 0x7F else 0
			#Does the value overflow?
			overflow = 1 if value & 0x80 == 0x80 else 0

			group = ( cont_bit << 7 ) | group
			ret = ( ret << 8 ) | group
			value = value >> 7
		
		#We overflowed, so tack on the overflow bit
		#To the integer.
		if overflow == 1:
			ret = ( ret << 8 ) | overflow

		return ret
	
	def decode( self, value ):
		"""This will decode value as if it is a integer."""
		ret = 0
		shift = 0
		
		#Convert back to a integer from the larger value.
		while value > 0:
			group = value & 0x7F
			ret = ( ret << 7 ) | group
			value = value >> 8

		#We may have a positive or negative number
		#but it is a encoded value so decode it back.
		return ZigZag.decode( ret )


	def _get( self, value ):
		cont = True
		ret = 0

		while cont:
			v = value & 0x7F
			if v & 0x80 == 0:
				cont = False
			ret = ( ret << 8 ) | v
			value = value >> 8

		ret = self.decode( ret )

		return ret, value 
