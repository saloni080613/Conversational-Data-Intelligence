"""Tests for Pydantic v2 model validation on Python 3.14."""
import unittest
from typing import Optional, List

from pydantic import BaseModel, ValidationError


class ServerSettings(BaseModel):
    """Test model simulating chromadb-style settings."""
    chroma_server_nofile: Optional[int] = None
    host: str = 'localhost'
    port: int = 8000
    debug: bool = False
    allowed_origins: List[str] = []


class TestPydanticV2Models(unittest.TestCase):
    """Verify Pydantic v2 models work correctly on Python 3.14."""

    def test_default_instantiation(self) -> None:
        """Model should instantiate with all defaults."""
        s = ServerSettings()
        self.assertIsNone(s.chroma_server_nofile)
        self.assertEqual(s.host, 'localhost')
        self.assertEqual(s.port, 8000)
        self.assertFalse(s.debug)
        self.assertEqual(s.allowed_origins, [])

    def test_custom_values(self) -> None:
        """Model should accept valid custom values."""
        s = ServerSettings(
            chroma_server_nofile=1024,
            host='0.0.0.0',
            port=9090,
            debug=True,
            allowed_origins=['http://localhost:3000'],
        )
        self.assertEqual(s.chroma_server_nofile, 1024)
        self.assertEqual(s.host, '0.0.0.0')
        self.assertEqual(s.port, 9090)
        self.assertTrue(s.debug)

    def test_optional_none(self) -> None:
        """Optional field should accept explicit None."""
        s = ServerSettings(chroma_server_nofile=None)
        self.assertIsNone(s.chroma_server_nofile)

    def test_serialization_dict(self) -> None:
        """Model should serialize to dict via model_dump."""
        s = ServerSettings(port=5000)
        d = s.model_dump()
        self.assertIsInstance(d, dict)
        self.assertEqual(d['port'], 5000)

    def test_serialization_json(self) -> None:
        """Model should serialize to JSON string."""
        s = ServerSettings()
        j = s.model_json_schema()
        self.assertIn('properties', j)
        self.assertIn('port', j['properties'])

    def test_validation_error_on_bad_type(self) -> None:
        """Model should raise ValidationError for wrong types."""
        with self.assertRaises(ValidationError):
            ServerSettings(port='not_a_number')  # type: ignore

    def test_model_fields_metadata(self) -> None:
        """model_fields should expose field metadata."""
        fields = ServerSettings.model_fields
        self.assertIn('chroma_server_nofile', fields)
        self.assertIn('host', fields)


if __name__ == '__main__':
    unittest.main()
