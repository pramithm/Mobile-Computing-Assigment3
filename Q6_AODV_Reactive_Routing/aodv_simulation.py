
import os
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# Q6: AODV REACTIVE ROUTING SIMULATION
# ==========================================

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==========================================
# 1. CREATE AD HOC NETWORK
# ==========================================

def create_network():

    G = nx.Graph()

    G.add_edges_from([
        ("S", "A"),
        ("A", "B"),
        ("B", "D"),
        ("S", "C"),
        ("C", "E"),
        ("E", "D"),
        ("B", "E")
    ])

    return G


def draw_network(G, filename, title, route=None):

    positions = {
        "S": (0, 1),
        "A": (1, 2),
        "B": (3, 2),
        "C": (1, 0),
        "E": (3, 0),
        "D": (5, 1)
    }

    route_edges = set()

    if route:
        route_edges = {
            frozenset((route[i], route[i + 1]))
            for i in range(len(route) - 1)
        }

    colors = [
        "green" if frozenset(edge) in route_edges else "gray"
        for edge in G.edges()
    ]

    plt.figure(figsize=(9, 6))

    nx.draw_networkx(
        G,
        pos=positions,
        node_color="skyblue",
        node_size=1700,
        font_size=12,
        font_weight="bold",
        edge_color=colors,
        width=2.5
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
# 2. AODV ROUTE DISCOVERY - RREQ
# ==========================================

def route_discovery(G, source, destination):

    print("\nAODV ROUTE DISCOVERY")
    print("--------------------------------")

    print("Source:", source)
    print("Destination:", destination)

    # Each discovery has a unique broadcast ID
    broadcast_id = 1

    print("\nRREQ BROADCAST")

    print(
        f"RREQ: Source={source}, "
        f"Destination={destination}, "
        f"Broadcast ID={broadcast_id}"
    )

    # Simulate RREQ propagation using BFS
    queue = [source]

    visited = {source}
    reverse_route = {source: None}

    destination_found = False

    while queue:

        current = queue.pop(0)

        print(f"Node {current} receives RREQ")

        if current == destination:

            destination_found = True
            break

        for neighbour in G.neighbors(current):

            if neighbour not in visited:

                visited.add(neighbour)

                reverse_route[neighbour] = current

                print(
                    f"Node {current} forwards RREQ "
                    f"to {neighbour}"
                )

                queue.append(neighbour)

            else:

                print(
                    f"Duplicate RREQ discarded at {neighbour}"
                )

    if not destination_found:

        print("\nNo route available.")
        return None

    # Reconstruct source-to-destination route
    route = []
    node = destination

    while node is not None:

        route.append(node)
        node = reverse_route[node]

    route.reverse()

    # RREP travels backwards along the reverse route
    print("\nRREP REPLY")

    reverse_path = list(reversed(route))

    print("RREP path:", " -> ".join(reverse_path))

    # Install forward route at every intermediate node
    print("\nFORWARD ROUTE INSTALLATION")

    for i in range(len(route) - 1):

        print(
            f"Node {route[i]}: "
            f"Next hop = {route[i + 1]}"
        )

    print("\nRoute established:")
    print(" -> ".join(route))

    return route


# ==========================================
# 3. DATA TRANSMISSION
# ==========================================

def transmit_data(route):

    print("\nDATA TRANSMISSION")
    print("--------------------------------")

    if route is None:
        print("Transmission failed.")
        return False

    print("Data packet follows:")

    print(" -> ".join(route))

    print("Packet successfully delivered.")

    return True


# ==========================================
# 4. ROUTE ERROR - RERR
# ==========================================

def generate_rerr(source, broken_link):

    print("\nAODV ROUTE ERROR")
    print("--------------------------------")

    print("Broken link:", broken_link[0], "-", broken_link[1])

    print("RERR message generated.")

    print(
        "Unreachable destination:",
        "D"
    )

    print(
        "RERR forwarded to affected source:",
        source
    )

    print("Source invalidates the broken route.")


# ==========================================
# 5. ROUTE FAILURE AND REDISCOVERY
# ==========================================

def simulate_route_failure():

    G = create_network()

    print("\nINITIAL NETWORK TOPOLOGY")

    draw_network(
        G,
        "aodv_initial_topology.png",
        "AODV Network Before Link Failure"
    )

    # Initial route discovery
    initial_route = route_discovery(
        G, "S", "D"
    )

    transmit_data(initial_route)

    draw_network(
        G,
        "aodv_initial_route.png",
        "AODV Initial Route",
        initial_route
    )

    # Break an active route
    broken_link = ("B", "D")

    G.remove_edge(*broken_link)

    print("\nLINK FAILURE DETECTED")
    print("--------------------------------")

    print("Link B-D has failed.")

    generate_rerr(
        "S",
        broken_link
    )

    draw_network(
        G,
        "aodv_after_failure.png",
        "AODV Network After Link Failure"
    )

    # Rediscover route
    print("\nSTARTING NEW ROUTE DISCOVERY")

    new_route = route_discovery(
        G, "S", "D"
    )

    transmit_data(new_route)

    draw_network(
        G,
        "aodv_alternative_route.png",
        "AODV Alternative Route After RERR",
        new_route
    )

    # Save route information
    records = [
        {
            "Stage": "Before failure",
            "Route": " -> ".join(initial_route),
            "Hop Count": len(initial_route) - 1,
            "Status": "Available"
        },
        {
            "Stage": "After rediscovery",
            "Route": " -> ".join(new_route),
            "Hop Count": len(new_route) - 1,
            "Status": "Available"
        }
    ]

    pd.DataFrame(records).to_csv(
        f"{OUTPUT_DIR}/route_discovery_results.csv",
        index=False
    )

    return initial_route, new_route


# ==========================================
# 6. DSDV VS AODV - NETWORK SIZE ANALYSIS
# ==========================================

def network_size_comparison():

    data = [
        [10, 3.8, 57.8, 44.2, 47.0, 20.7, 30.8],
        [20, 17.8, 123.3, 70.4, 74.9, 25.4, 44.0],
        [30, 38.8, 80.2, 84.0, 88.7, 26.7, 40.2],
        [40, 61.9, 79.3, 84.6, 89.9, 28.6, 39.8],
        [50, 86.7, 90.5, 85.5, 90.5, 29.3, 38.6]
    ]

    columns = [
        "Nodes",
        "DSDV Control/s",
        "AODV Control/s",
        "DSDV PDR (%)",
        "AODV PDR (%)",
        "DSDV Delay (ms)",
        "AODV Delay (ms)"
    ]

    df = pd.DataFrame(data, columns=columns)

    df.to_csv(
        f"{OUTPUT_DIR}/network_size_comparison.csv",
        index=False
    )

    print("\nDSDV VS AODV - NETWORK SIZE")
    print("--------------------------------")

    print(df.to_string(index=False))

    # Graph 1: Control overhead
    plt.figure(figsize=(9, 5))

    plt.plot(
        df["Nodes"],
        df["DSDV Control/s"],
        marker="o",
        label="DSDV"
    )

    plt.plot(
        df["Nodes"],
        df["AODV Control/s"],
        marker="s",
        label="AODV"
    )

    plt.title("DSDV vs AODV - Control Overhead")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Control Transmissions / Second")
    plt.grid(True)
    plt.legend()

    plt.savefig(
        f"{OUTPUT_DIR}/control_overhead_comparison.png",
        dpi=300
    )

    plt.show()

    # Graph 2: Packet delivery ratio
    plt.figure(figsize=(9, 5))

    plt.plot(
        df["Nodes"],
        df["DSDV PDR (%)"],
        marker="o",
        label="DSDV"
    )

    plt.plot(
        df["Nodes"],
        df["AODV PDR (%)"],
        marker="s",
        label="AODV"
    )

    plt.title("DSDV vs AODV - Packet Delivery Ratio")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Packet Delivery Ratio (%)")
    plt.grid(True)
    plt.legend()

    plt.savefig(
        f"{OUTPUT_DIR}/packet_delivery_comparison.png",
        dpi=300
    )

    plt.show()

    # Graph 3: End-to-end delay
    plt.figure(figsize=(9, 5))

    plt.plot(
        df["Nodes"],
        df["DSDV Delay (ms)"],
        marker="o",
        label="DSDV"
    )

    plt.plot(
        df["Nodes"],
        df["AODV Delay (ms)"],
        marker="s",
        label="AODV"
    )

    plt.title("DSDV vs AODV - Average Delay")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Average Delay (ms)")
    plt.grid(True)
    plt.legend()

    plt.savefig(
        f"{OUTPUT_DIR}/delay_comparison.png",
        dpi=300
    )

    plt.show()

    return df


# ==========================================
# 7. MOBILITY SPEED ANALYSIS
# ==========================================

def mobility_comparison():

    data = [
        [1, 7.3, 73.0, 91.8, 92.2, 30.9, 45.0],
        [5, 24.9, 65.4, 90.0, 91.9, 25.8, 36.7],
        [10, 38.8, 80.2, 84.0, 88.7, 26.7, 40.2],
        [20, 52.4, 104.2, 73.6, 83.0, 27.7, 48.5],
        [30, 57.2, 132.2, 63.5, 77.9, 26.8, 55.7]
    ]

    columns = [
        "Speed (m/s)",
        "DSDV Control/s",
        "AODV Control/s",
        "DSDV PDR (%)",
        "AODV PDR (%)",
        "DSDV Delay (ms)",
        "AODV Delay (ms)"
    ]

    df = pd.DataFrame(data, columns=columns)

    df.to_csv(
        f"{OUTPUT_DIR}/mobility_comparison.csv",
        index=False
    )

    print("\nDSDV VS AODV - MOBILITY SPEED")
    print("--------------------------------")

    print(df.to_string(index=False))

    # Graph 1: Control overhead
    plt.figure(figsize=(9, 5))

    plt.plot(
        df["Speed (m/s)"],
        df["DSDV Control/s"],
        marker="o",
        label="DSDV"
    )

    plt.plot(
        df["Speed (m/s)"],
        df["AODV Control/s"],
        marker="s",
        label="AODV"
    )

    plt.title("Routing Overhead vs Mobility Speed")
    plt.xlabel("Speed (m/s)")
    plt.ylabel("Control Transmissions / Second")
    plt.grid(True)
    plt.legend()

    plt.savefig(
        f"{OUTPUT_DIR}/mobility_overhead.png",
        dpi=300
    )

    plt.show()

    # Graph 2: Packet delivery
    plt.figure(figsize=(9, 5))

    plt.plot(
        df["Speed (m/s)"],
        df["DSDV PDR (%)"],
        marker="o",
        label="DSDV"
    )

    plt.plot(
        df["Speed (m/s)"],
        df["AODV PDR (%)"],
        marker="s",
        label="AODV"
    )

    plt.title("Packet Delivery vs Mobility Speed")
    plt.xlabel("Speed (m/s)")
    plt.ylabel("Packet Delivery Ratio (%)")
    plt.grid(True)
    plt.legend()

    plt.savefig(
        f"{OUTPUT_DIR}/mobility_delivery.png",
        dpi=300
    )

    plt.show()

    # Graph 3: Delay
    plt.figure(figsize=(9, 5))

    plt.plot(
        df["Speed (m/s)"],
        df["DSDV Delay (ms)"],
        marker="o",
        label="DSDV"
    )

    plt.plot(
        df["Speed (m/s)"],
        df["AODV Delay (ms)"],
        marker="s",
        label="AODV"
    )

    plt.title("Average Delay vs Mobility Speed")
    plt.xlabel("Speed (m/s)")
    plt.ylabel("Average Delay (ms)")
    plt.grid(True)
    plt.legend()

    plt.savefig(
        f"{OUTPUT_DIR}/mobility_delay.png",
        dpi=300
    )

    plt.show()

    return df


# ==========================================
# 8. PROTOCOL COMPARISON SUMMARY
# ==========================================

def protocol_summary():

    comparison = [
        [
            "Route discovery",
            "Periodic and triggered updates",
            "RREQ and RREP on demand"
        ],
        [
            "Routing table",
            "Entry for every destination",
            "Entries for active destinations"
        ],
        [
            "Control overhead",
            "Continuous table broadcasts",
            "Discovery floods and HELLO"
        ],
        [
            "Initial delay",
            "Low; route already available",
            "Higher; discovery required"
        ],
        [
            "Mobility handling",
            "May use temporarily stale routes",
            "RERR and route rediscovery"
        ],
        [
            "Suitable scenario",
            "Small and stable network",
            "Large or highly mobile network"
        ]
    ]

    df = pd.DataFrame(
        comparison,
        columns=[
            "Parameter",
            "DSDV",
            "AODV"
        ]
    )

    df.to_csv(
        f"{OUTPUT_DIR}/protocol_comparison.csv",
        index=False
    )

    print("\nPROTOCOL COMPARISON")
    print("--------------------------------")

    print(df.to_string(index=False))


# ==========================================
# 9. MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    print("====================================")
    print(" AODV REACTIVE ROUTING SIMULATION")
    print("====================================")

    simulate_route_failure()

    network_size_comparison()

    mobility_comparison()

    protocol_summary()

    print("\n====================================")
    print(" Q6 SIMULATION COMPLETED")
    print("====================================")

    print("Check the outputs folder.")
