import pytest
from bs4 import BeautifulSoup


@pytest.mark.parametrize('id, name, http_status', [
    pytest.param(3, 'Jozko Mrkvicka', 200, id='200-correct'),
    pytest.param(30000,  None, 404, id='404-item_not_found'),
    ])
def test_get(client, init_db_with_data, id, name, http_status):
    """Start with a blank database."""

    rv = client.get(f'/actors/{id}')
    assert rv.status_code == http_status
    if http_status == 200:
        soup = BeautifulSoup(rv.data, "html.parser")
        assert soup.find('h2').text == 'Jozko Mrkvicka'
