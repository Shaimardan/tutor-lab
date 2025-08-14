import json


async def test_create_user(client):
    user_data = {
        "username": "Luke",
        "fullname": "Skiwoker",
        "email": "Skiwoker@kek.com",
        "disabled": False,
        "password": "66",
    }
    resp = client.post(
        "/api/users/",
        data=json.dumps(user_data),
    )
    user_id_resp = resp.json()
    assert resp.status_code == 200
    assert type(user_id_resp) is int


async def test_create_similar_user(client):
    user_data = {
        "username": "Luke_similar_test",
        "fullname": "Skiwoker",
        "email": "Skiwoker@kek.com",
        "disabled": False,
        "password": "66",
    }
    resp = client.post(
        "/api/users/",
        data=json.dumps(user_data),
    )
    assert resp.status_code == 200

    resp = client.post(
        "/api/users/",
        data=json.dumps(user_data),
    )
    assert resp.status_code == 409


async def test_delete_user(client):
    user_data = {
        "username": "user_for_delete",
        "fullname": "Opel",
        "email": "Opel@kek.com",
        "disabled": False,
        "password": "123",
    }
    resp = client.post(
        "/api/users/",
        data=json.dumps(user_data),
    )
    assert resp.status_code == 200

    resp_delete = client.delete(
        "/api/users/?user_id={}".format(resp.json()),
    )
    assert resp.status_code == 200
    assert resp_delete.json() == resp.json()


async def test_update_user(client):
    user_data = {
        "username": "Luke_update_user",
        "fullname": "Skiwoker",
        "email": "Skiwoker@kek.com",
        "disabled": False,
        "password": "66",
    }
    res = client.post(
        "/api/users/",
        data=json.dumps(user_data),
    )

    update_data = {
        "username": "NewUsername",
        "email": "newemail@example.com",
        "fullname": "New Full Name",
    }

    resp = client.patch(
        "/api/users/?user_id={}".format(res.json()),
        json=update_data,
    )
    data_from_resp = resp.json()
    assert resp.status_code == 200
    assert data_from_resp["updated_user_id"] == res.json()


async def test_change_password(client):
    user_data = {
        "password": "1111",
    }

    resp = client.patch(
        f"/api/users/password/{1}",
        json=user_data,
    )
    assert resp.status_code == 200

    login_data = {"username": "johndoe", "password": "1111"}
    resp = client.post(
        "/api/auth/token",
        data=login_data,
    )
    assert resp.status_code == 200

    user_data = {
        "password": "123",
    }
    resp = client.patch(
        f"/api/users/password/{1}",
        json=user_data,
    )
    assert resp.status_code == 200

    login_data = {"username": "johndoe", "password": "123"}
    resp = client.post(
        "/api/auth/token",
        data=login_data,
    )
    assert resp.status_code == 200


async def test_change_password_incorrect_id(client):
    user_data = {
        "password": "1111",
    }

    resp = client.patch(
        f"/api/users/password/{-1}",
        json=user_data,
    )
    assert resp.status_code == 404
