"""
Various helpers for working with classes
"""

import sys
import types


PYTHON_GE_3_6 = sys.version_info >= (3, 6)


def partial_class(cls, name, *args, **kwargs):
    """
    Create a subclass of ``cls`` identical to the original
    except for its name and additional arguments passed to ``__init__``

    :param cls: the class to be subclassed
    :param name: name of the new class
    :param args: positional arguments for ``__init__``
    :param kwargs: keyword arguments for ``__init__``
    :return: a subclass of ``cls``

    Say you have
    ::

        class Square:
            def __init__(self, size, color=None):
                pass  # implementation goes here

    The 'standard' way to subclass with fixed argument values would be to
    ::

        class RedSquare1x1(Square):
            def __init__(self):
                super().__init__(1, color='red)

    Consider the less-verbose alternative:
    ::

        RedSquare1x1 = partial_class(Square, 'RedSquare1x1', 1, color='red)
    """
    def new_init(self, *_args, **_kwargs):
        cls.__init__(self, *(args + _args), **dict(kwargs, **_kwargs))

    new_init.__name__ = '__init__'

    return types.new_class(
        name, (cls,), exec_body=lambda ns: (ns.__setitem__('__init__', new_init))
    )


class PartialProperty:
    """
    A descriptor that returns a :func:`partial_class` of the owner class when accessed.

    Basically it allows a class to have attributes that are its own subclasses:
    ::

        class Tree:
            Peach = PartialProperty(fruit='peach')
            Pine = PartialProperty(fruit='cone')
            # both will return subclasses of Tree when accessed

            def __init__(self, fruit):
                self.fruit = fruit

        issubclass(Tree.Pine, Tree)  # == True
        Tree.Pine().fruit  # == 'cone'
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self._cls_map = {}
        self._name = None  # type: str
        self._original_owner = None  # type: type

    def __set_name__(self, owner: type, name: str):
        self._name = name
        self._original_owner = owner
        self._cls_map[owner] = partial_class(owner, name, *self.args, **self.kwargs)

    def __get__(self, instance, owner):
        if not self._name:  # has not been set yet
            # get the name of the attribute - it will serve as the name
            # of the new partial class
            own_name = [
                name for name, attr in owner.__dict__.items()
                if attr is self
            ][0]
            self.__set_name__(owner=owner, name=own_name)

        return self._cls_map[self._original_owner]
