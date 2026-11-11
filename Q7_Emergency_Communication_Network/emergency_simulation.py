
import os
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

from config import *


# ==========================================
# MODULE 1: EMERGENCY NETWORK ARCHITECTURE
# ==========================================

def create_emergency_network():

    G = nx.Graph()

    # Emergency responder nodes
    G.add_nodes_from(RESPONDERS)

    # Drone relays
    G.add_nodes_from(DRONE_RELAYS)

    # Gateway vehicles
    G.add_nodes_from(GATEWAYS)

    # Command Centre components
    G.add_nodes_from([
        HOME_AGENT,
        CORRESPONDENT_NODE
    ])

    # Wireless mesh connections
    G.add_edges_from([
        ("Ambulance", "Police"),
        ("Ambulance", "Drone_1"),
        ("Police", "Rescue_Team"),
        ("Rescue_Team", "Medical_Team"),
        ("Drone_1", "Drone_2"),
        ("Drone_2", "Medical_Team"),
        ("Drone_1", "Gateway_A"),
        ("Drone_2", "Gateway_B")
    ])

    # Gateway backhaul connections
    G.add_edges_from([
        ("Gateway_A", HOME_AGENT),
        ("Gateway_B", HOME_AGENT),
        (HOME_AGENT, CORRESPONDENT_NODE)
    ])

    return G


def draw_emergency_architecture(G):

    positions = {
        "Ambulance": (0, 3),
        "Police": (2, 4),
        "Rescue_Team": (4, 4),
        "Medical_Team": (6, 3),

        "Drone_1": (2, 2),
        "Drone_2": (5, 2),

        "Gateway_A": (1, 0),
        "Gateway_B": (6, 0),

        HOME_AGENT: (3.5, -1.5),
        CORRESPONDENT_NODE: (3.5, -3)
    }

    colors = []

    for node in G.nodes():

        if node in RESPONDERS:
            colors.append("skyblue")

        elif node in DRONE_RELAYS:
            colors.append("gold")

        elif node in GATEWAYS:
            colors.append("orange")

        elif node == HOME_AGENT:
            colors.append("lightgreen")

        else:
            colors.append("lightcoral")

    plt.figure(figsize=(14, 9))

    nx.draw_networkx(
        G,
        pos=positions,
        node_color=colors,
        node_size=2600,
        font_size=8,
        font_weight="bold",
        edge_color="gray",
        width=2
    )

    plt.title(
        "Mobile Emergency Communication Network Architecture",
        fontsize=15
    )

    plt.text(
        3.5,
        -0.5,
        "Satellite / Microwave Backhaul",
        ha="center",
        fontsize=10
    )

    plt.axis("off")
    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "emergency_network_architecture.png"
        ),
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    print("\nEmergency network architecture generated.")


# ==========================================
# MODULE 2: MOBILE IP REGISTRATION
# ==========================================

def calculate_registration_delay(backhaul_delay):

    delay = (
        2 * (WIRELESS_DELAY + backhaul_delay)
        + HA_PROCESSING_DELAY
    )

    return delay


def calculate_handoff_interruption(registration_delay):

    return (
        LAYER2_HANDOFF
        + AGENT_DISCOVERY
        + registration_delay
    )


def simulate_registration():

    print("\n====================================")
    print(" MOBILE IP REGISTRATION SIMULATION")
    print("====================================")

    print("\nMobile Node:")
    print("Ambulance")

    print("Permanent Home Address:", HOME_ADDRESS)

    binding_table = {}

    handoff_records = []

    gateway_sequence = [
        "Gateway_A",
        "Gateway_B",
        "Gateway_A"
    ]

    for index, gateway in enumerate(gateway_sequence):

        coa = CARE_OF_ADDRESSES[gateway]

        print("\n------------------------------------")

        print(f"HANDOFF {index + 1}")

        print("[MN] Gateway advertisement received.")
        print("[MN] Current gateway:", gateway)

        print("[MN] Care-of Address:", coa)

        print("[MN] Sending registration request.")

        print("[FA] Forwarding registration request to HA.")

        # Simulate Home Agent registration
        binding_table[HOME_ADDRESS] = coa

        print("[HA] Registration accepted.")

        print("[HA] Binding table updated:")
        print(HOME_ADDRESS, "->", coa)

        print("[FA] Registration reply received.")

        print("[MN] Registration successful.")

        handoff_records.append({
            "Handoff": index + 1,
            "Gateway": gateway,
            "Home Address": HOME_ADDRESS,
            "Care-of Address": coa
        })

    handoff_df = pd.DataFrame(handoff_records)

    handoff_df.to_csv(
        os.path.join(OUTPUT_DIR, "handoff_log.csv"),
        index=False
    )

    binding_df = pd.DataFrame([
        {
            "Home Address": home,
            "Current Care-of Address": coa
        }
        for home, coa in binding_table.items()
    ])

    binding_df.to_csv(
        os.path.join(OUTPUT_DIR, "binding_table.csv"),
        index=False
    )

    print("\nFINAL HOME AGENT BINDING TABLE")
    print("------------------------------------")
    print(binding_df.to_string(index=False))

    return handoff_df


