def auth(client):
    res = client.post("/auth/sign-up", json={"email": "ops@x.com", "password": "password1"})
    return {"Authorization": f"Bearer {res.json()['access_token']}"}
def test_three_fails_then_alert_and_route(client):
    headers = auth(client)
    client.post("/targets", json={"name": "api-a", "kind": "ok"}, headers=headers)
    client.post("/targets", json={"name": "api-b", "kind": "fail"}, headers=headers)
    for _ in range(3):
        client.post("/targets/tick", headers=headers)
    states = {t["name"]: t["state"] for t in client.get("/targets", headers=headers).json()}
    assert states["api-a"] == "healthy"
    assert states["api-b"] == "down"
    alerts = client.get("/alerts", headers=headers).json()
    assert any("api-b" in a["message"] for a in alerts)
    assert client.get("/route", headers=headers).json()["name"] == "api-a"
    assert client.get("/status").json()["status"] in {"degraded", "outage"}
