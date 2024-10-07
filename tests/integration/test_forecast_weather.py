import pytest


@pytest.mark.asyncio
async def test_post_weather_forecast_by_coordinates(use_test_client):
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
    get_weather_forecast_response = use_test_client.post("/api/v1/forecast-weather/coordinates", params=params, headers=headers)
    assert get_weather_forecast_response.status_code == 201

    response_json = get_weather_forecast_response.json()


@pytest.mark.asyncio
async def test_post_weather_forecast_by_city(use_test_client):
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
    get_weather_forecast_response = use_test_client.post(f"/api/v1/forecast-weather/{city}", headers=headers)
    assert get_weather_forecast_response.status_code == 201

    response_json = get_weather_forecast_response.json()


@pytest.mark.asyncio
async def test_get_all_weather_forecast_by_user(use_test_client):
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

    get_weather_forecast_response = use_test_client.get(f"/api/v1/forecast-weather/user/{user_id}")
    assert get_weather_forecast_response.status_code == 404

    city= "Liberdade"
    get_weather_forecast_response = use_test_client.post(f"/api/v1/forecast-weather/{city}", headers=headers)
    assert get_weather_forecast_response.status_code == 201

    get_weather_forecast_response = use_test_client.get(f"/api/v1/forecast-weather/user/{user_id}")
    assert get_weather_forecast_response.status_code == 200


@pytest.mark.asyncio
async def test_put_weather_forecast(use_test_client):
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
    get_weather_forecast_response = use_test_client.post(f"/api/v1/forecast-weather/{city}", headers=headers)
    assert get_weather_forecast_response.status_code == 201

    response_json = get_weather_forecast_response.json()

    id = int(response_json["weathers"][0]["id"])
    
    json_request = {
        "id": id,
        "city": "Curitiba",
        "latitude": -25.504,
        "longitude": -49.2908,
        "date": "2024-10-07T15:50:56",
        "average_temperature": 12.76,
        "min_temperature": 12.76,
        "max_temperature": 12.76,
        "weather_description": "nublado",
        "humidity": 86,
        "wind_speed": 2.45
    }
    put_weather_forecast_response = use_test_client.put(f"/api/v1/forecast-weather/{id}", headers=headers, json=json_request)
    assert put_weather_forecast_response.status_code == 200

    response_json = put_weather_forecast_response.json()


@pytest.mark.asyncio
async def test_delete_weather_forecast(use_test_client):
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
    get_weather_forecast_response = use_test_client.post(f"/api/v1/forecast-weather/{city}", headers=headers)
    assert get_weather_forecast_response.status_code == 201

    response_json = get_weather_forecast_response.json()

    id = int(response_json["weathers"][0]["id"])

    delete_weather_forecast_response = use_test_client.delete(f"/api/v1/forecast-weather/{id}", headers=headers)
    assert delete_weather_forecast_response.status_code == 200

    response_json = delete_weather_forecast_response.json()

