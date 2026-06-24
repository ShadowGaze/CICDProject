import pytest
from app import app as flask_app
from models.user_model import get_all_users, create_user, delete_user
import psycopg2

# ── Test DB connection ───────────────────────────────────


def get_test_connection():
    return psycopg2.connect(
        dbname='crud_test_db',
        user='postgres',
        password='1234',
        host='localhost',
        port='5432',
    )

# ── Fixtures ─────────────────────────────────────────────


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr('models.user_model.get_connection',
                        get_test_connection)
    flask_app.config['TESTING'] = True
    return flask_app.test_client()


@pytest.fixture(autouse=True)
def clean_db(monkeypatch):
    monkeypatch.setattr('models.user_model.get_connection',
                        get_test_connection)
    # setup table
    conn = get_test_connection()
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id    SERIAL PRIMARY KEY,
                name  VARCHAR(100) NOT NULL,
                dob   DATE NOT NULL,
                email VARCHAR(150) NOT NULL UNIQUE
            );
        """)
        cur.execute("DELETE FROM users;")
    conn.commit()
    conn.close()

# ─────────────────────────────────────────────────────────
# MODEL TESTS
# ─────────────────────────────────────────────────────────


def test_get_all_users_empty():
    result = get_all_users()
    assert result == []


def test_create_user_saves_to_db():
    create_user('Rishabh Singh', '2000-05-15', 'rishabh@test.com')
    users = get_all_users()
    assert len(users) == 1
    assert users[0]['name'] == 'Rishabh Singh'
    assert users[0]['email'] == 'rishabh@test.com'


def test_create_multiple_users():
    create_user('Alice', '1995-01-01', 'alice@test.com')
    create_user('Bob',   '1998-06-20', 'bob@test.com')
    assert len(get_all_users()) == 2


def test_duplicate_email_raises_error():
    create_user('Alice', '1995-01-01', 'same@test.com')
    with pytest.raises(Exception):
        create_user('Bob', '1998-06-20', 'same@test.com')


def test_delete_user_removes_from_db():
    create_user('Rishabh', '2000-05-15', 'rishabh@test.com')
    user_id = get_all_users()[0]['id']
    delete_user(user_id)
    assert get_all_users() == []


def test_delete_removes_only_correct_user():
    create_user('Alice', '1995-01-01', 'alice@test.com')
    create_user('Bob',   '1998-06-20', 'bob@test.com')
    users = get_all_users()
    alice = next(u for u in users if u['name'] == 'Alice')
    delete_user(alice['id'])
    remaining = get_all_users()
    assert len(remaining) == 1
    assert remaining[0]['name'] == 'Bob'


def test_delete_nonexistent_id_does_not_crash():
    delete_user(99999)   # should not raise
    assert get_all_users() == []

# ─────────────────────────────────────────────────────────
# ROUTE TESTS
# ─────────────────────────────────────────────────────────


def test_home_page_loads(client):
    response = client.get('/')
    assert response.status_code == 200


def test_users_page_loads(client):
    response = client.get('/users')
    assert response.status_code == 200


def test_valid_form_submission_redirects(client):
    response = client.post('/', data={
        'name':  'Rishabh Singh',
        'dob':   '2000-05-15',
        'email': 'rishabh@test.com'
    })
    assert response.status_code == 302


def test_empty_fields_does_not_redirect(client):
    response = client.post('/', data={
        'name': '', 'dob': '', 'email': ''
    })
    assert response.status_code == 200   # stays on same page


def test_users_page_shows_added_user(client):
    create_user('Rishabh', '2000-05-15', 'rishabh@test.com')
    response = client.get('/users')
    assert b'Rishabh' in response.data


def test_delete_route_redirects(client):
    create_user('Rishabh', '2000-05-15', 'rishabh@test.com')
    user_id = get_all_users()[0]['id']
    response = client.post(f'/delete/{user_id}')
    assert response.status_code == 302


def test_delete_route_removes_user(client):
    create_user('Rishabh', '2000-05-15', 'rishabh@test.com')
    user_id = get_all_users()[0]['id']
    client.post(f'/delete/{user_id}')
    assert get_all_users() == []