# ==========================================
# MODULE 2A: MICROWAVE AND SATELLITE
# ==========================================

def analyze_backhaul():

    scenarios = [
        ("Microwave", MICROWAVE_DELAY),
        ("Satellite", SATELLITE_DELAY)
    ]

    results = []

    print("\nBACKHAUL PERFORMANCE ANALYSIS")
    print("------------------------------------")

    for name, backhaul in scenarios:

        registration = calculate_registration_delay(
            backhaul
        )

        interruption = calculate_handoff_interruption(
            registration
        )

        lost_packets = (
            interruption / 1000
        ) * PACKET_RATE

        results.append({
            "Backhaul": name,
            "One-way FA-HA Delay (ms)": backhaul,
            "Registration Delay (ms)": registration,
            "Handoff Interruption (ms)": interruption,
            "Estimated Lost Packets": int(lost_packets)
        })

        print(f"\n{name} Backhaul")

        print(
            "Registration delay:",
            registration,
            "ms"
        )

        print(
            "Handoff interruption:",
            interruption,
            "ms"
        )

        print(
            "Estimated lost packets:",
            int(lost_packets)
        )

    df = pd.DataFrame(results)

    df.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "mobile_ip_validation.csv"
        ),
        index=False
    )

    print("\nBackhaul comparison:")
    print(df.to_string(index=False))

    return df


# ==========================================
# MODULE 2B: TUNNELLING OVERHEAD
# ==========================================

def calculate_tunnelling_overhead():

    original_packet = PAYLOAD_SIZE + 40

    tunnel_packet = (
        original_packet + TUNNEL_HEADER
    )

    overhead = (
        TUNNEL_HEADER / original_packet
    ) * 100

    print("\nIP-IN-IP TUNNELLING ANALYSIS")
    print("------------------------------------")

    print("Payload size:", PAYLOAD_SIZE, "bytes")
    print("Original packet:", original_packet, "bytes")
    print("Tunnel packet:", tunnel_packet, "bytes")
    print("Additional header:", TUNNEL_HEADER, "bytes")
    print("Overhead:", round(overhead, 2), "%")

    return overhead


# ==========================================
# MODULE 3: AODV EMERGENCY MESH ROUTING
# ==========================================

def aodv_route_discovery(G, source, destination):

    print("\nAODV ROUTE DISCOVERY")
    print("------------------------------------")

    print("[SOURCE]", source)
    print("[DESTINATION]", destination)

    broadcast_id = 1

    print("\n[RREQ] Route Request broadcast initiated.")

    print(
        f"[RREQ] Source={source}, "
        f"Destination={destination}, "
        f"Broadcast ID={broadcast_id}"
    )

    queue = [source]

    visited = {source}

    reverse_route = {
        source: None
    }

    found = False

    # RREQ propagation using breadth-first search
    while queue:

        current = queue.pop(0)

        print(f"[NODE] {current} received RREQ.")

        if current == destination:
            found = True
            break

        for neighbour in sorted(G.neighbors(current)):

            if neighbour not in visited:

                visited.add(neighbour)

                reverse_route[neighbour] = current

                print(
                    f"[RREQ] {current} forwards request "
                    f"to {neighbour}"
                )

                queue.append(neighbour)

            else:

                print(
                    f"[RREQ] Duplicate request ignored at "
                    f"{neighbour}"
                )

    if not found:

        print("\n[ERROR] No route available.")
        return None

    # Reconstruct source-to-destination route
    route = []

    current = destination

    while current is not None:

        route.append(current)

        current = reverse_route[current]

    route.reverse()

    # RREP travels back through reverse path
    print("\n[RREP] Route Reply generated.")

    reply_path = list(reversed(route))

    print(
        "[RREP] Reply path:",
        " -> ".join(reply_path)
    )

    # Install forwarding entries
    print("\n[ROUTE TABLE] Forwarding entries")

    routing_entries = []

    for index in range(len(route) - 1):

        entry = {
            "Node": route[index],
            "Destination": destination,
            "Next Hop": route[index + 1],
            "Hop Count": len(route) - index - 1
        }

        routing_entries.append(entry)

        print(
            f"{route[index]} -> "
            f"Next Hop: {route[index + 1]}"
        )

    return route, routing_entries


# ==========================================
# AODV DATA TRANSMISSION
# ==========================================

