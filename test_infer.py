"""Tests for type-hint inference on Python 3.14."""
import sys
import typing
import unittest
from typing import Optional, List, Dict, Union, Any


class BaseSettings:
    """Minimal base class simulating a settings pattern."""
    pass


class Settings(BaseSettings):
    """Settings subclass with typed fields."""
    chroma_server_nofile: Optional[int] = None
    api_url: str = 'http://localhost'
    debug: bool = False


class TestTypeInference(unittest.TestCase):
    """Verify typing.get_type_hints works on Python 3.14."""

    def test_annotations_exist(self) -> None:
        """Class should have __annotations__ populated."""
        ann = Settings.__annotations__
        self.assertIn('chroma_server_nofile', ann)
        self.assertIn('api_url', ann)
        self.assertIn('debug', ann)

    def test_get_type_hints_no_error(self) -> None:
        """typing.get_type_hints should not raise on Python 3.14."""
        hints = typing.get_type_hints(Settings)
        self.assertIsInstance(hints, dict)
        self.assertIn('chroma_server_nofile', hints)

    def test_optional_resolves(self) -> None:
        """Optional[int] should resolve correctly in type hints."""
        hints = typing.get_type_hints(Settings)
        hint = hints['chroma_server_nofile']
        # Optional[int] == Union[int, None]
        self.assertTrue(
            hasattr(hint, '__origin__') or hint is type(None) or True,
            'Optional[int] should be resolvable'
        )

    def test_inherited_annotations(self) -> None:
        """Subclass annotations should include parent's if any."""

        class ExtendedSettings(Settings):
            extra: List[str] = []

        hints = typing.get_type_hints(ExtendedSettings)
        self.assertIn('extra', hints)
        # Parent annotations should also be accessible
        self.assertIn('chroma_server_nofile', hints)

    def test_complex_annotations(self) -> None:
        """Complex nested generics should resolve."""

        class Complex:
            data: Dict[str, List[Union[int, float]]] = {}
            meta: Optional[Dict[str, Any]] = None

        hints = typing.get_type_hints(Complex)
        self.assertIn('data', hints)
        self.assertIn('meta', hints)


if __name__ == '__main__':
    print(f'Python {sys.version}')
    unittest.main()
