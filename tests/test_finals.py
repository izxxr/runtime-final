from runtime_final import final
import unittest


@final
class FinalClass:
    pass


class ClassWithFinals:
    @final
    def foo(self) -> None:
        pass

    @final
    def bar(self) -> None:
        pass

    def foo_nofinal(self) -> None:
        pass

    def bar_nofinal(self) -> None:
        pass


class TestFinals(unittest.TestCase):
    def test_finals(self) -> None:
        with self.assertRaises(RuntimeError):
            
            class Subclass(ClassWithFinals):
                def foo(self) -> None:
                    pass

                def bar(self) -> None:
                    pass
        
        with self.assertRaises(RuntimeError):
            
            class Subclass(FinalClass):
                pass


if __name__ == "__main__":
    unittest.main()
