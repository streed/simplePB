import unittest

from ..parser.grammar import *

class TestGrammar( unittest.TestCase ):

	def setUp( self ):
		global indentStack
		indentStack = [1]

	def test_include( self ):
		p = Include.parseString( "include test.pb" )
		self.assertEquals( "test.pb", p[0] )

	def test_packagename( self ):
		p = PackageName.parseString( "package examples" )

		self.assertEquals( "examples", p[0] )

	def test_list( self ):
		p = List.parseString( "List:String" )
		self.assertEquals( { "List": "String" }, p[0] )

	def test_attribute_normal( self ):
		p = Attribute.parseString( "name -> String" )
		self.assertEquals( { "key": "name", "value": "String" }, p[0] )

	def test_attribute_list( self ):
		p = Attribute.parseString( "list -> List:Int" )
		self.assertEquals( { "key": "list", "value": { "List": "Int" } }, p[0] )

	def test_protocol( self ):
		p = IndentedProtocol.parseString( "proto Person ->\n\tname -> String\n\tage -> Int\n" )
		self.assertEquals( { "name": "Person", "attributes": [ { "key": "name", "value": "String" },
								       { "key": "age", "value": "Int" } ] }, p[0] )
	def test_protocoldescription( self ):
		p = ProtocolDescription.parseString( "package example\n\nproto Person ->\n\tname -> String\n\tage -> Int\n" )

		self.assertEquals( { 
					"package": "example", 
					"includes": [], 
					"protocol": { 
							"name": "Person", 
							"attributes": [ 
									{ "key": "name", "value": "String" },
								       	{ "key": "age", "value": "Int" } ] } }, p[0] )

	def test_protocoldescription_includes( self ):
		p = ProtocolDescription.parseString( "package example\ninclude child.pb\nproto Person ->\n\tname -> String\n\tage -> Int\n" )

		self.assertEquals( { 
					"package": "example", 
					"includes": [ "child.pb" ], 
					"protocol": { 
							"name": "Person", 
							"attributes": [ 
									{ "key": "name", "value": "String" },
								       	{ "key": "age", "value": "Int" } ] } }, p[0] )

