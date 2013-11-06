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

		self.assertEquals( int( "06020406", 16 ), l.encode( tests ) )

		l = List( String() )
		names = []
		names.append( "A" )
		names.append( "AB" )
		names.append( "ABC" )

		self.assertEquals( int( "06024104414206414243", 16 ), l.encode( names ) )

	def test_List_decodes_the_values_correctly( self ):

		#l = List( Integer() )
		#tests = l.decode( "020802040608" )

		#self.assertEquals( [ 1, 2, 3, 4 ], tests )

		#l = List( String() )
		#names = l.decode( "0206024104414206414243" )

		#self.assertEquals( [ "A", "AB", "ABC" ], names )
		pass
