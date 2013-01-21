from nose.tools import assert_equals, assert_true

from simplePB.protocol import Protocol
from simplePB.encoding import Int, String

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

	assert_equals( "0648AC02", t.encode() )

class Person( Protocol ):
	first_name = String()
	last_name = String()
	age = Int()

def test_Protocol_encodes_to_proper_values_with_intermixed_types():

	person = Person()

	person.first_name = "Sean"
	person.last_name = "Reed"
	person.age = 21

	assert_equals( "015945365616E11452656564", person.encode() )
