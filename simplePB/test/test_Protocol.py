from nose.tools import assert_equals, assert_true

from simplePB.protocol import Protocol
from simplePB.encoding import Int, String

class Test( Protocol ):
	test_num = Int()
	another_num = Int()

	def __init__( self, test_num=0, another_num=0 ):
		self.test_num = test_num
		self.another_num = another_num

def test_Protocol_add_the_required_methods():

	t = Test( test_num = 300, another_num = 100 )


	assert_true( "_fields" in dir( t ) )

def test_Protocol_encodes_the_values_properly():

	t = Test( test_num = 300, another_num = 150 )

	assert_equals( "0AC028D804", t.encode() )

class Person( Protocol ):
	first_name = String()
	last_name = String()
	age = Int()

def test_Protocol_encodes_to_proper_values_with_intermixed_types():

	person = Person()

	person.first_name = "Sean"
	person.last_name = "Reed"
	person.age = 21

	assert_equals( "02A985365616E11852656564", person.encode() )
