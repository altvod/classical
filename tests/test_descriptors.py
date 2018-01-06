from unittest import TestCase

from classical.descriptors import (
    ArgumentedSubclass, AttributedSubclass,
    AutoProperty, DummySubclass
)


class TestDescriptors(TestCase):
    def test_argumented_subclass(self):
        class Tree:
            Peach = ArgumentedSubclass(fruit='peach')
            Pine = ArgumentedSubclass(fruit='cone')

            def __init__(self, fruit):
                self.fruit = fruit

        self.assertTrue(issubclass(Tree.Peach, Tree))
        self.assertEqual('Peach', Tree.Peach.__name__)
        self.assertIsInstance(Tree.Peach(), Tree)
        self.assertEqual('peach', Tree.Peach().fruit)
        self.assertEqual('cone', Tree.Pine().fruit)
        self.assertIs(
            Tree.Peach, Tree.Peach,
            msg='Subsequent calls return different subclasses'
        )

    def test_argumented_subclass_recursion(self):
        class Polygon:
            Blue = ArgumentedSubclass(color='blue')
            Pentagon = ArgumentedSubclass(sides=5)

            def __init__(self, color=None, sides=3):
                self.color = color
                self.sides = sides

        blue_pentagon = Polygon.Pentagon.Blue()
        self.assertEqual(5, blue_pentagon.sides)
        self.assertEqual('blue', blue_pentagon.color)

    def test_attributed_subclass(self):
        class Tree:
            fruit = None

            Peach = AttributedSubclass(fruit='peach')
            Pine = AttributedSubclass(fruit='cone')

        self.assertTrue(issubclass(Tree.Peach, Tree))
        self.assertEqual('Peach', Tree.Peach.__name__)
        self.assertIsInstance(Tree.Peach(), Tree)
        self.assertEqual('peach', Tree.Peach().fruit)
        self.assertEqual('cone', Tree.Pine().fruit)
        self.assertIs(
            Tree.Peach, Tree.Peach,
            msg='Subsequent calls return different subclasses'
        )

    def test_attributed_subclass_recursion(self):
        class Polygon:
            color = None
            sides = None

            Blue = AttributedSubclass(color='blue')
            Pentagon = AttributedSubclass(sides=5)

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
        self.assertIs(
            Thing.book, Thing.book,
            msg='Subsequent calls return different instances'
        )
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
            size = None

            Blue = ArgumentedSubclass(color='blue')
            Red = ArgumentedSubclass(color='red')

            Small = AttributedSubclass(size='small')
            Large = AttributedSubclass(size='large')

            book = AutoProperty(has='pages')
            lamp = AutoProperty(has='light')

            def __init__(self, color=None, has=None):
                self.color = color
                self.has = has

        self.assertIsInstance(Thing.Red.book, Thing.Red)
        self.assertIsInstance(Thing.Large.book, Thing.Large)
        self.assertIsInstance(Thing.Small.Red.book, Thing.Small)
        self.assertIsInstance(Thing.Small.Red.book, Thing.Small.Red)
        self.assertTrue(Thing.Large.book, Thing.Large)
        self.assertEqual('red', Thing.Small.Red.book.color)
        self.assertEqual('pages', Thing.Small.Red.book.has)
        self.assertEqual('small', Thing.Small.Red.book.size)

    def test_terminal_property(self):
        class Thing:
            my_subclass = DummySubclass()
            my_terminal_subclass = DummySubclass().terminal

            my_instance = AutoProperty()
            my_terminal_instance = AutoProperty().terminal

        class ClassyThing(Thing):
            pass

        self.assertTrue(issubclass(ClassyThing.my_subclass, ClassyThing))
        self.assertFalse(issubclass(ClassyThing.my_terminal_subclass, ClassyThing))

        self.assertIsInstance(ClassyThing.my_instance, ClassyThing)
        self.assertIs(ClassyThing.my_instance.__class__, ClassyThing)
        self.assertNotIsInstance(ClassyThing.my_terminal_instance, ClassyThing)
        self.assertIs(ClassyThing.my_terminal_instance.__class__, Thing)
