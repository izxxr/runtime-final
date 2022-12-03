import _tests
import unittest


class TestFinals(unittest.TestCase):
    def test_final_class(self) -> None:
        with self.assertRaises(RuntimeError):
            class __Subclass__(_tests.FinalClass):
                pass

    def test_finals_methods(self) -> None:
        with self.assertRaises(RuntimeError):
            class __SubclassOverrides__(_tests.ClassWithFinals):
                def foo(self) -> None:
                    pass

        with self.assertRaises(RuntimeError):
            class __SubclassOverridesClassMethod__(_tests.ClassWithFinals):
                @classmethod
                def foo_classmethod(cls) -> None:
                    pass

        with self.assertRaises(RuntimeError):
            class __SubclassOverridesStaticMethod__(_tests.ClassWithFinals):
                @staticmethod
                def foo_staticmethod() -> None:
                    pass

        with self.assertRaises(RuntimeError):
            class __SubclassOverridesProperty__(_tests.ClassWithFinals):
                @property
                def foo_property(self) -> None:
                    pass


if __name__ == "__main__":
    unittest.main()