def aodv_transmit_data(route):

    print("\nEMERGENCY DATA TRANSMISSION")
    print("------------------------------------")

    if route is None:

        print("[ERROR] No route. Packet transmission failed.")

        return False

    print("[SOURCE] Ambulance")

    print("[DESTINATION] Command Centre Server")

    print("[ROUTE]", " -> ".join(route))

    print("[DATA] Emergency patient information transmitted.")

    print("[SUCCESS] Packet delivered to Command Centre.")

    return True


# ==========================================
# AODV ROUTE ERROR MESSAGE
# ==========================================

def aodv_generate_rerr(broken_link, destination):

    print("\nAODV ROUTE ERROR")
    print("------------------------------------")

    print(
        "[LINK FAILURE]",
        broken_link[0],
        "<->",
        broken_link[1]
    )

    print("[RERR] Route Error message generated.")

    print("[RERR] Unreachable destination:", destination)

    print("[RERR] Invalid route removed from routing table.")

    print("[SOURCE] Ambulance informed about route failure.")


# ==========================================
# AODV ROUTE FAILURE AND RECOVERY
# ==========================================

def simulate_emergency_aodv():

    print("\n====================================")
    print(" MODULE 3: AODV EMERGENCY ROUTING")
    print("====================================")

    G = create_emergency_network()

    source = "Ambulance"

    destination = CORRESPONDENT_NODE

    # Initial route discovery
    print("\nPHASE 1: INITIAL ROUTE DISCOVERY")

    initial_result = aodv_route_discovery(
        G,
        source,
        destination
    )

    if initial_result is None:

        print("[ERROR] Initial route discovery failed.")

        return

    initial_route, initial_entries = initial_result

    aodv_transmit_data(initial_route)

    # Save initial route table
    initial_df = pd.DataFrame(initial_entries)

    initial_df.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "aodv_initial_routing_table.csv"
        ),
        index=False
    )

    # Draw initial route
    positions = {
        "Ambulance": (0, 3),
        "Police": (2, 4),
        "Rescue_Team": (4, 4),
        "Medical_Team": (6, 3),
        "Drone_1": (2, 2),
        "Drone_2": (5, 2),
        "Gateway_A": (1, 0),
        "Gateway_B": (6, 0),
        HOME_AGENT: (3.5, -1.5),
        CORRESPONDENT_NODE: (3.5, -3)
    }

    def draw_aodv_route(graph, route, filename, title):

        plt.figure(figsize=(14, 9))

        route_edges = {
            frozenset((route[i], route[i + 1]))
            for i in range(len(route) - 1)
        }

        edge_colors = [
            "green" if frozenset(edge) in route_edges else "gray"
            for edge in graph.edges()
        ]

        nx.draw_networkx(
            graph,
            pos=positions,
            node_color="lightblue",
            node_size=2400,
            font_size=8,
            font_weight="bold",
            edge_color=edge_colors,
            width=2.5
        )

        plt.title(title, fontsize=14)

        plt.axis("off")

        plt.tight_layout()

        plt.savefig(
            os.path.join(OUTPUT_DIR, filename),
            dpi=300,
            bbox_inches="tight"
        )

        plt.show()

    draw_aodv_route(
        G,
        initial_route,
        "aodv_initial_emergency_route.png",
        "Emergency AODV Initial Route"
    )

    # Simulate wireless link failure
    print("\nPHASE 2: WIRELESS LINK FAILURE")

    broken_link = ("Drone_1", "Gateway_A")

    G.remove_edge(*broken_link)

    print(
        "[FAILURE] Wireless link",
        broken_link[0],
        "-",
        broken_link[1],
        "has failed."
    )

    # Generate RERR
    aodv_generate_rerr(
        broken_link,
        destination
    )

    # Draw network after failure
    plt.figure(figsize=(14, 9))

    nx.draw_networkx(
        G,
        pos=positions,
        node_color="lightblue",
        node_size=2400,
        font_size=8,
        font_weight="bold",
        edge_color="gray",
        width=2.5
    )

    plt.title(
        "Emergency Network After Wireless Link Failure"
    )

    plt.axis("off")

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "aodv_network_after_failure.png"
        ),
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    # Rediscover alternative route
    print("\nPHASE 3: ALTERNATIVE ROUTE DISCOVERY")

    recovery_result = aodv_route_discovery(
        G,
        source,
        destination
    )

    if recovery_result is None:

        print("[FAILURE] Network recovery unsuccessful.")

        return

    recovery_route, recovery_entries = recovery_result

    aodv_transmit_data(recovery_route)

    # Save recovered route
    recovery_df = pd.DataFrame(recovery_entries)

    recovery_df.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "aodv_recovered_routing_table.csv"
        ),
        index=False
    )

    draw_aodv_route(
        G,
        recovery_route,
        "aodv_recovered_emergency_route.png",
        "Emergency AODV Alternative Route"
    )

    # Save recovery comparison
    recovery_summary = pd.DataFrame([
        {
            "Stage": "Before link failure",
            "Route": " -> ".join(initial_route),
            "Hop Count": len(initial_route) - 1,
            "Status": "Connected"
        },
        {
            "Stage": "After route recovery",
            "Route": " -> ".join(recovery_route),
            "Hop Count": len(recovery_route) - 1,
            "Status": "Connected"
        }
    ])

    recovery_summary.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "aodv_recovery_summary.csv"
        ),
        index=False
    )

    print("\nAODV RECOVERY SUMMARY")
    print("------------------------------------")

    print(recovery_summary.to_string(index=False))

    print("\nAODV emergency routing completed successfully.")


