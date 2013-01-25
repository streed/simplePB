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

	assert_equals( "00AC0208D804", t.encode() )

class Person( Protocol ):
	first_name = String()
	last_name = String()
	age = Int()

def test_Protocol_encodes_to_proper_values_with_intermixed_types():

	person = Person()

	person.first_name = "Sean"
	person.last_name = "Reed"
	person.age = 21

	assert_equals( "002A09085365616E110852656564", person.encode() )

def test_Protocol_decodes_and_sets_the_proper_fields():

	person = Person()

	person.decode( "002A09085365616E110852656564" )

	assert_equals( 21, person.age )
	assert_equals( "Sean", person.first_name )
	assert_equals( "Reed", person.last_name )
