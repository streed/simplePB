from simplePB.encoding import Encode

class _ProtocolMetaClass( type ):

	def __new__( cls, name, bases, dct ):
		fields = []
		tmp = {}
		keys = dct.keys()
		keys.sort()
		for a in keys:
			tmp[a] = dct[a]
			if isinstance( dct[a], Encode ):
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


	def from_string( self, string ):
		"""
			This method will take a string and extract the values and assign the proper
			attribute it's associated value.
		"""
		pass

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

			header = ( _id << 3 ) | _type._TYPE
			body = _type.encode( v )
			
			fields.append( [ header, body ] )	
		
		return "".join( [ "%X%X" % ( h, b ) for h, b in fields ] )