# ==========================================
# MODULE 4: NETWORK FAILURE AND RECOVERY
# ==========================================

def find_emergency_route(G):

    source = "Ambulance"
    destination = CORRESPONDENT_NODE

    try:
        return nx.shortest_path(
            G,
            source=source,
            target=destination
        )

    except (nx.NetworkXNoPath, nx.NodeNotFound):
        return None


def draw_failure_topology(G, filename, title, route=None):

    positions = {
        "Ambulance": (0, 3),
        "Police": (2, 4),
        "Rescue_Team": (4, 4),
        "Medical_Team": (6, 3),
        "Drone_1": (2, 2),
        "Drone_2": (5, 2),
        "Gateway_A": (1, 0),
        "Gateway_B": (6, 0),
        HOME_AGENT: (3.5, -1.5),
        CORRESPONDENT_NODE: (3.5, -3)
    }

    valid_positions = {
        node: positions[node]
        for node in G.nodes()
        if node in positions
    }

    route_edges = set()

    if route:
        route_edges = {
            frozenset((route[i], route[i + 1]))
            for i in range(len(route) - 1)
        }

    edge_colors = [
        "green" if frozenset(edge) in route_edges else "gray"
        for edge in G.edges()
    ]

    plt.figure(figsize=(12, 8))

    nx.draw_networkx(
        G,
        pos=valid_positions,
        node_color="skyblue",
        node_size=2200,
        font_size=8,
        font_weight="bold",
        edge_color=edge_colors,
        width=2.5
    )

    plt.title(title)
    plt.axis("off")
    plt.tight_layout()

    plt.savefig(
        os.path.join(OUTPUT_DIR, filename),
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


def simulate_node_failure():

    print("\n====================================")
    print(" MODULE 4A: NODE FAILURE")
    print("====================================")

    G = create_emergency_network()

    initial_route = find_emergency_route(G)

    print("\nBEFORE NODE FAILURE")
    print("Route:", " -> ".join(initial_route))

    # Simulate Drone 1 failure
    failed_node = "Drone_1"

    G.remove_node(failed_node)

    print("\nNODE FAILURE DETECTED")
    print("Failed node:", failed_node)

    print("\nAODV ROUTE REDISCOVERY")

    new_route = find_emergency_route(G)

    if new_route:

        print("Alternative route:", " -> ".join(new_route))
        print("Emergency communication restored.")

    else:

        print("No alternative route available.")

    draw_failure_topology(
        G,
        "node_failure_topology.png",
        "Emergency Network After Drone Failure",
        new_route
    )

    return {
        "Experiment": "Drone node failure",
        "Failed Component": failed_node,
        "Status": "Recovered" if new_route else "Disconnected",
        "Route": " -> ".join(new_route) if new_route else "None",
        "Hop Count": len(new_route) - 1 if new_route else 0
    }


def simulate_link_failure():

    print("\n====================================")
    print(" MODULE 4B: LINK FAILURE")
    print("====================================")

    G = create_emergency_network()

    initial_route = find_emergency_route(G)

    print("\nINITIAL ROUTE")
    print(" -> ".join(initial_route))

    failed_link = ("Drone_1", "Gateway_A")

    G.remove_edge(*failed_link)

    print("\nWIRELESS LINK FAILURE")
    print("Failed link:", failed_link[0], "-", failed_link[1])

    print("[RERR] Route error generated.")
    print("[AODV] Starting alternative route discovery.")

    new_route = find_emergency_route(G)

    if new_route:

        print("\nALTERNATIVE ROUTE")
        print(" -> ".join(new_route))

        print("Communication successfully restored.")

    else:

        print("No alternative route available.")

    draw_failure_topology(
        G,
        "link_failure_topology.png",
        "Emergency Network After Link Failure",
        new_route
    )

    return {
        "Experiment": "Wireless link failure",
        "Failed Component": "Drone_1-Gateway_A",
        "Status": "Recovered" if new_route else "Disconnected",
        "Route": " -> ".join(new_route) if new_route else "None",
        "Hop Count": len(new_route) - 1 if new_route else 0
    }


def simulate_network_partition():

    print("\n====================================")
    print(" MODULE 4C: NETWORK PARTITION")
    print("====================================")

    G = create_emergency_network()

    print("\nINITIAL NETWORK")
    print("Connected:", nx.is_connected(G))

    # Disconnect both gateway backhaul connections
    G.remove_edge("Gateway_A", HOME_AGENT)
    G.remove_edge("Gateway_B", HOME_AGENT)

    print("\nNETWORK PARTITION DETECTED")

    components = list(nx.connected_components(G))

    for index, component in enumerate(components, start=1):

        print(
            f"Partition {index}:",
            sorted(component)
        )

    print("Number of partitions:", len(components))

    route_before_recovery = find_emergency_route(G)

    if route_before_recovery is None:

        print("\nCommand Centre is unreachable.")
        print("[AODV] No end-to-end route available.")

    # Restore one gateway backhaul connection
    print("\nNETWORK RECOVERY")

    G.add_edge("Gateway_B", HOME_AGENT)

    print("Gateway_B backhaul restored.")

    recovered_route = find_emergency_route(G)

    if recovered_route:

        print("Recovered route:")
        print(" -> ".join(recovered_route))

        print("Command Centre communication restored.")

    else:

        print("Network recovery unsuccessful.")

    draw_failure_topology(
        G,
        "network_partition_recovery.png",
        "Emergency Network After Partition Recovery",
        recovered_route
    )

    return {
        "Experiment": "Network partition",
        "Failed Component": "Both gateway backhaul links",
        "Status": "Recovered" if recovered_route else "Disconnected",
        "Route": " -> ".join(recovered_route) if recovered_route else "None",
        "Hop Count": len(recovered_route) - 1 if recovered_route else 0
    }


def run_module_4():

    print("\n====================================")
    print(" MODULE 4: FAILURE ANALYSIS")
    print("====================================")

    results = []

    results.append(simulate_node_failure())

    results.append(simulate_link_failure())

    results.append(simulate_network_partition())

    df = pd.DataFrame(results)

    df.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "failure_recovery_results.csv"
        ),
        index=False
    )

    print("\nFAILURE ANALYSIS SUMMARY")
    print("------------------------------------")

    print(df.to_string(index=False))

    return df


