# Mobile Computing – Assignment 3

## Python-Based Mobile Computing Simulations

**Programming Language:** Python  
**IDE:** Visual Studio Code  
**Operating System:** Windows  
**Python Environment:** Virtual Environment (`venv`)

---

## 1. Project Overview

This repository contains the implementation of seven Mobile Computing experiments using Python.

The objective is to understand and simulate important concepts in mobile and wireless communication, network mobility, routing protocols, healthcare applications and emergency communication systems.

The experiments use Python libraries to create network topologies, simulate communication scenarios, analyze network performance, generate graphical representations and export simulation results.

### Objectives

- Understand wireless mobility and communication.
- Implement Mobile IP registration and tunnelling.
- Compare Cellular and Ad Hoc networks.
- Develop a mobile healthcare communication simulation.
- Implement DSDV proactive routing.
- Implement AODV reactive routing.
- Design and evaluate a mobile emergency communication network.
- Analyze network performance using graphs and CSV reports.

---

## 2. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Visual Studio Code | Development environment |
| NetworkX | Network topology and routing simulations |
| NumPy | Numerical calculations |
| Pandas | Data analysis and CSV generation |
| Matplotlib | Graphs and network diagrams |
| SciPy | Scientific and numerical support |

---

## 3. Project Structure

```text
Mobile_Computing_Assignment3/
│
├── Q1_Wireless_Mobility/
│   ├── wireless_simulation.py
│   └── outputs/
│
├── Q2_Mobile_IP/
│   ├── mobile_ip.py
│   └── outputs/
│
├── Q3_Cellular_vs_AdHoc/
│   ├── network_comparison.py
│   └── outputs/
│
├── Q4_Mobile_Healthcare/
│   ├── healthcare_simulation.py
│   └── outputs/
│
├── Q5_DSDV_Proactive_Routing/
│   ├── dsdv_simulation.py
│   └── outputs/
│
├── Q6_AODV_Reactive_Routing/
│   ├── aodv_simulation.py
│   └── outputs/
│
├── Q7_Emergency_Communication_Network/
│   ├── config.py
│   ├── emergency_simulation.py
│   ├── README.md
│   └── outputs/
│
├── venv/
│
└── README.md
```

Each experiment contains its own Python implementation and an `outputs` directory for generated results.

---

## 4. Experiment Details

### Q1 – Wireless Mobility

**Folder:** `Q1_Wireless_Mobility`

**File:** `wireless_simulation.py`

**Objective:**

To simulate wireless mobility concepts and analyze communication behaviour in a mobile wireless environment.

**Implementation includes:**
- Wireless mobility simulation.
- Mobile node movement and communication analysis.
- Performance visualization.
- Graph and output generation.

**Execution:**

```bash
cd Q1_Wireless_Mobility
python wireless_simulation.py
```

---

### Q2 – Mobile IP

**Folder:** `Q2_Mobile_IP`

**File:** `mobile_ip.py`

**Objective:**

To implement Mobile IP registration, packet tunnelling and mobility management.

**Implementation includes:**
- Mobile Node (MN).
- Home Agent (HA).
- Foreign Agent (FA).
- Correspondent Node (CN).
- Home Address and Care-of Address.
- Mobile IP registration.
- IP-in-IP encapsulation.
- Packet delivery.
- Registration delay analysis.
- Tunnelling overhead analysis.
- Triangular routing analysis.
- Mobility interruption analysis.

**Execution:**

```bash
cd Q2_Mobile_IP
python mobile_ip.py
```

---

### Q3 – Cellular vs Ad Hoc Networks

**Folder:** `Q3_Cellular_vs_AdHoc`

**File:** `network_comparison.py`

**Objective:**

To compare Cellular and Ad Hoc wireless networks under normal and failure conditions.

**Implementation includes:**
- Cellular network topology.
- Ad Hoc network topology.
- Base station failure simulation.
- Wireless link failure simulation.
- Alternative route discovery.
- Network connectivity analysis.
- Cellular vs Ad Hoc comparison.

**Execution:**

```bash
cd Q3_Cellular_vs_AdHoc
python network_comparison.py
```

---

### Q4 – Mobile Healthcare

**Folder:** `Q4_Mobile_Healthcare`

**File:** `healthcare_simulation.py`

**Objective:**

To simulate a mobile healthcare communication system and demonstrate communication between mobile healthcare components.

**Implementation includes:**
- Mobile healthcare simulation.
- Healthcare communication analysis.
- Network performance evaluation.
- Generated reports and visualizations.

**Execution:**

```bash
cd Q4_Mobile_Healthcare
python healthcare_simulation.py
```

---

### Q5 – DSDV Proactive Routing

**Folder:** `Q5_DSDV_Proactive_Routing`

**File:** `dsdv_simulation.py`

**Objective:**

To implement Destination-Sequenced Distance Vector (DSDV), a proactive routing protocol used in Mobile Ad Hoc Networks.

**Implementation includes:**
- DSDV routing tables.
- Periodic routing updates.
- Triggered routing updates.
- Sequence number management.
- Link failure detection.
- Broken route identification.
- Alternative route selection.
- Route convergence.
- Network size performance analysis.

**Execution:**

```bash
cd Q5_DSDV_Proactive_Routing
python dsdv_simulation.py
```

---

### Q6 – AODV Reactive Routing

**Folder:** `Q6_AODV_Reactive_Routing`

**File:** `aodv_simulation.py`

**Objective:**

To implement Ad Hoc On-Demand Distance Vector (AODV), a reactive routing protocol for mobile wireless networks.

