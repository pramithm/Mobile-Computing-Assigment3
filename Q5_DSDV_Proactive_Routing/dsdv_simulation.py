
import os
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# Q5: DSDV PROACTIVE ROUTING SIMULATION
# ==========================================

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

UPDATE_INTERVAL = 15  # seconds
SIMULATION_TIME = 150

# ==========================================
# 1. CREATE MOBILE AD HOC TOPOLOGY
# ==========================================

def create_network():

    G = nx.Graph()

    G.add_edges_from([
        ("A", "B"),
        ("B", "C"),
        ("B", "D"),
        ("B", "E"),
        ("E", "D"),
        ("D", "C"),
        ("B", "F"),
        ("F", "E")
    ])

    return G


def draw_topology(G, filename, title, broken_edge=None):

    positions = {
        "A": (0, 1),
        "B": (2, 1),
        "C": (5, 2),
        "D": (4, 0),
        "E": (3, -1),
        "F": (1, -1)
    }

    plt.figure(figsize=(9, 6))

    edge_colors = []

    for u, v in G.edges():

        if broken_edge and set((u, v)) == set(broken_edge):
            edge_colors.append("red")
        else:
            edge_colors.append("gray")

    nx.draw_networkx(
        G,
        pos=positions,
        node_color="skyblue",
        node_size=1700,
        font_size=13,
        font_weight="bold",
        edge_color=edge_colors,
        width=2.5
    )

    if broken_edge:
        x1, y1 = positions[broken_edge[0]]
        x2, y2 = positions[broken_edge[1]]

        plt.plot(
            [x1, x2], [y1, y2],
            color="red",
            linestyle="--",
            linewidth=2
        )

    plt.title(title, fontsize=15)
    plt.axis("off")
    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/{filename}",
        dpi=300
    )

    plt.show()


# ==========================================
# 2. DSDV ROUTING TABLES AT NODE A
# ==========================================

def create_routing_tables():

    before = [
        ["A", "A", 0, 206],
        ["B", "B", 1, 134],
        ["C", "B", 2, 156],
        ["D", "B", 3, 210],
        ["E", "B", 2, 178],
        ["F", "B", 4, 322]
    ]

    immediate = [
        ["A", "A", 0, 206],
        ["B", "B", 1, 134],
        ["C", "B", float("inf"), 157],
        ["D", "B", 3, 210],
        ["E", "B", 2, 178],
        ["F", "B", 4, 322]
    ]

    after = [
        ["A", "A", 0, 206],
        ["B", "B", 1, 134],
        ["C", "B", 4, 158],
        ["D", "B", 3, 210],
        ["E", "B", 2, 178],
        ["F", "B", 4, 322]
    ]

    columns = [
        "Destination",
        "Next Hop",
        "Metric",
        "Sequence Number"
    ]

    tables = {
        "before": pd.DataFrame(before, columns=columns),
        "immediate": pd.DataFrame(immediate, columns=columns),
        "after": pd.DataFrame(after, columns=columns)
    }

    for name, table in tables.items():

        table.to_csv(
            f"{OUTPUT_DIR}/routing_table_{name}.csv",
            index=False
        )

        print(f"\nROUTING TABLE - {name.upper()}")
        print("--------------------------------")
        print(table.to_string(index=False))

    return tables


# ==========================================
# 3. LINK FAILURE AND ROUTE UPDATE
# ==========================================

def simulate_link_failure():

    G = create_network()

    print("\nDSDV TOPOLOGY CHANGE")
    print("--------------------------------")

    print("Initial route from A to C:")

    route_before = nx.shortest_path(
        G, "A", "C"
    )

    print(" -> ".join(route_before))

    draw_topology(
        G,
        "topology_before_failure.png",
        "DSDV Network Before Link Failure"
    )

    # Link B-C fails
    G.remove_edge("B", "C")

    print("\nWireless link B-C has failed.")

    draw_topology(
        G,
        "topology_after_failure.png",
        "DSDV Network After Link B-C Failure",
        broken_edge=("B", "C")
    )

    tables = create_routing_tables()

    print("\nTriggered update from B:")
    print("Destination C marked unreachable.")
    print("Metric = Infinity")
    print("Sequence number = 157 (odd)")

    print("\nRoute convergence:")
    print("C advertises a newer even sequence number 158.")
    print("Alternative route: A -> B -> E -> D -> C")
    print("Updated metric: 4 hops")

    route_after = nx.shortest_path(
        G, "A", "C"
    )

    print(
        "Verified graph route:",
        " -> ".join(route_after)
    )

    return tables


