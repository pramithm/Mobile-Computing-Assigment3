
import os
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# Q3: CELLULAR VS AD HOC WIRELESS NETWORKS
# ==========================================

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==========================================
# EXPERIMENT 1: CELLULAR NETWORK
# ==========================================

def create_cellular_network():

    G = nx.Graph()

    # Mobile devices
    G.add_nodes_from([
        "Mobile 1", "Mobile 2",
        "Mobile 3", "Mobile 4"
    ])

    # Base stations and core network
    G.add_nodes_from([
        "BS1", "BS2", "MSC", "Internet"
    ])

    # Wireless connections
    G.add_edges_from([
        ("Mobile 1", "BS1"),
        ("Mobile 2", "BS1"),
        ("Mobile 3", "BS2"),
        ("Mobile 4", "BS2")
    ])

    # Infrastructure connections
    G.add_edges_from([
        ("BS1", "MSC"),
        ("BS2", "MSC"),
        ("MSC", "Internet")
    ])

    return G


def draw_cellular_network(G, filename, title):

    positions = {
        "Mobile 1": (0, 3),
        "Mobile 2": (2, 3),
        "Mobile 3": (5, 3),
        "Mobile 4": (7, 3),
        "BS1": (1, 1.5),
        "BS2": (6, 1.5),
        "MSC": (3.5, 0),
        "Internet": (3.5, -1.5)
    }

    colors = []

    for node in G.nodes():

        if node.startswith("Mobile"):
            colors.append("skyblue")
        elif node.startswith("BS"):
            colors.append("orange")
        elif node == "MSC":
            colors.append("lightgreen")
        else:
            colors.append("lightcoral")

    plt.figure(figsize=(11, 7))

    nx.draw_networkx(
        G,
        pos=positions,
        node_color=colors,
        node_size=2300,
        font_size=9,
        font_weight="bold",
        edge_color="gray",
        width=2
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
# EXPERIMENT 2: CELLULAR FAILURE
# ==========================================

def test_cellular_failure():

    G = create_cellular_network()

    source = "Mobile 1"
    destination = "Internet"

    print("\nCELLULAR NETWORK FAILURE TEST")
    print("--------------------------------")

    # Normal communication
    try:
        route = nx.shortest_path(
            G, source, destination
        )

        print("Before failure:", route)
        before = True

    except nx.NetworkXNoPath:
        before = False

    # Base station failure
    G.remove_node("BS1")

    print("\nBS1 has failed.")

    try:
        route = nx.shortest_path(
            G, source, destination
        )

        print("After failure:", route)
        after = True

    except nx.NetworkXNoPath:
        print("After failure: No route available.")
        after = False

    draw_cellular_network(
        G,
        "cellular_failure.png",
        "Cellular Network After BS1 Failure"
    )

    return before, after


# ==========================================
# EXPERIMENT 3: AD HOC NETWORK
# ==========================================

def create_adhoc_network():

    G = nx.Graph()

    # Mobile nodes
    G.add_nodes_from([
        "S", "A", "B", "C", "E", "D"
    ])

    # Primary route: S -> A -> B -> D
    # Alternative route: S -> C -> E -> D
    G.add_edges_from([
        ("S", "A"),
        ("A", "B"),
        ("B", "D"),
        ("S", "C"),
        ("C", "E"),
        ("E", "D")
    ])

    return G


def draw_adhoc_network(G, filename, title, route=None):

    positions = {
        "S": (0, 1),
        "A": (1, 2),
        "B": (3, 2),
        "C": (1, 0),
        "E": (3, 0),
        "D": (4, 1)
    }

    route_edges = set()

    if route:

        route_edges = {
            tuple(sorted((route[i], route[i+1])))
            for i in range(len(route)-1)
        }

    edge_colors = []

    for u, v in G.edges():

        if tuple(sorted((u, v))) in route_edges:
            edge_colors.append("green")
        else:
            edge_colors.append("gray")

    plt.figure(figsize=(9, 6))

    nx.draw_networkx(
        G,
        pos=positions,
        node_color="skyblue",
        node_size=1800,
        font_size=12,
        font_weight="bold",
        edge_color=edge_colors,
        width=3
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
# EXPERIMENT 4: AD HOC LINK FAILURE
# ==========================================

def test_adhoc_failure():

    G = create_adhoc_network()

    source = "S"
    destination = "D"

    print("\nAD HOC NETWORK FAILURE TEST")
    print("----------------------------")

    # Before link failure
    route_before = nx.shortest_path(
        G, source, destination
    )

    print("Before failure:", route_before)

    draw_adhoc_network(
        G,
        "adhoc_before_failure.png",
        "Ad Hoc Network Before Link Failure",
        route_before
    )

    # Break one link
    G.remove_edge("A", "B")

    print("\nLink A-B has failed.")

    # Find alternative route
    try:

        route_after = nx.shortest_path(
            G, source, destination
        )

        print("Alternative route:", route_after)

        draw_adhoc_network(
            G,
            "adhoc_after_failure.png",
            "Ad Hoc Network After Link Failure",
            route_after
        )

        after = True

    except nx.NetworkXNoPath:

        print("No alternative route available.")
        after = False

    return True, after


# ==========================================
# EXPERIMENT 5: COMPARISON TABLE
# ==========================================

def generate_comparison():

    comparison = [
        {
            "Parameter": "Infrastructure",
            "Cellular": "Fixed base stations and core",
            "Ad Hoc": "No fixed infrastructure"
        },
        {
            "Parameter": "Communication",
            "Cellular": "Centralized through base station",
            "Ad Hoc": "Direct or multi-hop"
        },
        {
            "Parameter": "Routing",
            "Cellular": "Handled by core network",
            "Ad Hoc": "Distributed routing"
        },
        {
            "Parameter": "Mobility",
            "Cellular": "Managed handoff",
            "Ad Hoc": "Topology changes"
        },
        {
            "Parameter": "Topology",
            "Cellular": "Fixed cell structure",
            "Ad Hoc": "Dynamic topology"
        },
        {
            "Parameter": "Scalability",
            "Cellular": "Expand using additional cells",
            "Ad Hoc": "Limited by routing overhead"
        },
        {
            "Parameter": "Handoff",
            "Cellular": "Network-controlled",
            "Ad Hoc": "Route discovery and repair"
        },
        {
            "Parameter": "Failure Handling",
            "Cellular": "Base station failure affects its cell",
            "Ad Hoc": "Alternative paths may be found"
        },
        {
            "Parameter": "Applications",
            "Cellular": "Mobile broadband and telephony",
            "Ad Hoc": "Disaster recovery and rescue"
        }
    ]

    df = pd.DataFrame(comparison)

    df.to_csv(
        f"{OUTPUT_DIR}/network_comparison.csv",
        index=False
    )

    print("\nCELLULAR VS AD HOC COMPARISON")
    print("-----------------------------")

    print(df.to_string(index=False))

    return df


# ==========================================
# EXPERIMENT 6: CONNECTIVITY SUMMARY
# ==========================================

def generate_connectivity_results(
    cellular_before,
    cellular_after,
    adhoc_before,
    adhoc_after
):

    data = [
        {
            "Network": "Cellular",
            "Condition": "Normal",
            "Communication": cellular_before
        },
        {
            "Network": "Cellular",
            "Condition": "BS1 failure",
            "Communication": cellular_after
        },
        {
            "Network": "Ad Hoc",
            "Condition": "Normal",
            "Communication": adhoc_before
        },
        {
            "Network": "Ad Hoc",
            "Condition": "Link A-B failure",
            "Communication": adhoc_after
        }
    ]

    df = pd.DataFrame(data)

    df["Status"] = df["Communication"].map({
        True: "Connected",
        False: "Disconnected"
    })

    df.to_csv(
        f"{OUTPUT_DIR}/connectivity_results.csv",
        index=False
    )

    print("\nCONNECTIVITY RESULTS")
    print("--------------------")
    print(df.to_string(index=False))


# ==========================================
# MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    print("====================================")
    print(" Q3: CELLULAR VS AD HOC SIMULATION")
    print("====================================")

    # Cellular architecture
    cellular = create_cellular_network()

    draw_cellular_network(
        cellular,
        "cellular_architecture.png",
        "Cellular Network Architecture"
    )

    # Cellular failure
    cellular_before, cellular_after = (
        test_cellular_failure()
    )

    # Ad hoc failure
    adhoc_before, adhoc_after = test_adhoc_failure()

    # Comparison table
    generate_comparison()

    # Connectivity results
    generate_connectivity_results(
        cellular_before,
        cellular_after,
        adhoc_before,
        adhoc_after
    )

    print("\n====================================")
    print(" Q3 SIMULATION COMPLETED")
    print("====================================")

    print("Check the outputs folder.")
