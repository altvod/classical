from unittest import TestCase

from classical.subclass import argumented_subclass, attributed_subclass


class TestPartials(TestCase):
    def test_argumented_subclass(self):
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

        Subclass = argumented_subclass(Base, 'Subclass', 123, d='qwerty')
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

    def test_attributed_subclass(self):
        class Base:
            attr_1 = 8
            attr_2 = 'abc'

            def __init__(self, a):
                self.a = a

            def works(self):
                return True

            @classmethod
            def class_works(cls):
                return True

            @staticmethod
            def static_works():
                return True

        Subclass = attributed_subclass(Base, 'Subclass', attr_2='qwerty', attr_3=5)
        self.assertEqual('Subclass', Subclass.__name__)
        self.assertEqual(Base.attr_1, Subclass.attr_1)
        self.assertEqual(
            'abc', Base.attr_2,
            msg='Original class\'s attribute was redefined'
        )
        self.assertEqual('qwerty', Subclass.attr_2)
        self.assertEqual(5, Subclass.attr_3)

        inst = Subclass(456)
        self.assertEqual(456, inst.a)
        self.assertEqual(Subclass.attr_1, inst.attr_1)
        self.assertEqual(Subclass.attr_2, inst.attr_2)
        self.assertEqual(Subclass.attr_3, inst.attr_3)

        # check method calling
        self.assertTrue(inst.works())
        self.assertTrue(Subclass.class_works())
        self.assertTrue(Subclass.static_works())
