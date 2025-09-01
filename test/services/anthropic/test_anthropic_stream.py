import asyncio
import unittest.mock

import anthropic
import pytest

import services.anthropic


@pytest.mark.asyncio
async def test_anthropic_stream(mocker):
    def stream_side_effect(*args, **kwargs):
        yield "some initial content"
        raise anthropic.APIStatusError(
            message="overloaded",
            body="body",
            response=unittest.mock.MagicMock(status_code=529),
        )

    mock_anthropic_client = unittest.mock.MagicMock(spec=anthropic.Anthropic)

    mock_stream = unittest.mock.MagicMock()
    mock_stream.__enter__.return_value.text_stream = stream_side_effect()
    mock_anthropic_client.messages.stream.return_value = mock_stream

    mocker.patch("anthropic.Anthropic", return_value=mock_anthropic_client)

    message_i = 0
    async for message in services.anthropic.stream(query="hello", tools=[]):
        if message_i == 0:
            assert "data:" in message

        if message_i == 1:
            assert "529" in message
            assert "overloaded" in message

        message_i += 1
