import unittest

from ..parser.generators.klass import Klass

class TestKlass( unittest.TestCase ):

	SIMPLE_FILE = """import simplePB

class Person:
    __metaclass__ = simplePB.metaclass.GeneratedMetaclass
    name = String()
    age = Int()
"""
	MEMBER_LIST_FILE = """import simplePB

class Person:
    __metaclass__ = simplePB.metaclass.GeneratedMetaclass
    name = List( String() )
    age = Int()
"""
	INCLUDES_FILE = """import simplePB
import Child
class Person:
    __metaclass__ = simplePB.metaclass.GeneratedMetaclass
    name = String()
    age = Int()
"""
	def test_generate_proper_file( self ):
		p = {	
				"package": "example", 
				"includes": [], 
				"protocol": { 
						"name": "Person", 
						"attributes": [ 
								{ "key": "name", "value": "String" },
								{ "key": "age", "value": "Int" } ] } }
		c = Klass( includes=p["includes"], **p["protocol"] )	
		self.assertEquals( self.SIMPLE_FILE, c.generate() )
	
	def test_generate_file_with_imcludes( self ):
		child = {	
				"package": "example", 
				"includes": [], 
				"protocol": { 
						"name": "Child", 
						"attributes": [ 
								{ "key": "name", "value": "String" },
								{ "key": "age", "value": "Int" } ] } }
		p = {	
				"package": "example", 
				"includes": [ child ], 
				"protocol": { 
						"name": "Person", 
						"attributes": [ 
								{ "key": "name", "value": "String" },
								{ "key": "age", "value": "Int" } ] } }
		c = Klass( includes=p["includes"], **p["protocol"] )	
		self.assertEquals( self.INCLUDES_FILE, c.generate() )

	def test_generate_file_with_list_member( self ):
		p = {	
				"package": "example", 
				"includes": [], 
				"protocol": { 
						"name": "Person", 
						"attributes": [ 
								{ "key": "name", "value": { "List": "String" } },
								{ "key": "age", "value": "Int" } ] } }
		c = Klass( includes=p["includes"], **p["protocol"] )	
		self.assertEquals( self.MEMBER_LIST_FILE, c.generate() )
