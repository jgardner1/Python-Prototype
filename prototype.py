"""
prototype - A tiny python library that simulates prototype inheritence in javascript

# create a new type using @constructor
>>> from prototype import *
>>> @constructor
... def Person(this, first, last):
...   this.firstName = first
...   this.lastName = last
...
>>> Person
<constructor 'Person'>

# initialize an instance
>>> bird = Person('Charlie', 'Parker')
>>> bird.firstName
'Charlie'
>>> bird.lastName
'Parker'

# dynamically add attributes
>>> bird.instrument = 'alto sax'
>>> bird.instrument
'alto sax'

# unset attributes just return None
>>> print bird.age
None

# add methods to the instance
>>> def sing(this):
...   print '%s sings!!' % this.lastName
...
>>> bird.sing = sing
>>> bird.sing()
Parker sings!!

# use the prototype chain to add properties and methods to the type
>>> def getName(this):
...   return '%s %s' % (this.firstName, this.lastName)
...
>>> Person.prototype.name = property(getName)
>>> bird.name
'Charlie Parker'
>>> def greet(this):
...   print 'Hello, my name is %s' % this.name
...
>>> Person.prototype.greet = greet
>>> bird.greet()
Hello, my name is Charlie Parker
>>> monk = Person('Thelonious', 'Monk')
>>> monk.greet()
Hello, my name is Thelonious Monk

# property setter
>>> def setName(this, name):
...   first, last = name.split(' ')
...   this.firstName = first
...   this.lastName = last
...
>>> Person.prototype.name = property(getName, setName)
>>> bird.name = 'Dizzy Gillespie'
>>> bird.firstName
'Dizzy'
>>> bird.lastName
'Gillespie'

# property deleter
>>> def deleteName(this):
...   print 'Deleting %s.' % this.name
...   del this.firstName
...   del this.lastName
...
>>> Person.prototype.name = property(getName, setName, deleteName)
>>> del bird.name
Deleting Dizzy Gillespie.
>>> bird.name
'None None'

# using prototype inheritence
>>> father = Person('Tom', 'Bard')
>>> son = Person('Tommy', 'Bard')
>>> son.__proto__ = father
>>> father.eyeColor = 'blue'
>>> son.eyeColor
'blue'

# prototype chain relationships
>>> assert son.__proto__ == father
>>> assert son.constructor == father.constructor == Person
>>> assert father.__proto__ == Person.prototype
>>> assert Object.prototype.constructor == Object
>>> assert Person.prototype.constructor == Person
>>> assert Person.prototype.__proto__ == Object.prototype

# should work with lists
>>> father.children = [son]
>>> len(father.children)
1

# multi-level inheritence
>>> grandson = Person('Tony', 'Bard')
>>> grandson.__proto__ = son
>>> grandson.eyeColor
'blue'
"""

# I, Jonathan Gardner <jgardner@jonathangardner.net>, created a setup script
# and made superficial changes.  The original author is Toby Ho. See
# http://tobyho.com/Prototype_Inheritence_in_Python I assume it is in
# the public domain. I couldn't find any note of any license anywhere.

import new
import inspect

def _getattr(obj, name):
    # Jonathan Gardner: Really, missing attributes should throw an exception.
    return object.__getattribute__(obj, name)

def _setattr(obj, name, val):
    object.__setattr__(obj, name, val)

def _proto_getattr(obj, name):
    val = _getattr(obj, name)
    while val is None and obj is not None:
        obj = _getattr(obj, '__proto__')
        val = _getattr(obj, name)
    return val

class ObjectMetaClass(type):
    def __repr__(cls):
        return "<constructor '%s'>" % cls.__name__

class Object(object):
    __metaclass__ = ObjectMetaClass
    prototype = None
    
    def __init__(this):
        this.__proto__ = this.prototype
        this.constructor = this.__class__
    
    def __getattribute__(this, name):
        val = _proto_getattr(this, name)
        if isinstance(val, property) and val.fget:
            get = new.instancemethod(val.fget, this)
            return get()
        elif inspect.isfunction(val):
            func = new.instancemethod(val, this)
            return func
        else:
            return val
            
    def __setattr__(this, name, val):
        if not isinstance(val, property):
            _val = _proto_getattr(this, name)
            if isinstance(_val, property) and _val.fset:
                _val.fset(this, val)
                return
        _setattr(this, name, val)

    def __delattr__(this, name):
        val = _proto_getattr(this, name)
        if isinstance(val, property) and val.fdel:
            val.fdel(this)
        else:
            object.__delattr__(this, name)

Object.prototype = Object()

def constructor(func):
    ret = type(func.__name__, (Object,), dict())
    ret.prototype = ret()
    def init(this, *vargs, **kwargs):
        Object.__init__(this)
        func(this, *vargs, **kwargs)
    ret.__init__ = init
    return ret
