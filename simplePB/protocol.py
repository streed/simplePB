from simplePB.encoding import Encode, Int, String

class _ProtocolMetaClass( type ):

	def __new__( cls, name, bases, dct ):
		fields = []
		tmp = {}
		keys = dct.keys()
		keys.sort()
		for a in keys:
			tmp[a] = dct[a]
			if isinstance( dct[a], Encode ) and not a in [ "_int", "_string" ]:
				tmp["_%s" % a] = dct[a]
				tmp[a] = None
				fields.append( a )

		dct = tmp
		dct["_fields"] = fields

		return type.__new__( cls, name, bases, dct )
class Protocol( object ):
	"""
		For example:

		class Person( Protocol ):
			first_name = String( 10 )
			last_name = String( 10 )
			age = Int()

		This class will have the following methods added to it after instantiation.

		`new()` - Makes a new Person object with the values copied over this class, can only encode.
		`decode()` - This will decode a byte stream and make sure to parse it and will return a new 
				Person object.
		
		The following fields will exist in the Person class:

		`_fields` - This will be a _list_ will contain  the fields to encode. The list holds the 
			order in which they are encoded in the final output string. This is alphabetical
			order.

	"""

	__metaclass__ = _ProtocolMetaClass
	 
	_int = Int()
	_string = String()


	def encode( self ):
		"""
			This method will convert the current object into a hex string that represents
			the fields that this object contains.

			For example:

			class Simple( Protocol ):
				num = Int()

			s = Simple()
			s.num = 100

			print s.encode()

			"0064"
		"""
		fields = []
		for a in self._fields:
			_id = self._fields.index( a )
			v = getattr( self, a )
			_type = getattr( self, "_%s" % a )

			header = ( _id << 3 ) | ( _type._TYPE & 0b00000111 )
			body = self.__convert_body_to_string( _type.encode( v ) )
		
			fields.append(  ( header, body ) )
		
		return "".join( [ "%02X%s" % ( h, b ) for h, b in fields ] )

	
	def decode( self, value ):
		"""
			This method should receive a properly encoded string that represents a integer.
			The length of the string must be divisible by 2

			The function after parsing the integer will set the correct attributes to their
			respective values.
		"""
		value = "".join( reversed( [ value[i:i+2] for i in xrange( 0, len( value ), 2 ) ] ) )
		value = int( value, 16 )

		while value > 0:
			v = value & 0xFF

			_type = v & 0b00000111
			_id = ( v & 0b11111000 ) >> 3

			decoder = getattr( self, "_%s" % self._fields[_id] )

			value = value >> 8
			if _type == Int._TYPE:
				decoded_value, value = self.__get_integer( value )
				setattr( self, self._fields[_id], decoded_value )
			elif _type == String._TYPE:
				_str, value = self.__get_string( value )
				setattr( self, self._fields[_id], _str )
			else:
				value = value >> 8


	def __get_string( self, value ):
		"""
			This will return the string represented by the assocaited bytes.
			It will also advance _value_ along as it parses the string.
		"""
		length, value = self.__get_integer( value )

		_str = 0
		for i in xrange( length ):
			v = value & 0xFF
			_str = ( _str << 8 ) | v
			value = value >> 8

		return ( Protocol._string.decode( _str ), value )


	def __get_integer( self, value ):
		"""
			This will start where a integer is found and return the integer represented
			as well as the advanced _value_ to continue parsing.
		"""
		cont_int = True
		ret = 0
		while cont_int:
			v = value & 0x7F
			if v & 0x80 == 0:
				cont_int = False
			ret = ( ret << 8 ) | v	
			value = value >> 8

		ret = Protocol._int.decode( ret )

		return ( ret, value )


	def __convert_body_to_string( self, value ):
		"""
			Because of how the data is formated wherein each byte is represented by
			2 characters this will take the current _value_ which is a interger and
			convert it to a string such that every 8bits will be represented by 2
			hexidecimal characters.
		"""
		ret = []
		while value > 0:
			v = value & 0xFF
			ret.append( "%02X" % v )
			value = value >> 8

		ret.reverse()
		return "".join( ret )


