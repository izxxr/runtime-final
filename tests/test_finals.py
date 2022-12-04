from __future__ import annotations
import unittest
from runtime_final import final


@final
class FinalClass:
    pass


class NonFinalClass:
    @final
    def __init__(self, a):
        self.a = a

    @final
    def final_method(self, a):
        return a

    @final
    @property
    def final_property(self):
        return 5

    @final
    @classmethod
    def final_classmethod(cls, a):
        return a

    @final
    @staticmethod
    def final_staticmethod(a):
        return a

    def non_final_method(self, a):
        return a

    @property
    def non_final_property(self):
        return 5

    @classmethod
    def non_final_classmethod(cls, a):
        return a

    @staticmethod
    def non_final_staticmethod(a):
        return a


class TestFinals(unittest.TestCase):
    def test_final_function(self):
        @final
        def func():
            pass

        with self.assertRaises(RuntimeError):
            func()

    def test_final_subclass(self):
        """Test subclassing a final class"""
        with self.assertRaises(RuntimeError):
            class Subclass(FinalClass):
                pass

    def test_base_class(self):
        """Test the base class works correctly"""
        # Final methods
        cls = NonFinalClass(5)
        self.assertEqual(5, cls.a)
        self.assertEqual(5, cls.final_method(5))
        self.assertEqual(5, cls.final_property)
        self.assertEqual(5, cls.final_classmethod(5))
        self.assertEqual(5, NonFinalClass.final_classmethod(5))
        self.assertEqual(5, cls.final_staticmethod(5))
        self.assertEqual(5, NonFinalClass.final_staticmethod(5))
        # Non-final methods
        self.assertEqual(5, cls.non_final_method(5))
        self.assertEqual(5, cls.non_final_property)
        self.assertEqual(5, cls.non_final_classmethod(5))
        self.assertEqual(5, NonFinalClass.non_final_classmethod(5))
        self.assertEqual(5, cls.non_final_staticmethod(5))
        self.assertEqual(5, NonFinalClass.non_final_staticmethod(5))

    def test_non_final_subclass(self):
        class Subclass(NonFinalClass):
            pass

        # Final methods
        cls = Subclass(5)
        self.assertEqual(5, cls.a)
        self.assertEqual(5, cls.final_method(5))
        self.assertEqual(5, cls.final_property)
        self.assertEqual(5, cls.final_classmethod(5))
        self.assertEqual(5, Subclass.final_classmethod(5))
        self.assertEqual(5, cls.final_staticmethod(5))
        self.assertEqual(5, Subclass.final_staticmethod(5))
        # Non-final methods
        self.assertEqual(5, cls.non_final_method(5))
        self.assertEqual(5, cls.non_final_property)
        self.assertEqual(5, cls.non_final_classmethod(5))
        self.assertEqual(5, Subclass.non_final_classmethod(5))
        self.assertEqual(5, cls.non_final_staticmethod(5))
        self.assertEqual(5, Subclass.non_final_staticmethod(5))

    def test_final_methods(self):
        # Without final decorator
        with self.subTest("Subclass constructor"), self.assertRaises(RuntimeError):
            class Subclass(NonFinalClass):
                def __init__(self, a):
                    self.a = a

        with self.subTest("Subclass method"), self.assertRaises(RuntimeError):
            class Subclass(NonFinalClass):
                def final_method(self, a):
                    return a

        with self.subTest("Subclass property"), self.assertRaises(RuntimeError):
            class Subclass(NonFinalClass):
                @property
                def final_property(self):
                    return 5

        with self.subTest("Subclass classmethod"), self.assertRaises(RuntimeError):
            class Subclass(NonFinalClass):
                @classmethod
                def final_classmethod(cls, a):
                    return a

        with self.subTest("Subclass staticmethod"), self.assertRaises(RuntimeError):
            class Subclass(NonFinalClass):
                @staticmethod
                def final_staticmethod(a):
                    return a

        # With final decorator
        with self.subTest("Subclass constructor"), self.assertRaises(RuntimeError):
            class Subclass(NonFinalClass):
                @final
                def __init__(self, a):
                    self.a = a

        with self.subTest("Subclass method"), self.assertRaises(RuntimeError):
            class Subclass(NonFinalClass):
                @final
                def final_method(self, a):
                    return a

        with self.subTest("Subclass property"), self.assertRaises(RuntimeError):
            class Subclass(NonFinalClass):
                @final
                @property
                def final_property(self):
                    return 5

        with self.subTest("Subclass classmethod"), self.assertRaises(RuntimeError):
            class Subclass(NonFinalClass):
                @final
                @classmethod
                def final_classmethod(cls, a):
                    return a

        with self.subTest("Subclass staticmethod"), self.assertRaises(RuntimeError):
            class Subclass(NonFinalClass):
                @final
                @staticmethod
                def final_staticmethod(a):
                    return a

    def test_non_final_methods(self):
        # Without final decorator
        with self.subTest("Subclass non-final"):
            class SubclassNonFinal1(NonFinalClass):
                def non_final_method(self, a):
                    return a + 1

                @property
                def non_final_property(self):
                    return 6

                @classmethod
                def non_final_classmethod(cls, a):
                    return a + 1

                @staticmethod
                def non_final_staticmethod(a):
                    return a + 1

            cls = SubclassNonFinal1(6)
            self.assertEqual(6, cls.non_final_method(5))
            self.assertEqual(6, cls.non_final_property)
            self.assertEqual(6, cls.non_final_classmethod(5))
            self.assertEqual(6, SubclassNonFinal1.non_final_classmethod(5))
            self.assertEqual(6, cls.non_final_staticmethod(5))
            self.assertEqual(6, SubclassNonFinal1.non_final_staticmethod(5))

            class SubclassNonFinal2(SubclassNonFinal1):
                def non_final_method(self, a):
                    return a + 2

                @property
                def non_final_property(self):
                    return 7

                @classmethod
                def non_final_classmethod(cls, a):
                    return a + 2

                @staticmethod
                def non_final_staticmethod(a):
                    return a + 2

            cls = SubclassNonFinal2(7)
            self.assertEqual(7, cls.non_final_method(5))
            self.assertEqual(7, cls.non_final_property)
            self.assertEqual(7, cls.non_final_classmethod(5))
            self.assertEqual(7, SubclassNonFinal2.non_final_classmethod(5))
            self.assertEqual(7, cls.non_final_staticmethod(5))
            self.assertEqual(7, SubclassNonFinal2.non_final_staticmethod(5))

            class SubclassNonFinal3(SubclassNonFinal2):
                def non_final_method(self, a):
                    return super().non_final_method(a) + 1

                @property
                def non_final_property(self):
                    return super().non_final_property + 1

            cls = SubclassNonFinal3(8)
            self.assertEqual(8, cls.non_final_method(5))
            self.assertEqual(8, cls.non_final_property)

        # With final decorator
        with self.subTest("Subclass method"):
            class SubclassFinal(NonFinalClass):
                @final
                def non_final_method(self, a):
                    return a + 1

                @final
                @property
                def non_final_property(self):
                    return 6

                @final
                @classmethod
                def non_final_classmethod(cls, a):
                    return a + 1

                @final
                @staticmethod
                def non_final_staticmethod(a):
                    return a + 1

            cls = SubclassFinal(6)
            self.assertEqual(6, cls.non_final_method(5))
            self.assertEqual(6, cls.non_final_property)
            self.assertEqual(6, cls.non_final_classmethod(5))
            self.assertEqual(6, SubclassFinal.non_final_classmethod(5))
            self.assertEqual(6, cls.non_final_staticmethod(5))
            self.assertEqual(6, SubclassFinal.non_final_staticmethod(5))

            # Without final decorator
            with self.subTest("Subclass method"), self.assertRaises(RuntimeError):
                class SubclassFinal2(SubclassFinal):
                    def non_final_method(self, a):
                        return a

            with self.subTest("Subclass property"), self.assertRaises(RuntimeError):
                class SubclassFinal2(SubclassFinal):
                    @property
                    def non_final_property(self):
                        return 5

            with self.subTest("Subclass classmethod"), self.assertRaises(RuntimeError):
                class SubclassFinal2(SubclassFinal):
                    @classmethod
                    def non_final_classmethod(cls, a):
                        return a

            with self.subTest("Subclass staticmethod"), self.assertRaises(RuntimeError):
                class SubclassFinal2(SubclassFinal):
                    @staticmethod
                    def non_final_staticmethod(a):
                        return a

            # With final decorator
            with self.subTest("Subclass method"), self.assertRaises(RuntimeError):
                class SubclassFinal2(SubclassFinal):
                    @final
                    def non_final_method(self, a):
                        return a

            with self.subTest("Subclass property"), self.assertRaises(RuntimeError):
                class SubclassFinal2(SubclassFinal):
                    @final
                    @property
                    def non_final_property(self):
                        return 5

            with self.subTest("Subclass classmethod"), self.assertRaises(RuntimeError):
                class SubclassFinal2(SubclassFinal):
                    @final
                    @classmethod
                    def non_final_classmethod(cls, a):
                        return a

            with self.subTest("Subclass staticmethod"), self.assertRaises(RuntimeError):
                class SubclassFinal2(SubclassFinal):
                    @final
                    @staticmethod
                    def non_final_staticmethod(a):
                        return a


if __name__ == "__main__":
    unittest.main()
