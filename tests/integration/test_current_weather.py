import pytest


@pytest.mark.asyncio
async def test_post_weather_current_by_coordinates(use_test_client):
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
    get_weather_current_response = use_test_client.post("/api/v1/current-weather/coordinates", params=params, headers=headers)
    assert get_weather_current_response.status_code == 201

    response_json = get_weather_current_response.json()

    assert response_json["city"] == "Liberdade"

@pytest.mark.asyncio
async def test_post_weather_current_by_city(use_test_client):
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
    get_weather_current_response = use_test_client.post(f"/api/v1/current-weather/{city}", headers=headers)
    assert get_weather_current_response.status_code == 201

    response_json = get_weather_current_response.json()

    assert response_json["city"] == "Liberdade"

@pytest.mark.asyncio
async def test_get_all_weather_current_by_user(use_test_client):
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

    get_weather_current_response = use_test_client.get(f"/api/v1/current-weather/user/{user_id}")
    assert get_weather_current_response.status_code == 404

    city= "Liberdade"
    get_weather_current_response = use_test_client.post(f"/api/v1/current-weather/{city}", headers=headers)
    assert get_weather_current_response.status_code == 201

    get_weather_current_response = use_test_client.get(f"/api/v1/current-weather/user/{user_id}")
    assert get_weather_current_response.status_code == 200


@pytest.mark.asyncio
async def test_put_weather_current(use_test_client):
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
    get_weather_current_response = use_test_client.post(f"/api/v1/current-weather/{city}", headers=headers)
    assert get_weather_current_response.status_code == 201

    response_json = get_weather_current_response.json()

    assert response_json["city"] == "Liberdade"
    id = response_json["id"]

    json_request = {
        "id": response_json["id"],
        "city": "Curitiba",
        "latitude": -25.504,
        "longitude": -49.2908,
        "current_temperature": 0,
        "feels_like": 0,
        "temp_min": 0,
        "temp_max": 0,
        "pressure": 0,
        "humidity": 0,
        "visibility": 0,
        "wind_speed": 0,
        "wind_deg": 0,
        "wind_gust": 0,
        "cloudiness": 0,
        "weather_description": "string",
        "observation_datetime": "2024-10-07T15:38:39",
        "sunrise": "2024-10-07T15:38:39",
        "sunset": "2024-10-07T15:38:39",
        "user_id": user_id
    }
    put_weather_current_response = use_test_client.put(f"/api/v1/current-weather/{id}", headers=headers, json=json_request)
    assert put_weather_current_response.status_code == 200

    response_json = put_weather_current_response.json()


@pytest.mark.asyncio
async def test_delete_weather_current(use_test_client):
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
    get_weather_current_response = use_test_client.post(f"/api/v1/current-weather/{city}", headers=headers)
    assert get_weather_current_response.status_code == 201

    response_json = get_weather_current_response.json()

    assert response_json["city"] == "Liberdade"
    id = response_json["id"]

    delete_weather_current_response = use_test_client.delete(f"/api/v1/current-weather/{id}", headers=headers)
    assert delete_weather_current_response.status_code == 200

    response_json = delete_weather_current_response.json()



    

