from unittest import TestCase

from classical.tools import partial_class, PartialProperty


class TestTools(TestCase):
    def test_partial_class(self):
        class Base:
            clsattr = 8

            def __init__(self, a, b, c=None, d=None):
                self.a = a
                self.b = b
                self.c = c
                self.d = d

            def works(self):
                return True

            @classmethod
            def class_works(cls):
                return True

            @staticmethod
            def static_works():
                return True

        Subclass = partial_class(Base, 'Subclass', 123, d='qwerty')
        self.assertEqual('Subclass', Subclass.__name__)
        self.assertEqual(Base.clsattr, Subclass.clsattr)

        inst = Subclass(456)
        self.assertEqual(Base.clsattr, inst.clsattr)
        self.assertEqual(123, inst.a)
        self.assertEqual(456, inst.b)
        self.assertEqual(None, inst.c)
        self.assertEqual('qwerty', inst.d)

        # check method calling
        self.assertTrue(inst.works())
        self.assertTrue(Subclass.class_works())
        self.assertTrue(Subclass.static_works())

    def test_partial_property(self):
        class Tree:
            Peach = PartialProperty(fruit='peach')
            Pine = PartialProperty(fruit='cone')

            def __init__(self, fruit):
                self.fruit = fruit

        self.assertTrue(issubclass(Tree.Peach, Tree))
        self.assertEqual('Peach', Tree.Peach.__name__)
        self.assertIsInstance(Tree.Peach(), Tree)
        self.assertEqual('peach', Tree.Peach().fruit)
        self.assertEqual('cone', Tree.Pine().fruit)
        self.assertIs(Tree.Peach, Tree.Peach, msg='Subsequent calls return different subclasses')

    def test_partial_property_recursion(self):
        class Tree:
            Peach = PartialProperty(fruit='peach')

            def __init__(self, fruit):
                self.fruit = fruit

        self.assertIs(Tree.Peach, Tree.Peach.Peach)
        self.assertIs(Tree.Peach, Tree.Peach.Peach.Peach.Peach.Peach)