# ==========================================
# 4. PERIODIC ROUTING UPDATE ANALYSIS
# ==========================================

def simulate_periodic_updates():

    update_times = list(
        range(
            UPDATE_INTERVAL,
            SIMULATION_TIME + 1,
            UPDATE_INTERVAL
        )
    )

    records = []

    for time in update_times:

        records.append({
            "Time (seconds)": time,
            "Update Type": "Full routing table dump",
            "Update Interval (seconds)": UPDATE_INTERVAL
        })

    df = pd.DataFrame(records)

    df.to_csv(
        f"{OUTPUT_DIR}/periodic_updates.csv",
        index=False
    )

    print("\nPERIODIC ROUTING UPDATES")
    print("--------------------------------")
    print(df.to_string(index=False))

    return df


# ==========================================
# 5. CONTROL OVERHEAD BY NETWORK SIZE
# ==========================================

def analyze_network_size():

    # DSDV simulation results from the assignment model
    data = [
        [10, 3.8, 44.2, 20.7],
        [20, 17.8, 70.4, 25.4],
        [30, 38.8, 84.0, 26.7],
        [40, 61.9, 84.6, 28.6],
        [50, 86.7, 85.5, 29.3]
    ]

    df = pd.DataFrame(
        data,
        columns=[
            "Number of Nodes",
            "Control Transmissions/s",
            "Packet Delivery (%)",
            "Average Delay (ms)"
        ]
    )

    df.to_csv(
        f"{OUTPUT_DIR}/network_size_analysis.csv",
        index=False
    )

    print("\nNETWORK SIZE PERFORMANCE")
    print("--------------------------------")
    print(df.to_string(index=False))

    # Graph 1: Control overhead
    plt.figure(figsize=(9, 5))

    plt.plot(
        df["Number of Nodes"],
        df["Control Transmissions/s"],
        marker="o",
        linewidth=2
    )

    plt.title("DSDV Control Overhead vs Network Size")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Control Transmissions per Second")
    plt.grid(True)

    plt.savefig(
        f"{OUTPUT_DIR}/control_overhead.png",
        dpi=300
    )

    plt.show()

    # Graph 2: Packet delivery
    plt.figure(figsize=(9, 5))

    plt.plot(
        df["Number of Nodes"],
        df["Packet Delivery (%)"],
        marker="o",
        linewidth=2
    )

    plt.title("DSDV Packet Delivery vs Network Size")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Packet Delivery Ratio (%)")
    plt.grid(True)

    plt.savefig(
        f"{OUTPUT_DIR}/packet_delivery_ratio.png",
        dpi=300
    )

    plt.show()

    # Graph 3: Average delay
    plt.figure(figsize=(9, 5))

    plt.plot(
        df["Number of Nodes"],
        df["Average Delay (ms)"],
        marker="o",
        linewidth=2
    )

    plt.title("DSDV Average Delay vs Network Size")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Average Delay (ms)")
    plt.grid(True)

    plt.savefig(
        f"{OUTPUT_DIR}/average_delay.png",
        dpi=300
    )

    plt.show()

    return df


# ==========================================
# 6. DSDV PROTOCOL SUMMARY
# ==========================================

def display_protocol_summary():

    summary = [
        ["Routing Type", "Proactive / Table-driven"],
        ["Protocol", "DSDV"],
        ["Algorithm", "Distance Vector (Bellman-Ford)"],
        ["Periodic Update", "Every 15 seconds"],
        ["Triggered Update", "After topology changes"],
        ["Route Metric", "Hop count"],
        ["Route Freshness", "Sequence number"],
        ["Broken Route", "Infinite metric + odd sequence"],
        ["Fresh Route", "Newer even sequence number"]
    ]

    df = pd.DataFrame(
        summary,
        columns=["Parameter", "Description"]
    )

    df.to_csv(
        f"{OUTPUT_DIR}/dsdv_protocol_summary.csv",
        index=False
    )

    print("\nDSDV PROTOCOL SUMMARY")
    print("--------------------------------")
    print(df.to_string(index=False))


# ==========================================
# 7. MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    print("====================================")
    print(" DSDV PROACTIVE ROUTING SIMULATION")
    print("====================================")

    simulate_link_failure()

    simulate_periodic_updates()

    analyze_network_size()

    display_protocol_summary()

    print("\n====================================")
    print(" DSDV SIMULATION COMPLETED")
    print("====================================")

    print("Check the outputs folder.")
