from runtime_final import get_final_methods, is_final
import _tests
import unittest


class TestHelpers(unittest.TestCase):
    def test_get_final_methods(self) -> None:
        assert len(get_final_methods(_tests.ClassWithFinals)) == 5

    def test_is_final(self) -> None:
        assert is_final(_tests.FinalClass)
        assert is_final(_tests.ClassWithFinals.foo)
        assert is_final(_tests.ClassWithFinals.bar)
        assert not is_final(_tests.ClassWithFinals.foo_nofinal)
        assert not is_final(_tests.ClassWithFinals.bar_nofinal)


if __name__ == "__main__":
    unittest.main()
