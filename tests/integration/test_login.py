import server


def test_unknown_email_returns_to_login_with_error_message():
    client = server.app.test_client()

    response = client.post(
        '/showSummary',
        data={'email': 'unknown@example.com'}
    )

    assert response.status_code == 302
    assert response.location == '/'


def test_valid_email_displays_welcome_page():
    client = server.app.test_client()

    response = client.post(
        '/showSummary',
        data={'email': 'john@simplylift.co'}
    )

    assert response.status_code == 200


def test_index_page_is_accessible():
    client = server.app.test_client()

    response = client.get('/')

    assert response.status_code == 200
    assert b'GUDLFT Registration' in response.data


def test_logout_redirects_to_index():
    client = server.app.test_client()

    response = client.get('/logout')

    assert response.status_code == 302
    assert response.location == '/'