**Implementation includes:**
- Route Request (RREQ).
- Route Reply (RREP).
- Route Error (RERR).
- On-demand route discovery.
- Duplicate RREQ handling.
- Route establishment.
- Link failure detection.
- Route recovery.
- DSDV vs AODV comparison.
- Network size analysis.
- Mobility speed analysis.

**Execution:**

```bash
cd Q6_AODV_Reactive_Routing
python aodv_simulation.py
```

---

### Q7 – Mobile Emergency Communication Network

**Folder:** `Q7_Emergency_Communication_Network`

**Files:**
- `config.py`
- `emergency_simulation.py`

**Objective:**

To design and evaluate a mobile emergency communication network using Mobile IP, wireless mesh communication and AODV routing.

The proposed network supports communication between ambulances, police vehicles, rescue teams, medical personnel, drone relays, gateway vehicles and a central command centre.

**Module 1 – Emergency Network Architecture**
- Emergency mobile nodes.
- Wireless mesh topology.
- Drone relay nodes.
- Gateway vehicles.
- Home Agent.
- Command Centre Server.
- Microwave and satellite backhaul.

**Module 2 – Mobile IP Registration and Handoff**
- Home Address management.
- Care-of Address assignment.
- Home Agent registration.
- Gateway switching.
- Binding table updates.
- Registration delay analysis.
- Microwave vs satellite comparison.
- IP-in-IP tunnelling overhead.

**Module 3 – AODV Emergency Routing**
- RREQ broadcasting.
- RREP route establishment.
- Data packet transmission.
- Link failure detection.
- RERR generation.
- Alternative route discovery.
- Emergency communication recovery.

**Module 4 – Network Failure Analysis**
- Mobile node failure.
- Wireless link failure.
- Network partition.
- Alternative route discovery.
- Gateway backhaul restoration.
- Failure recovery evaluation.

**Module 5 – Performance Evaluation**
- End-to-end delay.
- Packet Delivery Ratio (PDR).
- AODV control transmission estimation.
- Route hop count.
- Microwave and satellite comparison.
- Performance graphs.
- CSV result generation.

**Module 6 – Joint Evaluation**
- Combined network assessment.
- Failure recovery evaluation.
- Backhaul comparison.
- Network component evaluation.
- Final conclusions.
- Simulation limitations.

**Execution:**

```bash
cd Q7_Emergency_Communication_Network
python emergency_simulation.py
```

---

## 5. Installation and Setup

### Prerequisites

- Python 3.x
- Visual Studio Code
- Windows operating system
- Python extension for VS Code

### Step 1 – Open the project

Open the `Mobile_Computing_Assignment3` folder in Visual Studio Code.

### Step 2 – Create a virtual environment

```bash
python -m venv venv
```

### Step 3 – Activate the virtual environment

For Windows Command Prompt:

```bash
venv\Scripts\activate
```

### Step 4 – Install required dependencies

```bash
pip install networkx pandas numpy matplotlib scipy
```

### Step 5 – Verify installed packages

```bash
pip list
```

---

## 6. Running the Experiments

After activating the virtual environment, navigate to the required experiment folder and execute its Python file.

Example:

```bash
cd Q7_Emergency_Communication_Network
python emergency_simulation.py
```

Repeat the process for Q1–Q6 using their respective execution commands.

Each simulation prints its execution details in the terminal and saves its generated outputs in the corresponding `outputs` directory.

---

## 7. Output and Result Analysis

The simulations generate different types of output files depending on the experiment.

| Output Type | Description |
|---|---|
| PNG | Network architecture diagrams and performance graphs |
| CSV | Simulation results, routing tables and performance metrics |
| TXT | Consolidated evaluation and final reports |
| Terminal Output | Step-by-step simulation execution and results |

The generated files are stored in their respective experiment output directories.

---

## 8. Key Concepts Covered

| Concept | Experiment |
|---|---|
| Wireless Mobility | Q1 |
| Mobile IP | Q2 |
| Cellular Networks | Q3 |
| Ad Hoc Networks | Q3 |
| Mobile Healthcare | Q4 |
| DSDV Routing | Q5 |
| AODV Routing | Q6 |
| Mobile Emergency Communication | Q7 |
| Network Failure and Recovery | Q3, Q5, Q6, Q7 |
| Performance Analysis | Q1–Q7 |

---

## 9. Learning Outcomes

Through these experiments, the following concepts are explored:

1. Understanding mobile wireless communication.
2. Learning Mobile IP architecture and mobility management.
3. Comparing infrastructure-based and infrastructure-less networks.
4. Understanding mobile healthcare communication applications.
5. Implementing proactive routing using DSDV.
6. Implementing reactive routing using AODV.
7. Understanding RREQ, RREP and RERR mechanisms.
8. Analyzing network failures and route recovery.
9. Evaluating packet delivery, communication delay and routing overhead.
10. Designing an integrated emergency communication network.

---

## 10. Important Note

The project uses Python-based analytical simulations and graph-based network models.

The generated performance values depend on the parameters and assumptions configured in the respective programs. They should not be interpreted as measurements from a real-world wireless deployment.

---

## 11. Conclusion

Mobile Computing Assignment 3 provides practical exposure to wireless communication, mobility management, mobile routing protocols and network performance analysis.

By implementing seven experiments using Python, the project demonstrates different approaches to mobile communication, routing, failure handling and emergency network design.

The final emergency communication network combines Mobile IP, wireless mesh connectivity and AODV-based routing to demonstrate how communication can be maintained through alternative paths when network failures occur.

---

**Project:** Mobile Computing – Assignment 3  
**Programming Language:** Python  
**Development Environment:** Visual Studio Code  
**Platform:** Windows  
**Repository:** Mobile_Computing_Assignment3