from runtime_final import final, get_final_methods, is_final
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


class TestHelpers(unittest.TestCase):
    def test_get_final_methods(self) -> None:
        assert len(get_final_methods(ClassWithFinals)) == 2
    
    def test_is_final(self) -> None:
        assert is_final(FinalClass)
        assert is_final(ClassWithFinals.foo)
        assert is_final(ClassWithFinals.bar)


if __name__ == "__main__":
    unittest.main()
