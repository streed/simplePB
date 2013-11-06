import unittest
from ..converters.list import List
from ..converters.integer import Integer
from ..converters.string import String

class TestList( unittest.TestCase ):
	def test_List_encodes_the_values_correctly( self ):
		l = List( Integer() )
		tests = []
		tests.append( 1 )
		tests.append( 2 )
		tests.append( 3 )


		self.assertEquals( 0x06020406, l.encode( tests ) )

		l = List( String() )
		names = []
		names.append( "A" )
		names.append( "AB" )
		names.append( "ABC" )

		self.assertEquals( 0x06024104414206414243, l.encode( names ) )

	def test_List_decodes_the_values_correctly( self ):

		l = List( Integer() )
		tests = l.decode( 0x06020406 )

		self.assertEquals( [ 1, 2, 3 ], tests )

		l = List( String() )
		names = l.decode( 0x06024104414206414243 )

		self.assertEquals( [ "A", "AB", "ABC" ], names )
