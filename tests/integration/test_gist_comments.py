import pytest


@pytest.mark.asyncio
async def test_post_gist_comment_by_coordinates(use_test_client):
    signup_payload = {
        "username": "devMaster",
        "password": "jujuba",
        "email": "master@dev.com",
        "name": "dev",
    }
    signup_response = use_test_client.post("/api/v1/auth/signup", json=signup_payload)
    assert signup_response.status_code == 201

    login_payload = {"username": "master@dev.com", "password": "jujuba"}
    login_response = use_test_client.post("/api/v1/auth/login", data=login_payload)
    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"latitude": -23.5505, "longitude": -46.6333}
    get_gist_comment_response = use_test_client.post("/api/v1/gist-comments/coordinates", params=params, headers=headers)
    assert get_gist_comment_response.status_code == 201


@pytest.mark.asyncio
async def test_post_gist_comment_by_city(use_test_client):
    signup_payload = {
        "username": "devMaster",
        "password": "jujuba",
        "email": "master@dev.com",
        "name": "dev",
    }
    signup_response = use_test_client.post("/api/v1/auth/signup", json=signup_payload)
    assert signup_response.status_code == 201

    login_payload = {"username": "master@dev.com", "password": "jujuba"}
    login_response = use_test_client.post("/api/v1/auth/login", data=login_payload)
    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    city= "Liberdade"
    get_gist_comment_response = use_test_client.post(f"/api/v1/gist-comments/{city}", headers=headers)
    assert get_gist_comment_response.status_code == 201


@pytest.mark.asyncio
async def test_get_all_gist_comment_by_user(use_test_client):
    signup_payload = {
        "username": "devMaster",
        "password": "jujuba",
        "email": "master@dev.com",
        "name": "dev",
    }
    signup_response = use_test_client.post("/api/v1/auth/signup", json=signup_payload)
    assert signup_response.status_code == 201

    login_payload = {"username": "master@dev.com", "password": "jujuba"}
    login_response = use_test_client.post("/api/v1/auth/login", data=login_payload)
    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    get_me_response = use_test_client.get("/api/v1/users/me", headers=headers)
    assert get_me_response.status_code == 200

    response_json = get_me_response.json()
    user_id = response_json["id"]

    get_gist_comment_response = use_test_client.get(f"/api/v1/gist-comments/user/{user_id}")
    assert get_gist_comment_response.status_code == 404

    city= "Liberdade"
    get_gist_comment_response = use_test_client.post(f"/api/v1/gist-comments/{city}", headers=headers)
    assert get_gist_comment_response.status_code == 201

    get_gist_comment_response = use_test_client.get(f"/api/v1/gist-comments/user/{user_id}")
    assert get_gist_comment_response.status_code == 200


@pytest.mark.asyncio
async def test_put_gist_comment(use_test_client):
    signup_payload = {
        "username": "devMaster",
        "password": "jujuba",
        "email": "master@dev.com",
        "name": "dev",
    }
    signup_response = use_test_client.post("/api/v1/auth/signup", json=signup_payload)
    assert signup_response.status_code == 201

    login_payload = {"username": "master@dev.com", "password": "jujuba"}
    login_response = use_test_client.post("/api/v1/auth/login", data=login_payload)
    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    get_me_response = use_test_client.get("/api/v1/users/me", headers=headers)
    assert get_me_response.status_code == 200
    response_json = get_me_response.json()

    user_id = response_json["id"]
    city= "Liberdade"
    get_gist_comment_response = use_test_client.post(f"/api/v1/gist-comments/{city}", headers=headers)
    assert get_gist_comment_response.status_code == 201

    response_json = get_gist_comment_response.json()

    comment_id = response_json["comment_id"]

    json_request = {
        "city": "string",
        "latitude": 0,
        "longitude": 0,
        "current_temperature": 0,
        "weather_description": "string",
        "forecast_day_1_date": "string",
        "forecast_day_1_temperature": 0,
        "forecast_day_2_date": "string",
        "forecast_day_2_temperature": 0,
        "forecast_day_3_date": "string",
        "forecast_day_3_temperature": 0,
        "forecast_day_4_date": "string",
        "forecast_day_4_temperature": 0,
        "forecast_day_5_date": "string",
        "forecast_day_5_temperature": 0
    }
    put_gist_comment_response = use_test_client.put(f"/api/v1/gist-comments/{comment_id}", headers=headers, json=json_request)
    assert put_gist_comment_response.status_code == 200

    response_json = put_gist_comment_response.json()


@pytest.mark.asyncio
async def test_delete_gist_comment(use_test_client):
    signup_payload = {
        "username": "devMaster",
        "password": "jujuba",
        "email": "master@dev.com",
        "name": "dev",
    }
    signup_response = use_test_client.post("/api/v1/auth/signup", json=signup_payload)
    assert signup_response.status_code == 201

    login_payload = {"username": "master@dev.com", "password": "jujuba"}
    login_response = use_test_client.post("/api/v1/auth/login", data=login_payload)
    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    headers = {"Authorization": f"Bearer {access_token}"}
    city= "Liberdade"
    get_gist_comment_response = use_test_client.post(f"/api/v1/gist-comments/{city}", headers=headers)
    assert get_gist_comment_response.status_code == 201

    response_json = get_gist_comment_response.json()

    comment_id = response_json["comment_id"]

    delete_gist_comment_response = use_test_client.delete(f"/api/v1/gist-comments/{comment_id}", headers=headers)
    assert delete_gist_comment_response.status_code == 200

    response_json = delete_gist_comment_response.json()



    

