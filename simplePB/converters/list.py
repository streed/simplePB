import math
from .converter import Converter
from .integer import Integer

class List( Converter ):
	"""This will properly encode/decode a list of Convertable
	objects, such as Protocols, Integers, and Strings.
	
	Lists can only hold a single type of values, unlike
	a typical python list where different kinds of objects"""
	
	#Private Integer to serialize/deserialize the length
	#of the list.
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
		for v in value:
			temp = self.encoder.encode( v )        

			#TODO: Move this into a util function.
			#Get number of bits rounded to the nearest 8
			bits = math.log( temp, 2 )
			shift_distance = int( math.ceil( bits / 8 ) * 8 )
			ret = ( ret << shift_distance ) | temp

		return ret
	
	def decode( self, value ):
		"""This will take the `value` and decode it
		into the original list."""

		#Bits are reversed because of how they are
		#encoded.
		value = self._reverse_bits( value )

		#Get the length of the list,
		ret = []
		l, value = self._int._get( value )

		#Loop over the values l times.
		for _ in range( l ):
			v, value = self.encoder._get( value )
			ret.append( v )

		return ret