# ==========================================
# MODULE 5: PERFORMANCE EVALUATION
# ==========================================

def calculate_network_metrics(G, backhaul_type="Microwave"):

    route = find_emergency_route(G)

    if route is None:

        return {
            "Connected": False,
            "Hop Count": 0,
            "End-to-End Delay (ms)": 0,
            "Packet Delivery Ratio (%)": 0,
            "Control Transmissions": 0
        }

    hop_count = len(route) - 1

    wireless_hops = 0
    backhaul_delay = 0
    reliability = 1.0

    # Calculate delay and delivery probability per link
    for i in range(len(route) - 1):

        u = route[i]
        v = route[i + 1]

        edge = {u, v}

        if edge in [
            {"Gateway_A", HOME_AGENT},
            {"Gateway_B", HOME_AGENT}
        ]:

            if backhaul_type == "Microwave":

                backhaul_delay += MICROWAVE_DELAY
                reliability *= 0.995

            else:

                backhaul_delay += SATELLITE_DELAY
                reliability *= 0.98

        elif edge == {HOME_AGENT, CORRESPONDENT_NODE}:

            backhaul_delay += 5
            reliability *= 0.995

        else:

            wireless_hops += 1

            reliability *= 0.99

    wireless_delay = wireless_hops * WIRELESS_DELAY

    total_delay = wireless_delay + backhaul_delay

    pdr = reliability * 100

    # Approximate RREQ flood and RREP control transmissions
    reachable = nx.node_connected_component(
        G,
        "Ambulance"
    )

    reachable_graph = G.subgraph(reachable)

    rreq_transmissions = len(reachable) - 1

    rrep_transmissions = hop_count

    control_transmissions = (
        rreq_transmissions + rrep_transmissions
    )

    return {
        "Connected": True,
        "Hop Count": hop_count,
        "End-to-End Delay (ms)": round(total_delay, 2),
        "Packet Delivery Ratio (%)": round(pdr, 2),
        "Control Transmissions": control_transmissions
    }


