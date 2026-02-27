"""Tests for llm_client.py — all external calls mocked."""
import unittest
from unittest.mock import patch, MagicMock


class TestCheckServerHealth(unittest.TestCase):
    """Tests for check_server_health function."""

    @patch('llm_client.requests.get')
    def test_online_returns_models(self, mock_get: MagicMock) -> None:
        """Should return online status with model list on 200."""
        mock_get.return_value = MagicMock(
            status_code=200,
            json=lambda: {'data': [{'id': 'model-a'}, {'id': 'model-b'}]},
        )
        from llm_client import check_server_health
        result = check_server_health()
        self.assertEqual(result['status'], 'online')
        self.assertIn('model-a', result['models'])
        self.assertIn('model-b', result['models'])

    @patch('llm_client.requests.get')
    def test_error_status_on_non_200(self, mock_get: MagicMock) -> None:
        """Should return error status on non-200 response."""
        mock_get.return_value = MagicMock(status_code=500)
        from llm_client import check_server_health
        result = check_server_health()
        self.assertEqual(result['status'], 'error')

    @patch('llm_client.requests.get', side_effect=ConnectionError('refused'))
    def test_offline_on_exception(self, mock_get: MagicMock) -> None:
        """Should return offline status when server is unreachable."""
        from llm_client import check_server_health
        result = check_server_health()
        self.assertEqual(result['status'], 'offline')
        self.assertIn('error', result)


class TestGetEmbedding(unittest.TestCase):
    """Tests for get_embedding function."""

    @patch('llm_client.client')
    def test_returns_embedding_list(self, mock_client: MagicMock) -> None:
        """Should return the embedding vector from the API response."""
        fake_vec = [0.1] * 384
        mock_resp = MagicMock()
        mock_resp.data = [MagicMock(embedding=fake_vec)]
        mock_client.embeddings.create.return_value = mock_resp

        from llm_client import get_embedding
        result = get_embedding('test text')
        self.assertEqual(result, fake_vec)
        mock_client.embeddings.create.assert_called_once()

    @patch('llm_client.client')
    def test_truncates_long_input(self, mock_client: MagicMock) -> None:
        """Should truncate input text to 2000 chars."""
        mock_resp = MagicMock()
        mock_resp.data = [MagicMock(embedding=[0.0])]
        mock_client.embeddings.create.return_value = mock_resp

        from llm_client import get_embedding
        long_text = 'x' * 5000
        get_embedding(long_text)

        call_args = mock_client.embeddings.create.call_args
        self.assertTrue(len(call_args.kwargs.get('input', call_args[1].get('input', ''))) <= 2000)


class TestGenerateCode(unittest.TestCase):
    """Tests for generate_code function."""

    @patch('llm_client.client')
    def test_returns_stripped_content(self, mock_client: MagicMock) -> None:
        """Should return stripped message content."""
        mock_msg = MagicMock()
        mock_msg.content = '  print("hello")  \n'
        mock_choice = MagicMock()
        mock_choice.message = mock_msg
        mock_resp = MagicMock()
        mock_resp.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_resp

        from llm_client import generate_code
        code = generate_code('system prompt', 'user prompt')
        self.assertEqual(code, 'print("hello")')


class TestGenerateExplanation(unittest.TestCase):
    """Tests for generate_explanation function."""

    @patch('llm_client.client')
    def test_returns_explanation(self, mock_client: MagicMock) -> None:
        """Should return stripped explanation content."""
        mock_msg = MagicMock()
        mock_msg.content = '  The data shows a trend.  '
        mock_choice = MagicMock()
        mock_choice.message = mock_msg
        mock_resp = MagicMock()
        mock_resp.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_resp

        from llm_client import generate_explanation
        result = generate_explanation('system', 'user')
        self.assertEqual(result, 'The data shows a trend.')


if __name__ == '__main__':
    unittest.main()
