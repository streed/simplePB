import math

class Converter( object ):

  def encode( self, value ):
    """This will take the value and encode it into the
    proper format for this specfic type."""

  def decode( self, value ):
    """This will take an encoded value and decode it
    back to its original unencoded value."""

  #TODO: Find a faster method of doing this, or remove the need for it in the
  #first place.
  def _reverse_bits( self, n ):
    nn = 0

    bits = Converter.bit_count( n )
    while n > 0 and bits > 0:
      v = n & 0xFF
      nn = nn | ( v << bits )
      bits -= 8
      n = n >> 8

    return nn

  @classmethod
  def bit_count( cls, n ):
    bits = math.log( n, 2 )
    bits = int( math.ceil( bits / 8 ) * 8 ) - 8
    return bits