def create_performance_scenarios():

    scenarios = []

    # Scenario 1: Normal network
    G = create_emergency_network()

    scenarios.append((
        "Normal",
        G.copy()
    ))

    # Scenario 2: 20% node failure
    G20 = create_emergency_network()

    G20.remove_nodes_from([
        "Police",
        "Rescue_Team"
    ])

    scenarios.append((
        "20% Node Failure",
        G20
    ))

    # Scenario 3: 40% node failure
    G40 = create_emergency_network()

    G40.remove_nodes_from([
        "Police",
        "Rescue_Team",
        "Medical_Team",
        "Drone_2"
    ])

    scenarios.append((
        "40% Node Failure",
        G40
    ))

    # Scenario 4: Wireless link failure
    G_link = create_emergency_network()

    G_link.remove_edge(
        "Drone_1",
        "Gateway_A"
    )

    scenarios.append((
        "Link Failure",
        G_link
    ))

    # Scenario 5: Network partition
    G_partition = create_emergency_network()

    G_partition.remove_edge(
        "Gateway_A",
        HOME_AGENT
    )

    G_partition.remove_edge(
        "Gateway_B",
        HOME_AGENT
    )

    scenarios.append((
        "Network Partition",
        G_partition
    ))

    # Scenario 6: Network recovered
    G_recovered = G_partition.copy()

    G_recovered.add_edge(
        "Gateway_B",
        HOME_AGENT
    )

    scenarios.append((
        "After Recovery",
        G_recovered
    ))

    return scenarios


def run_performance_evaluation():

    print("\n====================================")
    print(" MODULE 5: PERFORMANCE EVALUATION")
    print("====================================")

    results = []

    scenarios = create_performance_scenarios()

    for scenario_name, G in scenarios:

        for backhaul in ["Microwave", "Satellite"]:

            metrics = calculate_network_metrics(
                G,
                backhaul
            )

            record = {
                "Scenario": scenario_name,
                "Backhaul": backhaul,
                **metrics
            }

            results.append(record)

            print("\nScenario:", scenario_name)
            print("Backhaul:", backhaul)
            print("Connected:", metrics["Connected"])
            print("Hop Count:", metrics["Hop Count"])
            print(
                "End-to-End Delay:",
                metrics["End-to-End Delay (ms)"],
                "ms"
            )
            print(
                "Packet Delivery Ratio:",
                metrics["Packet Delivery Ratio (%)"],
                "%"
            )
            print(
                "Estimated Control Transmissions:",
                metrics["Control Transmissions"]
            )

    df = pd.DataFrame(results)

    df.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "emergency_performance_results.csv"
        ),
        index=False
    )

    print("\nPERFORMANCE RESULTS")
    print("------------------------------------")

    print(df.to_string(index=False))

    # --------------------------------------
    # GRAPH 1: END-TO-END DELAY
    # --------------------------------------

    connected_df = df[df["Connected"] == True]

    delay_data = connected_df[
        connected_df["Backhaul"] == "Microwave"
    ]

    plt.figure(figsize=(11, 6))

    plt.bar(
        delay_data["Scenario"],
        delay_data["End-to-End Delay (ms)"]
    )

    plt.title("Emergency Network - End-to-End Delay")
    plt.xlabel("Network Condition")
    plt.ylabel("Delay (ms)")
    plt.xticks(rotation=25)
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "emergency_end_to_end_delay.png"
        ),
        dpi=300
    )

    plt.close()

    # --------------------------------------
    # GRAPH 2: PACKET DELIVERY RATIO
    # --------------------------------------

    pdr_data = connected_df[
        connected_df["Backhaul"] == "Microwave"
    ]

    plt.figure(figsize=(11, 6))

    plt.bar(
        pdr_data["Scenario"],
        pdr_data["Packet Delivery Ratio (%)"]
    )

    plt.title("Emergency Network - Packet Delivery Ratio")
    plt.xlabel("Network Condition")
    plt.ylabel("PDR (%)")
    plt.xticks(rotation=25)
    plt.ylim(0, 105)
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "emergency_packet_delivery.png"
        ),
        dpi=300
    )

    plt.close()

    # --------------------------------------
    # GRAPH 3: CONTROL TRANSMISSIONS
    # --------------------------------------

    control_data = connected_df[
        connected_df["Backhaul"] == "Microwave"
    ]

    plt.figure(figsize=(11, 6))

    plt.bar(
        control_data["Scenario"],
        control_data["Control Transmissions"]
    )

    plt.title("Emergency Network - AODV Control Overhead")
    plt.xlabel("Network Condition")
    plt.ylabel("Estimated Control Transmissions")
    plt.xticks(rotation=25)
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "emergency_control_overhead.png"
        ),
        dpi=300
    )

    plt.close()

    # --------------------------------------
    # GRAPH 4: MICROWAVE VS SATELLITE
    # --------------------------------------

    backhaul_data = df[
        (df["Scenario"] == "Normal") &
        (df["Connected"] == True)
    ]

    plt.figure(figsize=(8, 5))

    plt.bar(
        backhaul_data["Backhaul"],
        backhaul_data["End-to-End Delay (ms)"]
    )

    plt.title("Microwave vs Satellite Backhaul Delay")
    plt.xlabel("Backhaul Technology")
    plt.ylabel("End-to-End Delay (ms)")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "backhaul_delay_comparison.png"
        ),
        dpi=300
    )

    plt.close()

    print("\nPerformance graphs generated.")

    return df



