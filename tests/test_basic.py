import pytest
from app.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'URL Shortener API'

def test_shorten_and_redirect(client):
    res = client.post('/api/shorten', json={'url': 'https://example.com'})
    assert res.status_code == 200
    data = res.get_json()
    short_code = data['short_code']
    
    redirect_res = client.get(f'/{short_code}', follow_redirects=False)
    assert redirect_res.status_code == 302
    assert redirect_res.headers['Location'] == 'https://example.com'

def test_stats(client):
    res = client.post('/api/shorten', json={'url': 'https://test.com'})
    data = res.get_json()
    short_code = data['short_code']
    
    # simulate clicks
    for _ in range(3):
        client.get(f'/{short_code}')
    
    stats = client.get(f'/api/stats/{short_code}')
    assert stats.status_code == 200
    data = stats.get_json()
    assert data['clicks'] == 3
    assert data['url'] == 'https://test.com'
    assert 'created_at' in data

def test_invalid_url(client):
    res = client.post('/api/shorten', json={'url': 'not-a-valid-url'})
    assert res.status_code == 400

def test_missing_url(client):
    res = client.post('/api/shorten', json={})
    assert res.status_code == 400

def test_404_redirect(client):
    res = client.get('/nonexistent')
    assert res.status_code == 404
