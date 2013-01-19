
class Protocol( object ):
	"""
		A Protocol subclass will use the __ProtocolMetaClass to setup the field numbers and type values
		for the particular subclass.

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

		`_fields` - This will be a in order list of the fields as it comes across them in the 
				class's dictionary. Thus, they will be in alphabetical order.

	"""
	pass
