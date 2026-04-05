from fastapi import FastAPI
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
import os

app = FastAPI()

@app.get("/")
def health_check():
    return {"status": "Quantum Node Online", "workload": "Production-Ready"}

@app.get("/connection-status")
def check_connection():
    token = os.getenv("QUANTUM_TOKEN", "No Token Found")
    return {
        "backend": "Simulated_IBM_Q",
        "authorized": token != "No Token Found",
        "token_preview": f"{token[:5]}***" if token != "No Token Found" else "None"
    }

@app.post("/run-circuit")
def run_quantum_task(qubits: int = 2):
    # Classical Pre-processing
    if qubits > 12:  # Limit for local simulation safety
        return {"error": "Too many qubits for this pod's resource limits"}

    # Quantum Logic
    qc = QuantumCircuit(qubits)
    qc.h(0)  # Put the first qubit in superposition
    for i in range(1, qubits):
        qc.cx(0, i) # Entangle
        
    # Execution (Simulated)
    state = Statevector.from_instruction(qc)
    
    # Return results
    return {
        "message": f"Successfully executed {qubits}-qubit GHZ state",
        "result_metadata": str(state.probabilities_dict())
    }