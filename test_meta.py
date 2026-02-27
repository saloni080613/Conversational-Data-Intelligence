"""Tests for Python 3.14 metaclass annotation extraction."""
import sys
import unittest
from typing import Optional, List


class AnnotationCaptureMeta(type):
    """Metaclass that captures annotations from the class body."""
    captured_annotations: dict = {}

    def __new__(mcs, name: str, bases: tuple, namespace: dict) -> type:
        ann: dict = {}

        # Python 3.14+ uses __annotate_func__ (PEP 749)
        if '__annotate_func__' in namespace:
            try:
                ann = namespace['__annotate_func__'](1)
            except Exception:
                pass

        # Fallback: __annotations__ (Python <= 3.13)
        if not ann:
            ann = namespace.get('__annotations__', {})

        mcs.captured_annotations = ann
        return super().__new__(mcs, name, bases, namespace)


class TestMetaclassAnnotations(unittest.TestCase):
    """Verify custom metaclasses can extract type annotations on Python 3.14."""

    def test_simple_annotation_extraction(self) -> None:
        """Metaclass should capture basic int annotation."""

        class Sample(metaclass=AnnotationCaptureMeta):
            x: int = 1

        self.assertIn('x', AnnotationCaptureMeta.captured_annotations)
        self.assertEqual(AnnotationCaptureMeta.captured_annotations['x'], int)

    def test_optional_annotation_extraction(self) -> None:
        """Metaclass should capture Optional[str] annotation."""

        class Sample2(metaclass=AnnotationCaptureMeta):
            name: Optional[str] = None

        self.assertIn('name', AnnotationCaptureMeta.captured_annotations)

    def test_multiple_annotations(self) -> None:
        """Metaclass should capture all annotations from a class."""

        class Sample3(metaclass=AnnotationCaptureMeta):
            a: int = 0
            b: str = ''
            c: List[float] = []

        ann = AnnotationCaptureMeta.captured_annotations
        self.assertEqual(len(ann), 3)
        self.assertIn('a', ann)
        self.assertIn('b', ann)
        self.assertIn('c', ann)

    def test_no_annotations(self) -> None:
        """Metaclass should handle class with no annotations."""

        class EmptyClass(metaclass=AnnotationCaptureMeta):
            pass

        self.assertEqual(AnnotationCaptureMeta.captured_annotations, {})


if __name__ == '__main__':
    print(f'Python {sys.version}')
    unittest.main()
