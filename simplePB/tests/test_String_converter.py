import unittest
from ..converters.string import String

class TestString( unittest.TestCase ):
	def test_String_encodes_strings_properly( self ):
		string = String()

		self.assertEquals( 0x00, string.encode( "" ) )
		self.assertEquals( 0x0E74657374696E67, string.encode( "testing" ) )


	def test_String_decodes_to_string_properly( self ):
		string = String()

		self.assertEquals( "", string.decode( 0x00 ) )
		self.assertEquals( "testing", string.decode( 0x74657374696E67 ) )