# ==========================================
# MODULE 6: JOINT EVALUATION AND FINAL REPORT
# ==========================================

def run_joint_evaluation(failure_df, performance_df):

    print("\n====================================")
    print(" MODULE 6: JOINT EVALUATION")
    print("====================================")

    # --------------------------------------
    # 1. FAILURE RECOVERY EVALUATION
    # --------------------------------------

    print("\n1. FAILURE RECOVERY EVALUATION")
    print("------------------------------------")

    print(failure_df.to_string(index=False))

    recovered_count = (
        failure_df["Status"] == "Recovered"
    ).sum()

    total_experiments = len(failure_df)

    recovery_percentage = (
        recovered_count / total_experiments
    ) * 100

    print(
        "\nRecovery success rate:",
        round(recovery_percentage, 2),
        "%"
    )

    # --------------------------------------
    # 2. BACKHAUL COMPARISON
    # --------------------------------------

    print("\n2. BACKHAUL COMPARISON")
    print("------------------------------------")

    backhaul_df = performance_df[
        (performance_df["Scenario"] == "Normal") &
        (performance_df["Connected"] == True)
    ].copy()

    print(backhaul_df.to_string(index=False))

    microwave_delay = backhaul_df.loc[
        backhaul_df["Backhaul"] == "Microwave",
        "End-to-End Delay (ms)"
    ].iloc[0]

    satellite_delay = backhaul_df.loc[
        backhaul_df["Backhaul"] == "Satellite",
        "End-to-End Delay (ms)"
    ].iloc[0]

    # --------------------------------------
    # 3. PERFORMANCE EVALUATION
    # --------------------------------------

    print("\n3. NETWORK PERFORMANCE")
    print("------------------------------------")

    performance_summary = performance_df[
        [
            "Scenario",
            "Backhaul",
            "Connected",
            "Hop Count",
            "End-to-End Delay (ms)",
            "Packet Delivery Ratio (%)",
            "Control Transmissions"
        ]
    ]

    print(performance_summary.to_string(index=False))

    # --------------------------------------
    # 4. JOINT DESIGN COMPONENTS
    # --------------------------------------

    joint_components = [
        [
            "Emergency Mobile Nodes",
            "Ambulance, Police, Rescue and Medical Teams",
            "Mobile emergency communication"
        ],
        [
            "Wireless Mesh",
            "Multi-hop wireless connections",
            "Infrastructure-independent local communication"
        ],
        [
            "Drone Relays",
            "Drone_1 and Drone_2",
            "Alternative communication paths"
        ],
        [
            "AODV",
            "RREQ, RREP and RERR",
            "On-demand routing and failure recovery"
        ],
        [
            "Mobile IP",
            "Home Agent and Foreign Agents",
            "Mobility and gateway registration"
        ],
        [
            "Backhaul",
            "Microwave and Satellite",
            "Connection to Command Centre"
        ]
    ]

    components_df = pd.DataFrame(
        joint_components,
        columns=[
            "Component",
            "Implementation",
            "Purpose"
        ]
    )

    components_df.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "joint_network_evaluation.csv"
        ),
        index=False
    )

    # --------------------------------------
    # 5. FINAL CONCLUSIONS
    # --------------------------------------

    conclusions = [
        "The emergency network uses mobile nodes, drone relays and gateway vehicles.",
        "Mobile IP maintains the mapping between the permanent Home Address and current Care-of Address.",
        "AODV establishes routes on demand using RREQ and RREP messages.",
        "RERR reports broken links and allows affected routes to be rediscovered.",
        "Alternative gateway connectivity helps restore communication after failures.",
        "Microwave backhaul provides lower delay than satellite under the configured assumptions.",
        "Network partition recovery requires restoring at least one gateway connection.",
        "Redundant mesh paths improve emergency communication availability."
    ]

    # --------------------------------------
    # 6. GENERATE FINAL TEXT REPORT
    # --------------------------------------

    report_path = os.path.join(
        OUTPUT_DIR,
        "Q7_FINAL_REPORT.txt"
    )

    with open(
        report_path,
        "w",
        encoding="utf-8"
    ) as report:

        report.write(
            "MOBILE COMPUTING ASSIGNMENT 3\n"
        )

        report.write(
            "Q7: EMERGENCY COMMUNICATION NETWORK\n"
        )

        report.write("=" * 55 + "\n\n")

        report.write("1. NETWORK ARCHITECTURE\n")
        report.write("-" * 40 + "\n")

        report.write(
            "The proposed network consists of ambulances, "
            "police vehicles, rescue teams, medical personnel, "
            "drone relays, gateway vehicles and a Command Centre.\n\n"
        )

        report.write("2. MOBILE IP IMPLEMENTATION\n")
        report.write("-" * 40 + "\n")

        report.write(
            "Mobile IP registration and gateway handoff were "
            "implemented using a Home Agent and two gateway "
            "Care-of Addresses.\n\n"
        )

        report.write(
            f"Microwave end-to-end delay: {microwave_delay} ms\n"
        )

        report.write(
            f"Satellite end-to-end delay: {satellite_delay} ms\n\n"
        )

        report.write("3. AODV ROUTING\n")
        report.write("-" * 40 + "\n")

        report.write(
            "AODV route discovery, RREQ broadcasting, RREP "
            "route establishment, data forwarding and RERR "
            "failure notification were implemented.\n\n"
        )

        report.write("4. FAILURE ANALYSIS\n")
        report.write("-" * 40 + "\n")

        report.write(
            failure_df.to_string(index=False)
        )

        report.write("\n\n")

        report.write(
            f"Recovery success rate: "
            f"{recovery_percentage:.2f}%\n\n"
        )

        report.write("5. PERFORMANCE RESULTS\n")
        report.write("-" * 40 + "\n")

        report.write(
            performance_summary.to_string(index=False)
        )

        report.write("\n\n")

        report.write("6. JOINT NETWORK COMPONENTS\n")
        report.write("-" * 40 + "\n")

        report.write(
            components_df.to_string(index=False)
        )

        report.write("\n\n")

        report.write("7. CONCLUSION\n")
        report.write("-" * 40 + "\n")

        for number, conclusion in enumerate(
            conclusions,
            start=1
        ):

            report.write(
                f"{number}. {conclusion}\n"
            )

        report.write("\n8. SIMULATION LIMITATIONS\n")
        report.write("-" * 40 + "\n")

        report.write(
            "This implementation is an analytical Python "
            "network simulation using NetworkX. Performance "
            "metrics are calculated using configured delay "
            "and packet-loss assumptions. It does not model "
            "physical radio propagation, interference, "
            "congestion or real wireless packet captures.\n"
        )

    # --------------------------------------
    # 7. SAVE CONSOLIDATED RESULTS
    # --------------------------------------

    final_df = performance_df.copy()

    final_df.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "final_performance_summary.csv"
        ),
        index=False
    )

    # --------------------------------------
    # 8. DISPLAY FINAL SUMMARY
    # --------------------------------------

    print("\n4. JOINT NETWORK COMPONENTS")
    print("------------------------------------")

    print(components_df.to_string(index=False))

    print("\n5. FINAL CONCLUSIONS")

    for number, conclusion in enumerate(
        conclusions,
        start=1
    ):

        print(f"{number}. {conclusion}")

    print("\nFINAL EVALUATION COMPLETED.")

    print("Generated:", report_path)

    return components_df




