# Quantum-Kube Orchestrator: Hybrid Cloud Infrastructure
### *Productionizing Quantum-Classical Workflows with Kubernetes & Qiskit*

## 🌐 Architectural Vision
As Quantum Computing moves from research labs to production, the primary challenge is the **Classical-to-Quantum Bottleneck**. This project demonstrates a production-grade gateway designed to orchestrate hybrid quantum-classical jobs with a focus on low-latency, security, and self-healing reliability.



## 🛠 The Tech Stack: Why These Choices?

| Component | Technology | Architectural Rationale |
| :--- | :--- | :--- |
| **Orchestration** | **Kubernetes (K8s)** | Enables horizontal scaling and "Self-Healing." If a quantum simulation pod crashes due to memory limits, K8s restarts it automatically, ensuring high availability. |
| **Inference API** | **FastAPI (Asynchronous)** | Chosen over Flask for its native `async` support. In hybrid jobs, the classical CPU often waits for the QPU; `async` prevents the gateway from blocking during long-range entanglement tasks. |
| **CI/CD** | **GitHub Actions** | Implements "Infrastructure as Code" (IaC). Every change is automatically validated in a temporary Minikube cluster before being allowed into production. |
| **Security** | **K8s Secrets** | Decouples sensitive IBM/Azure Quantum API keys from the source code, following **Least Privilege** security principles. |
| **Observability** | **Metrics Server** | Quantum simulations scale exponentially ($2^n$). Monitoring memory spikes is critical to prevent "Noisy Neighbor" issues in a shared cluster. |

---

## 🚀 Senior-Level Architectural Features

### 1. Circuit-Aware Admission Control
I implemented logic to validate qubit counts *before* execution. Since memory requirements grow exponentially, this prevents **Resource Exhaustion** attacks and ensures the cluster remains stable under heavy loads.

### 2. DevOps for Quantum (Q-Ops)
Instead of manual deployment, I built a full CI/CD pipeline. This ensures that the physics logic (Qiskit) and the infrastructure logic (YAML/Docker) are tested together in an integrated environment.

### 3. Production Hardening & Compliance
* **Non-Root Containers:** The Docker image runs as a limited user (`quantumuser`), meeting strict US and EU (BSI/NIST) security compliance standards.
* **Liveness/Readiness Probes:** The cluster distinguishes between a pod that is "starting up" and a pod that is "ready to calculate," preventing dropped requests during scaling events.

---

## 📈 Performance & Scaling Insights
During the "Stress Test" phase, I observed the following resource behavior:
* **4-Qubit Job:** ~250MiB RAM / Negligible CPU.
* **10-Qubit Job:** ~480MiB RAM / 40% CPU Spike.
* **Architectural Takeaway:** To scale to 20+ qubits, the architecture would need to transition from standard Pods to **K8s Jobs** or **Argo Workflows** to handle the long-tail execution times without timing out the API Gateway.

---

## 🛠 Local Setup & Replicability

### Prerequisites
* WSL2 (Ubuntu)
* Docker Engine (Linux-native)
* Minikube & Kubectl

### Deployment Steps
1. **Start Infrastructure:**
   ```bash
   minikube start --driver=docker
   minikube addons enable metrics-server