Simple Protocol Buffers
=======================
[![Build Status](https://travis-ci.org/streed/simplePB.png?branch=master)](https://travis-ci.org/streed/simplePB)

This is a copy of the project that Google has that implements Protocol Buffers in a manner
that is cross language and is done off of their `.proto` files. 

Messages are descirbed by simply defining class such as the Person below.

```python
class Person( Protocol ):
 first_name = String()
 last_name = String()
 age = Int()   #Keep track of their age.
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
When it comes to transmit or store this message the `encode` method should be called. This
method will return a hex encoded string. The above message will become the following hex string
once it is printed out `002A09085365616E110852656564`. After it has been saved the object can
quickly and easily be restored by calling the `decode` method and passing the above hex string 
to it.

Complex messages can easily be built up by nesting _Protocol_ classes inside of each other.
To extend on the _Person_ above we will make a _Family_ messge.

```python
class Family( Protocol ):
 father = Person()
 mother = Person()
 oldest_child = Person()
 youngest_child = Person()
```

Describing a family as the above _Family_ message is very easy and natural. It will again encode
into a hex string which can be transmitted or stored.

The above way of describing the class is very natural and requires no outside dependencies,
besides this library.

TODO
=====

 - [ ] Add _dict_ type support.
 - [ ] Add _tuple_ type support.
 - [ ] Add compression.
 - [ ] Add in _unicode_ support.
