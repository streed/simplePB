import unittest
from ..converters.integer import Integer

class TestInteger( unittest.TestCase ):

	def test_Int_converts_to_proper_value( self ):
		i = Integer()

		self.assertEquals( 0b00000000, i.encode( 0 ) )
		self.assertEquals( 0b00000010, i.encode( 1 ) )
		self.assertEquals( 0b00000100, i.encode( 2 ) )
		self.assertEquals( 0b1010110000000010, i.encode( 150 ) )
		self.assertEquals( 0b1101100000000100, i.encode( 300 ) )
		self.assertEquals( 0b1110100000000111, i.encode( 500 ) )

	def test_Int_correctly_decodes_value( self ):
		i = Integer()

		self.assertEquals( 0, i.decode( 0b00000000 ) )
		self.assertEquals( 1, i.decode( 0b00000010 ) )
		self.assertEquals( 150, i.decode( 0b1010110000000010 ) )
		self.assertEquals( 300, i.decode( 0b1101100000000100 ) )
		self.assertEquals( 500, i.decode( 0b1110100000000111 ) )

	def test_Int_correctly_encodes_negatives( self ):
		i = Integer()

		self.assertEquals( 0b00000001, i.encode( -1 ) )
		self.assertEquals( 0b00000011, i.encode( -2 ) )
		self.assertEquals( 0b1100011100000001, i.encode( -100 ) )

	def test_Int_correctly_decodes_negatives( self ):
		i = Integer()

		self.assertEquals( -1, i.decode( 0b00000001 ) )
		self.assertEquals( -2, i.decode( 0b00000011 ) )
		self.assertEquals( -100, i.decode( 0b1100011100000001 ) )
