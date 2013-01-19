[![Build Status](https://travis-ci.org/streed/simplePB.png?branch=master)](undefined)
Simple Protocol Buffers
=======================

This is a copy of the project that Google has that implements Protocol Buffers in a manner
that is cross language and is done off of their `.proto` files. 

It is done by describing the protocol messages through python classes.

    class Person( Protocol ):
     first_name = String( 10 ) #Max string length of 10.
     last_name = String( 10 )  #Max string length of 10.
     age = Int()               #Keep track of their age.


The above class very simply describes the data in the message and provides a few
constraints on the length of the first and last name strings.

Then to actually create a message you simply do the following:

    me = Person()
    me.first_name = "Sean"
    me.last_name = "Reed"
    me.age = 21

This will print out the hex string encoded value of this object:

    print me.encode()

That's all there is to make your protocol buffer classes and use them.
