from nose.tools import assert_equals, assert_true

from simplePB.encoding import String

def test_String_encodes_strings_properly():
	string = String()

	assert_equals( 0x00, string.encode( "" ) )
	assert_equals( 0x0774657374696E67, string.encode( "testing" ) )

def test_String_decodes_to_string_properly():
	string = String()

	assert_equals( "", string.decode( 0x00 ) )
	assert_equals( "testing", string.decode( 0x74657374696E67 ) )
