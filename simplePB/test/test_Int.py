from nose.tools import assert_equals
from simplePB.encoding import Int

def test_Int_converts_to_proper_value():
	i = Int()

	assert_equals( 0b00000000, i.encode( 0 ) )
	assert_equals( 0b00000001, i.encode( 1 ) )
	assert_equals( 0b1001011000000001, i.encode( 150 ) )
	assert_equals( 0b1010110000000010, i.encode( 300 ) )
	assert_equals( 0b1111010000000011, i.encode( 500 ) )


def test_Int_correctly_decodes_value():
	i = Int()

	assert_equals( 0, i.decode( 0b00000000 ) )
	assert_equals( 1, i.decode( 0b00000001 ) )
	assert_equals( 150, i.decode( 0b1001011000000001 ) )
	assert_equals( 300, i.decode( 0b1010110000000010 ) )
	assert_equals( 500, i.decode( 0b1111010000000011 ) )
