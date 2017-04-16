from unittest import TestCase

from classical.partials import partial_class


class TestPartials(TestCase):
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
