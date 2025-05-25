import pytest
from unittest.mock import patch, mock_open, Mock, call
from collections import defaultdict
from main import get_animals_count, write_to_csv

@pytest.fixture
def mock_wiki_response():
    html = """
    <div class="mw-category">
        <div class="mw-category-group">
            <h3>А</h3>
            <ul>
                <li><a href="/wiki/Аист">Аист</a></li>
                <li><a href="/wiki/Акула">Акула</a></li>
            </ul>
        </div>
        <div class="mw-category-group">
            <h3>Б</h3>
            <ul>
                <li><a href="/wiki/Барсук">Барсук</a></li>
            </ul>
        </div>
    </div>
    """
    mock_resp = Mock()
    mock_resp.text = html
    mock_resp.raise_for_status = Mock()
    return mock_resp


def test_get_animals_count(mock_wiki_response):
    with patch('main.requests.get', return_value=mock_wiki_response) as mock_get:
        result = get_animals_count()

        assert isinstance(result, defaultdict)
        assert result['А'] == 2
        assert result['Б'] == 1
        mock_get.assert_called_once()


def test_write_to_csv():
    test_data = {'А': 2, 'Б': 1}

    m = mock_open()
    with patch('main.open', m):
        with patch('main.csv.writer') as mock_writer:
            mock_writer.return_value.writerow.side_effect = None
            write_to_csv(test_data)

            expected_calls = [call(['А', 2]), call(['Б', 1])]
            mock_writer.return_value.writerow.assert_has_calls(expected_calls)


@pytest.mark.integration
def test_integration_flow(mock_wiki_response):
    with patch('main.requests.get', return_value=mock_wiki_response):
        m = mock_open()
        with patch('main.open', m):
            with patch('main.csv.writer') as mock_writer:
                counts = get_animals_count()
                write_to_csv(counts)

                assert counts['А'] == 2
                mock_writer.return_value.writerow.assert_called()