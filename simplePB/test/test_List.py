from nose.tools import assert_equals, assert_true


from simplePB.encoding import List, Int, String
from simplePB.protocol import Protocol

class Tests( Protocol ):
	scores = List( Int() )

class Names( Protocol ):
	names = List( String() )

def test_List_encodes_the_values_correctly():
	tests = Tests()

	tests.scores.append( 1 )
	tests.scores.append( 2 )
	tests.scores.append( 3 )

	assert_equals( "0206020406", tests.encode() )

	names = Names()
	names.names.append( "A" )
	names.names.append( "AB" )
	names.names.append( "ABC" )

	assert_equals( "0206024104414206414243", names.encode() )

def test_List_decodes_the_values_correctly():

	test = Tests()

	test.decode( "020802040608" )

	assert_equals( [ 1, 2, 3, 4 ], test.scores )

	names = Names()

	names.decode( "0206024104414206414243" )

	assert_equals( [ "A", "AB", "ABC" ], names.names )
