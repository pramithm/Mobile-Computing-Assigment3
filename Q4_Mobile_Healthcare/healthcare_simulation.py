
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

# ==========================================
# Q4: MOBILE HEALTHCARE USING MOBILE IP
# ==========================================

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Simulation parameters
SIMULATION_TIME = 60
PACKET_RATE = 50
NORMAL_DELAY = 52

L2_HANDOFF = 50
AGENT_DISCOVERY = 20
REGISTRATION_DELAY = 110

HANDOFF_DURATION = (
    L2_HANDOFF
    + AGENT_DISCOVERY
    + REGISTRATION_DELAY
)

HANDOFF_TIMES = [20, 40]

HOME_IP = "10.1.1.5"

CARE_OF_ADDRESSES = [
    "20.2.2.1",
    "30.3.3.1",
    "40.4.4.1"
]


# ==========================================
# 1. HEALTHCARE NETWORK ARCHITECTURE
# ==========================================

def draw_healthcare_architecture():

    G = nx.DiGraph()

    nodes = [
        "Patient Sensors\nECG / SpO2 / BP",
        "Ambulance Gateway\nMobile Node",
        "Access Network A\nForeign Agent",
        "Access Network B\nForeign Agent",
        "Access Network C\nForeign Agent",
        "Hospital Gateway\nHome Agent",
        "Specialist Doctor\nCorrespondent Node",
        "EHR / Video Server"
    ]

    G.add_nodes_from(nodes)

    edges = [
        (nodes[0], nodes[1]),
        (nodes[1], nodes[2]),
        (nodes[2], nodes[5]),
        (nodes[1], nodes[3]),
        (nodes[3], nodes[5]),
        (nodes[1], nodes[4]),
        (nodes[4], nodes[5]),
        (nodes[5], nodes[6]),
        (nodes[5], nodes[7])
    ]

    G.add_edges_from(edges)

    positions = {
        nodes[0]: (0, 2),
        nodes[1]: (2, 2),
        nodes[2]: (4, 3.5),
        nodes[3]: (4, 2),
        nodes[4]: (4, 0.5),
        nodes[5]: (6, 2),
        nodes[6]: (8, 3),
        nodes[7]: (8, 1)
    }

    plt.figure(figsize=(15, 8))

    nx.draw_networkx(
        G,
        pos=positions,
        node_color="lightblue",
        node_size=3000,
        font_size=8,
        font_weight="bold",
        arrows=True,
        arrowsize=18,
        edge_color="gray",
        width=2
    )

    plt.title(
        "Mobile Healthcare Architecture Using Mobile IP",
        fontsize=15
    )

    plt.axis("off")
    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/healthcare_architecture.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()


# ==========================================
# 2. PATIENT SENSOR DATA GENERATION
# ==========================================

def generate_patient_data():

    times = np.arange(
        0,
        SIMULATION_TIME,
        1 / PACKET_RATE
    )

    rng = np.random.default_rng(42)

    data = pd.DataFrame({
        "Time (s)": times,
        "ECG (mV)": rng.normal(1.0, 0.08, len(times)),
        "SpO2 (%)": rng.normal(97, 0.5, len(times)),
        "Blood Pressure (mmHg)": rng.normal(
            120, 2, len(times)
        )
    })

    return data


# ==========================================
# 3. MOBILE IP NETWORK REGISTRATION
# ==========================================

def perform_registration():

    events = []

    print("\nMOBILE IP REGISTRATION EVENTS")
    print("--------------------------------")

    print("Permanent Home Address:", HOME_IP)

    for i, event_time in enumerate(HANDOFF_TIMES):

        old_coa = CARE_OF_ADDRESSES[i]
        new_coa = CARE_OF_ADDRESSES[i + 1]

        event = {
            "Time (s)": event_time,
            "Old CoA": old_coa,
            "New CoA": new_coa,
            "Registration Delay (ms)": REGISTRATION_DELAY,
            "Interruption (ms)": HANDOFF_DURATION
        }

        events.append(event)

        print(f"\nHandoff {i + 1} at {event_time} seconds")
        print("Old CoA:", old_coa)
        print("New CoA:", new_coa)
        print("HA binding updated.")
        print(
            "Registration delay:",
            REGISTRATION_DELAY,
            "ms"
        )
        print(
            "Total interruption:",
            HANDOFF_DURATION,
            "ms"
        )

    df = pd.DataFrame(events)

    df.to_csv(
        f"{OUTPUT_DIR}/handoff_log.csv",
        index=False
    )

    return df


# ==========================================
# 4. PACKET TRANSMISSION SIMULATION
# ==========================================

