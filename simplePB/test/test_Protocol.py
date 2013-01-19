from nose.tools import assert_equals, assert_true

from simplePB.protocol import Protocol
from simplePB.encoding import Int

class Test( Protocol ):
	test_num = Int()
	another_num = Int()

	def __init__( self, test_num=0, another_num=0 ):
		Protocol.__init__( self )
		self.test_num = test_num
		self.another_num = another_num

def test_Protocol_add_the_required_methods():

	t = Test( test_num = 300, another_num = 100 )


	assert_true( "_fields" in dir( t ) )

def test_Protocol_encodes_the_values_properly():

	t = Test( test_num = 300, another_num = 100 )

	assert_equals( "006408AC02", t.encode() )
