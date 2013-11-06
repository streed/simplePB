import math
from .converter import Converter
from .integer import Integer

class List( Converter ):

	_int =	Integer()
	
	def __init__( self, encoder ):
		self.encoder = encoder


	def encode( self, value ):
		"""This will take a list `value` and convert
		all of its entries into the properly encoded value
		based on the self._encoder that was passed in at
		construction time."""
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
	
	def decode( self, value ):
		"""This will take the `value` and decode it
		into the original list."""
