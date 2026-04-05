from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "Quantum Node Online", "workload": "Production-Ready"}

def test_quantum_circuit():
    # Test a simple 2-qubit request
    response = client.post("/run-circuit?qubits=2")
    assert response.status_code == 200
    assert "Successfully executed 2-qubit GHZ state" in response.json()["message"]