# ==========================================
# MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    print("\n====================================")
    print(" Q7 EMERGENCY NETWORK DESIGN")
    print("====================================")

    # MODULE 1
    print("\nMODULE 1: NETWORK ARCHITECTURE")

    network = create_emergency_network()

    draw_emergency_architecture(network)

    # MODULE 2
    print("\nMODULE 2: MOBILE IP")

    simulate_registration()

    analyze_backhaul()

    calculate_tunnelling_overhead()

    # MODULE 3
    print("\nMODULE 3: AODV EMERGENCY ROUTING")

    simulate_emergency_aodv()

    # MODULE 4
    print("\nMODULE 4: FAILURE ANALYSIS")

    failure_results = run_module_4()

    # MODULE 5
    print("\nMODULE 5: PERFORMANCE EVALUATION")

    performance_results = run_performance_evaluation()

    # MODULE 6
    print("\nMODULE 6: JOINT EVALUATION")

    run_joint_evaluation(
        failure_results,
        performance_results
    )

    # FINAL STATUS
    print("\n====================================")
    print(" ALL Q7 MODULES COMPLETED")
    print("====================================")

    print("\nModules completed:")
    print("1. Emergency Network Architecture")
    print("2. Mobile IP Registration and Handoff")
    print("3. AODV Emergency Routing")
    print("4. Node, Link and Partition Failure")
    print("5. Performance Evaluation")
    print("6. Joint Evaluation and Final Report")

    print("\nCheck the outputs folder.")
