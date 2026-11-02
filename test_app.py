import os
os.environ["AGENTUTILITY_API_KEY"]="test-secret-key-abcdefghijklmnopqrstuvwxyz"
from fastapi.testclient import TestClient
from app import app
client=TestClient(app)
headers={"X-API-Key":os.environ["AGENTUTILITY_API_KEY"]}
job={"labor_hours":10,"labor_rate":50,"materials":500,"target_margin":0.2}
def test_health(): assert client.get("/health").status_code==200
def test_no_key(): assert client.post("/v1/job-pricing",json=job).status_code==401
def test_bad_key(): assert client.post("/v1/job-pricing",json=job,headers={"X-API-Key":"bad"}).status_code==401
def test_job():
    r=client.post("/v1/job-pricing",json=job,headers=headers)
    assert r.status_code==200 and r.json()["recommended_price"]=="1250.00"
def test_invalid_margin():
    assert client.post("/v1/job-pricing",json={**job,"target_margin":1},headers=headers).status_code==422
def test_change_order():
    r=client.post("/v1/change-order",json={**job,"change_order_id":"CO-1","description":"Extra work","tax_rate":0.1},headers=headers)
    assert r.status_code==200 and r.json()["customer_total"]=="1375.00"
def test_invoice():
    r=client.post("/v1/invoice-check",json={"lines":[{"description":"Part","quantity":2,"unit_price":10,"stated_total":20}],"stated_subtotal":20,"stated_tax":0,"stated_total":20},headers=headers)
    assert r.status_code==200 and r.json()["valid"] is True