def simulate_communication(patient_data):

    total_packets = len(patient_data)

    packet_times = patient_data["Time (s)"].to_numpy()

    handoff_mask = np.zeros(
        total_packets,
        dtype=bool
    )

    # Mark packets generated during handoff
    for handoff_time in HANDOFF_TIMES:

        start = handoff_time

        end = (
            handoff_time
            + HANDOFF_DURATION / 1000
        )

        handoff_mask |= (
            (packet_times >= start)
            & (packet_times < end)
        )

    delivered = ~handoff_mask

    delays = np.full(
        total_packets,
        np.nan
    )

    delays[delivered] = NORMAL_DELAY

    results = patient_data.copy()

    results["Status"] = np.where(
        delivered,
        "Delivered",
        "Dropped"
    )

    results["One-way Delay (ms)"] = delays

    results.to_csv(
        f"{OUTPUT_DIR}/packet_transmission.csv",
        index=False
    )

    delivered_packets = int(np.sum(delivered))
    dropped_packets = int(np.sum(handoff_mask))

    pdr = (
        delivered_packets / total_packets
    ) * 100

    packet_loss = (
        dropped_packets / total_packets
    ) * 100

    average_delay = np.nanmean(delays)

    print("\nPACKET TRANSMISSION RESULTS")
    print("--------------------------------")

    print("Total packets:", total_packets)
    print("Delivered packets:", delivered_packets)
    print("Dropped packets:", dropped_packets)
    print("Packet delivery ratio:", round(pdr, 2), "%")
    print("Packet loss:", round(packet_loss, 2), "%")
    print("Average one-way delay:", average_delay, "ms")

    return results, {
        "Total Packets": total_packets,
        "Delivered Packets": delivered_packets,
        "Dropped Packets": dropped_packets,
        "Packet Delivery Ratio (%)": pdr,
        "Packet Loss (%)": packet_loss,
        "Average Delay (ms)": average_delay
    }


# ==========================================
# 5. ROUTING REQUIREMENTS
# ==========================================

def generate_requirements():

    requirements = [
        {
            "Requirement": "Mobility support",
            "Solution": "Mobile IP registration and CoA updates"
        },
        {
            "Requirement": "Low communication delay",
            "Solution": "Target one-way delay below 150 ms"
        },
        {
            "Requirement": "Reliable patient data",
            "Solution": "Acknowledgements and retransmissions"
        },
        {
            "Requirement": "Security",
            "Solution": "Authenticated registration and IPsec/TLS"
        },
        {
            "Requirement": "Handoff continuity",
            "Solution": "Buffering and fast registration"
        },
        {
            "Requirement": "Network reliability",
            "Solution": "Redundant Home Agents and link failover"
        },
        {
            "Requirement": "Data availability",
            "Solution": "EHR and hospital server backup"
        }
    ]

    df = pd.DataFrame(requirements)

    df.to_csv(
        f"{OUTPUT_DIR}/network_requirements.csv",
        index=False
    )

    print("\nNETWORK REQUIREMENTS")
    print("--------------------------------")
    print(df.to_string(index=False))

    return df


# ==========================================
# 6. PERFORMANCE SUMMARY
# ==========================================

def save_performance_summary(metrics):

    df = pd.DataFrame([
        {
            "Metric": key,
            "Value": value
        }
        for key, value in metrics.items()
    ])

    df.to_csv(
        f"{OUTPUT_DIR}/performance_summary.csv",
        index=False
    )

    print("\nPERFORMANCE SUMMARY")
    print("--------------------------------")
    print(df.to_string(index=False))


# ==========================================
# 7. PERFORMANCE GRAPHS
# ==========================================

def generate_graphs(results, metrics):

    # Graph 1: Packet delay over time
    plt.figure(figsize=(11, 5))

    plt.plot(
        results["Time (s)"],
        results["One-way Delay (ms)"],
        label="Delivered packet delay"
    )

    for t in HANDOFF_TIMES:

        plt.axvspan(
            t,
            t + HANDOFF_DURATION / 1000,
            alpha=0.2,
            color="red",
            label="Handoff interruption" if t == 20 else None
        )

    plt.title("Ambulance Communication Delay")
    plt.xlabel("Simulation Time (seconds)")
    plt.ylabel("One-way Delay (ms)")
    plt.grid(True)
    plt.legend()

    plt.savefig(
        f"{OUTPUT_DIR}/communication_delay.png",
        dpi=300
    )

    plt.show()

    # Graph 2: Packet delivery performance
    labels = ["Delivered", "Dropped"]

    values = [
        metrics["Delivered Packets"],
        metrics["Dropped Packets"]
    ]

    plt.figure(figsize=(7, 5))

    plt.bar(labels, values)

    plt.title("Patient Data Packet Delivery")
    plt.ylabel("Number of Packets")
    plt.grid(axis="y")

    plt.savefig(
        f"{OUTPUT_DIR}/packet_delivery.png",
        dpi=300
    )

    plt.show()

    # Graph 3: Patient vital signs
    plt.figure(figsize=(11, 5))

    plt.plot(
        results["Time (s)"],
        results["SpO2 (%)"],
        label="SpO2"
    )

    plt.title("Patient Oxygen Saturation Monitoring")
    plt.xlabel("Simulation Time (seconds)")
    plt.ylabel("SpO2 (%)")
    plt.grid(True)
    plt.legend()

    plt.savefig(
        f"{OUTPUT_DIR}/patient_vitals.png",
        dpi=300
    )

    plt.show()


# ==========================================
# 8. MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    print("======================================")
    print(" MOBILE HEALTHCARE MOBILE IP SIMULATION")
    print("======================================")

    print("\nGenerating network architecture...")

    draw_healthcare_architecture()

    print("\nGenerating patient sensor readings...")

    patient_data = generate_patient_data()

    print("Patient sensor records:", len(patient_data))

    handoff_log = perform_registration()

    results, metrics = simulate_communication(
        patient_data
    )

    generate_requirements()

    save_performance_summary(metrics)

    generate_graphs(results, metrics)

    print("\n======================================")
    print(" Q4 SIMULATION COMPLETED SUCCESSFULLY")
    print("======================================")

    print("Check the outputs folder.")
