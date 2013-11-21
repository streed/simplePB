import unittest

from ..parser.grammar import *

class TestGrammar( unittest.TestCase ):

	def setUp( self ):
		global indentStack
		indentStack = [1]

	def test_import( self ):
		p = Import.parseString( "import test" )
		self.assertEquals( "test", p[0] )

	def test_packagename( self ):
		p = PackageName.parseString( "package examples" )

		self.assertEquals( "examples", p[0] )

	def test_nest_packagename( self ):
		p = PackageName.parseString( "package example.examples.exampless" )

		self.assertEquals( "example.examples.exampless", p[0] )

	def test_list( self ):
		p = List.parseString( "List:String" )
		self.assertEquals( { "List": "String" }, p[0] )

	def test_attribute_normal( self ):
		p = IndentedAttribute.parseString( "name -> String" )
		self.assertEquals( { "key": "name", "value": "String" }, p[0] )

	def test_attribute_list( self ):
		p = IndentedAttribute.parseString( "list -> List:Int" )
		self.assertEquals( { "key": "list", "value": { "List": "Int" } }, p[0] )

	def test_inheirtence( self ):
		p = InheritedProtocols.parseString( "| Test |" )

		self.assertEquals( "Test", p[0] )

	def test_protocol( self ):
		p = IndentedProtocol.parseString( "proto Person ->\n\tname -> String\n\tage -> Int\n" )
		self.assertEquals( { "name": "Person", "attributes": [ { "key": "name", "value": "String" },
								       { "key": "age", "value": "Int" } ] }, p[0] )

	def test_protocol_inherit( self ):
		p = IndentedProtocol.parseString( "proto Person | Test | ->\n\tname -> String\n\tage -> Int\n" )
		self.assertEquals( { "name": "Person", 
				     "parent": "Test", 
				     "attributes": [ { "key": "name", "value": "String" },
								       { "key": "age", "value": "Int" } ] }, p[0] )

	def test_protocoldescription( self ):
		p = ProtocolDescription.parseString( "package example\n\nproto Person ->\n\tname -> String\n\tage -> Int\n" )

		self.assertEquals( { 
					"package": "example", 
					"imports": [], 
					"protocol": { 
							"name": "Person", 
							"attributes": [ 
									{ "key": "name", "value": "String" },
								       	{ "key": "age", "value": "Int" } ] } }, p[0] )

	def test_protocoldescription_imports( self ):
		p = ProtocolDescription.parseString( "package example\nimport child\nproto Person ->\n\tname -> String\n\tage -> Int\n" )

		self.assertEquals( { 
					"package": "example", 
					"imports": [ "child" ], 
					"protocol": { 
							"name": "Person", 
							"attributes": [ 
									{ "key": "name", "value": "String" },
								       	{ "key": "age", "value": "Int" } ] } }, p[0] )

	def test_protocoldescirption_all( self ):
		p = ProtocolDescription.parseString( "package example\nimport child\nproto Person | Life | ->\n\tname -> String\n\tage -> Int\n" )

		self.assertEquals( { 
					"package": "example", 
					"imports": [ "child" ], 
					"protocol": { 
							"name": "Person", 
							"parent": "Life",
							"attributes": [ 
									{ "key": "name", "value": "String" },
								       	{ "key": "age", "value": "Int" } ] } }, p[0] )

