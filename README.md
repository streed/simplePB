Simple Protocol Buffers
=======================
[![Build Status](https://travis-ci.org/streed/simplePB.png?branch=master)](https://travis-ci.org/streed/simplePB)

Info
====
This is a copy of the project that Google has that implements Protocol Buffers in a manner
that is cross language and is done off of their `.proto` files. 

Messages are descirbed by simply defining class such as the Person below.

```pythhon
    class Person( Protocol ):
     first_name = String( 10 ) #Max string length of 10.
     last_name = String( 10 )  #Max string length of 10.
     age = Int()               #Keep track of their age.
```

It is very clear what this `Person` entails: A `first_name`, `last_name`, and their `age`.
These attributes can be modified and changed as seen fit to best describe the `Person`.

```python
    me = Person()
    me.first_name = "Sean"
    me.last_name = "Reed"
    me.age = 21
```

The above describes `me` and sets up the _Protocol_ object to contain the required information.
When it comes to transmit or store this messge the `encode` method should be called. This
method will return a hex encoded string. The above message will become the following hex string
once it is printed out `002A09085365616E110852656564`. Once this is save the object can quickly
and easily be restored by calling the `decode` method and passing the above hex string to it.

The above way of describing the class is very natural and requires no outside dependencies,
besides this library.
