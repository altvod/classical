from unittest import TestCase

from classical.tools import partial_class, PartialProperty, AutoProperty


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
        class Polygon:
            Blue = PartialProperty(color='blue')
            Pentagon = PartialProperty(sides=5)

            def __init__(self, color=None, sides=3):
                self.color = color
                self.sides = sides

        blue_pentagon = Polygon.Pentagon.Blue()
        self.assertEqual(5, blue_pentagon.sides)
        self.assertEqual('blue', blue_pentagon.color)

    def test_auto_property(self):
        class Thing:
            book = AutoProperty(color='brown', has='pages')
            lamp = AutoProperty(color='white', has='light')
            # both will return instances of Thing when accessed

            def __init__(self, color, has):
                self.color = color
                self.has = has

        self.assertTrue(isinstance(Thing.book, Thing))
        self.assertIs(Thing, type(Thing.book))
        self.assertEqual('brown', Thing.book.color)
        self.assertEqual('pages', Thing.book.has)
        self.assertIs(Thing.book, Thing.book, msg='Subsequent calls return different instances')
        self.assertIs(Thing.book, Thing.book.book)

    def test_auto_property_in_subclass(self):
        class Thing:
            book = AutoProperty(has='pages')

            def __init__(self, has):
                self.has = has

        class ClassyThing(Thing):
            pass

        self.assertIsInstance(ClassyThing.book, ClassyThing)
        self.assertEqual('pages', ClassyThing.book.has)
        self.assertIs(ClassyThing.book, ClassyThing.book.book)
        self.assertIsNot(Thing.book, ClassyThing.book.book)

    def test_property_combination(self):
        class Thing:
            Blue = PartialProperty(color='blue')
            Red = PartialProperty(color='red')

            book = AutoProperty(has='pages')
            lamp = AutoProperty(has='light')

            def __init__(self, color, has):
                self.color = color
                self.has = has

        self.assertIsInstance(Thing.Red.book, Thing.Red)
        self.assertEqual('red', Thing.Red.book.color)
        self.assertEqual('pages', Thing.Red.book.has)
