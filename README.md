Simple Protocol Buffers
=======================
[![Build Status](https://travis-ci.org/streed/simplePB.png?branch=master)](https://travis-ci.org/streed/simplePB)

Problem:
========

Defining a suitable communication protocol can be difficult and hard to maintain when new fields are added to the protocol at a later point.

Solution:
=========
Looking at the Google library [Protocol Buffers](https://developers.google.com/protocol-buffers) I found a conventient soluton to my problem.
But, I wanted to take it a step further and create a DSL on top of the protocol buffers themselves and from this allow for the following properties.

* Protocols are broken into _proto_ classes.
* Protocols are defined in _.pb_ files.
* The _.pb_ files are compiled into their equivalent Python classes.
* Objects sent will be serialized into a binary format that can be represented in Base64.
* Objects read can be deserialized back into their Python object.

This mimics the current Protocol Buffers offered by Google, but to allow for the flexibility for my projects I am building ontop of this and
adding the following additional functionality.

* Protocols can inherit from other Protocols.
* Protocols can overload member fields from inherited Protocols.

This above allows for the following situation

_header.pb_
```python
package example

proto Header ->
	id -> Int
	length -> Int

```

_message.pb_
```python
package example

import header.pb

proto Message | Header | ->
	message -> String
	from -> String
	to -> List:String
	timestamp -> Date

```

_heartbeat.pb_
```python
package example

import message.pb

proto HeartBeat | Message | ->
	heartbeatId -> Int

```
The above class hierarchy allows for a common base _Header_ class to be defined that then allows for common fields to be moved there and independently
modified with respect to its sub-class Protocols.
