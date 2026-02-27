"""Sanity-check tests for config.py constants."""
import unittest


class TestConfigConstants(unittest.TestCase):
    """Verify all expected config constants exist and are well-formed."""

    def test_lm_studio_url_is_valid(self) -> None:
        """URL should start with http:// or https://."""
        from config import LM_STUDIO_URL
        self.assertTrue(
            LM_STUDIO_URL.startswith('http://') or LM_STUDIO_URL.startswith('https://'),
            f'Invalid URL: {LM_STUDIO_URL}',
        )

    def test_model_names_are_strings(self) -> None:
        """Model names should be non-empty strings."""
        from config import REASONING_MODEL, EMBEDDING_MODEL
        self.assertIsInstance(REASONING_MODEL, str)
        self.assertIsInstance(EMBEDDING_MODEL, str)
        self.assertTrue(len(REASONING_MODEL) > 0)
        self.assertTrue(len(EMBEDDING_MODEL) > 0)

    def test_chroma_dir_is_string(self) -> None:
        """CHROMA_DIR should be a non-empty string."""
        from config import CHROMA_DIR
        self.assertIsInstance(CHROMA_DIR, str)
        self.assertTrue(len(CHROMA_DIR) > 0)

    def test_max_tokens_positive(self) -> None:
        """MAX_TOKENS should be a positive integer."""
        from config import MAX_TOKENS
        self.assertIsInstance(MAX_TOKENS, int)
        self.assertGreater(MAX_TOKENS, 0)

    def test_temperatures_in_range(self) -> None:
        """Temperature values should be between 0 and 2."""
        from config import TEMP_CODE, TEMP_EXPLAIN
        for t in (TEMP_CODE, TEMP_EXPLAIN):
            self.assertGreaterEqual(t, 0.0)
            self.assertLessEqual(t, 2.0)

    def test_auto_questions_non_empty(self) -> None:
        """AUTO_QUESTIONS should be a non-empty list of strings."""
        from config import AUTO_QUESTIONS
        self.assertIsInstance(AUTO_QUESTIONS, list)
        self.assertGreater(len(AUTO_QUESTIONS), 0)
        for q in AUTO_QUESTIONS:
            self.assertIsInstance(q, str)
            self.assertTrue(len(q) > 0)


if __name__ == '__main__':
    unittest.main()
