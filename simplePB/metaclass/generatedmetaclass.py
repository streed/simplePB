
def _serialize( self, out=0 ):
  if( out == 0 ):
    return simplePB.representation.concatBinary( self._fields )
  elif( out == 1 ):
    return simplePB.representation.binaryToHex( self._serialize( out=0 ) )


class GeneratedMetaclass( type ):

  def __new__( meta, cls, bases, dct ):
    """
      In order to make sure that the classes work the following needs
      to be added to the generated classes:
        - binary
         - This is a property that when accessed will return the binary representation.
        - hex
         - This is a property that when accessed will return the hex string represenation.

        Both of the above properties will call the _serialize method. This method will
        be a function chain calling each of the attributes in turn concating the result.

          class Person:
            __meta__ == ...

            name = String()
            age = Int()

        During the initialization phase the following methods will be added to the above class:

            def _serialize( self, out=simplePB.representation.binary ):
              if( out == simplePB.representation.binary ):
                return simplePB.representation.concatBinary( [ self._name.serialize, self._age.serialize ] )
              elif( out == simplePB.representation.hex ):
                return simplePB.representation.binaryToHex( simplePB.representation.concatBinary( [ self._name.serialize, self._age.serialize ] ) )

            @Property
            def binary( self ):
              return self._serialize()

            @Property
            def hex( self ):
              return self._serialize( out=simplePB.representation.hex )

    """
    dct["_serialize"] = _serialize


    return type.__new__( meta, cls, bases, dct )
