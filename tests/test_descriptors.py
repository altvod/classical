from unittest import TestCase

from classical.descriptors import PartialProperty, AutoProperty


class TestTools(TestCase):
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

            def __init__(self, color=None, has=None):
                self.color = color
                self.has = has

        self.assertIsInstance(Thing.Red.book, Thing.Red)
        self.assertEqual('red', Thing.Red.book.color)
        self.assertEqual('pages', Thing.Red.book.has)
