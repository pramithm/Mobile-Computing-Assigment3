
import os
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# Q2: MOBILE IP AND MOBILITY MANAGEMENT
# ==========================================

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Network configuration
MN_HOME_IP = "10.1.1.5"
HA_IP = "10.1.1.1"
FA_IP = "20.2.2.1"
CN_IP = "30.3.3.7"

BINDING_LIFETIME = 300  # seconds

WIRELESS_DELAY = 10     # ms
FA_HA_DELAY = 40        # ms, one-way
HA_PROCESSING = 10      # ms

L2_HANDOFF = 50         # ms
AGENT_DISCOVERY = 20    # ms

TUNNEL_HEADER = 20      # bytes
IP_UDP_HEADER = 40      # bytes


# ==========================================
# 1. MOBILE IP COMPONENTS
# ==========================================

class MobileNode:

    def __init__(self, home_ip):

        self.home_ip = home_ip
        self.care_of_address = None
        self.is_away = False

    def discover_agent(self, foreign_agent):

        print("\n[MN] Agent advertisement received.")
        print("[MN] Foreign Agent:", foreign_agent.ip)

        self.care_of_address = foreign_agent.ip
        self.is_away = True

        return self.care_of_address


class HomeAgent:

    def __init__(self, ip):

        self.ip = ip
        self.binding_table = {}

    def register_mobile_node(self, mobile_node, coa):

        self.binding_table[mobile_node.home_ip] = {
            "care_of_address": coa,
            "lifetime": BINDING_LIFETIME
        }

        print("\n[HA] Registration accepted.")
        print("[HA] Binding table updated:")
        print(
            mobile_node.home_ip,
            "->",
            coa
        )

    def get_care_of_address(self, home_ip):

        entry = self.binding_table.get(home_ip)

        if entry is None:
            return None

        return entry["care_of_address"]

    def encapsulate(self, packet, coa):

        tunnel_packet = {
            "outer_source": self.ip,
            "outer_destination": coa,
            "protocol": "IP-in-IP",
            "inner_packet": packet,
            "tunnel_header_bytes": TUNNEL_HEADER
        }

        print("\n[HA] IP-in-IP encapsulation completed.")
        print("[HA] Outer source:", self.ip)
        print("[HA] Outer destination:", coa)

        return tunnel_packet


class ForeignAgent:

    def __init__(self, ip):

        self.ip = ip

    def receive_registration(self, mobile_node, home_agent):

        print("\n[FA] Forwarding registration request to HA.")

        home_agent.register_mobile_node(
            mobile_node,
            mobile_node.care_of_address
        )

        print("[FA] Registration reply received from HA.")

    def decapsulate(self, tunnel_packet):

        print("\n[FA] Tunnel packet received.")
        print("[FA] Removing outer IP header.")

        return tunnel_packet["inner_packet"]


class CorrespondentNode:

    def __init__(self, ip):

        self.ip = ip

    def create_packet(self, destination, payload_size):

        packet = {
            "source": self.ip,
            "destination": destination,
            "payload_bytes": payload_size,
            "header_bytes": IP_UDP_HEADER
        }

        print("\n[CN] Packet created.")
        print("[CN] Source:", self.ip)
        print("[CN] Destination:", destination)

        return packet


# ==========================================
# 2. MOBILE IP SIMULATION
# ==========================================

def run_mobile_ip():

    print("\n================================")
    print(" MOBILE IP SIMULATION")
    print("================================")

    mn = MobileNode(MN_HOME_IP)
    ha = HomeAgent(HA_IP)
    fa = ForeignAgent(FA_IP)
    cn = CorrespondentNode(CN_IP)

    # Step 1: Agent discovery
    coa = mn.discover_agent(fa)

    # Step 2: Registration request
    print("\n[MN] Sending registration request.")

    registration_request = {
        "home_address": mn.home_ip,
        "care_of_address": coa,
        "lifetime": BINDING_LIFETIME
    }

    print("[MN] Request:", registration_request)

    # Step 3: FA forwards request to HA
    fa.receive_registration(mn, ha)

    # Step 4: Registration reply
    print("\n[MN] Registration successful.")
    print("[MN] Permanent home IP:", mn.home_ip)
    print("[MN] Current CoA:", mn.care_of_address)

    # Step 5: CN sends packet to home address
    packet = cn.create_packet(
        MN_HOME_IP,
        payload_size=200
    )

    # Step 6: HA checks binding table
    coa = ha.get_care_of_address(
        packet["destination"]
    )

    if coa is None:
        print("[HA] No valid binding found.")
        return

    # Step 7: HA encapsulates packet
    tunnel_packet = ha.encapsulate(
        packet,
        coa
    )

    # Step 8: FA decapsulates packet
    delivered_packet = fa.decapsulate(
        tunnel_packet
    )

    # Step 9: Deliver packet to MN
    print("\n[MN] Packet successfully delivered.")
    print(
        "[MN] Original destination:",
        delivered_packet["destination"]
    )

    print("\nMOBILE IP PACKET DELIVERY SUCCESSFUL")

    return ha


# ==========================================
# 3. REGISTRATION DELAY ANALYSIS
# ==========================================

def calculate_registration_delay():

    delay = (
        2 * (WIRELESS_DELAY + FA_HA_DELAY)
        + HA_PROCESSING
    )

    print("\nREGISTRATION DELAY ANALYSIS")
    print("---------------------------")

    print("Wireless delay:", WIRELESS_DELAY, "ms")
    print("FA-HA delay:", FA_HA_DELAY, "ms")
    print("HA processing:", HA_PROCESSING, "ms")

    print("Total registration delay:", delay, "ms")

    return delay


# ==========================================
# 4. TUNNELLING OVERHEAD ANALYSIS
# ==========================================

def calculate_tunnelling_overhead():

    payload_sizes = [100, 200, 500, 1000, 1400]

    results = []

    print("\nTUNNELLING OVERHEAD ANALYSIS")
    print("----------------------------")

    for payload in payload_sizes:

        original_size = (
            payload + IP_UDP_HEADER
        )

        tunnel_size = (
            original_size + TUNNEL_HEADER
        )

        overhead = (
            TUNNEL_HEADER / original_size
        ) * 100

        results.append({
            "Payload (bytes)": payload,
            "Original Packet (bytes)": original_size,
            "Tunnel Packet (bytes)": tunnel_size,
            "Overhead (%)": overhead
        })

    df = pd.DataFrame(results)

    print(df.round(2).to_string(index=False))

    df.to_csv(
        f"{OUTPUT_DIR}/tunnelling_overhead.csv",
        index=False
    )

    return df


# ==========================================
# 5. TRIANGULAR ROUTING ANALYSIS
# ==========================================

def calculate_routing_delay():

    cn_ha_delay = 30
    ha_fa_delay = 40
    fa_mn_delay = 10

    mobile_ip_delay = (
        cn_ha_delay
        + ha_fa_delay
        + fa_mn_delay
    )

    direct_path_delay = 45

    print("\nTRIANGULAR ROUTING ANALYSIS")
    print("---------------------------")

    print(
        "CN -> HA -> FA -> MN:",
        mobile_ip_delay,
        "ms"
    )

    print(
        "Direct route:",
        direct_path_delay,
        "ms"
    )

    print(
        "Additional delay:",
        mobile_ip_delay - direct_path_delay,
        "ms"
    )

    return mobile_ip_delay, direct_path_delay


# ==========================================
# 6. PACKET LOSS DURING MOBILITY
# ==========================================

def calculate_mobility_interruption():

    interruption = (
        L2_HANDOFF
        + AGENT_DISCOVERY
        + calculate_registration_delay()
    )

    packet_rate = 50

    lost_packets = (
        interruption / 1000
    ) * packet_rate

    print("\nMOBILITY INTERRUPTION ANALYSIS")
    print("------------------------------")

    print("Layer-2 handoff:", L2_HANDOFF, "ms")
    print("Agent discovery:", AGENT_DISCOVERY, "ms")

    print(
        "Total interruption:",
        interruption,
        "ms"
    )

    print(
        "Estimated lost packets:",
        lost_packets
    )

    return interruption, lost_packets


# ==========================================
# 7. GENERATE GRAPHS
# ==========================================

def generate_graphs(overhead_df):

    # Graph 1: Tunnelling overhead
    plt.figure(figsize=(8, 5))

    plt.plot(
        overhead_df["Payload (bytes)"],
        overhead_df["Overhead (%)"],
        marker="o"
    )

    plt.title("Mobile IP Tunnelling Overhead")
    plt.xlabel("Payload Size (bytes)")
    plt.ylabel("Overhead (%)")
    plt.grid(True)

    plt.savefig(
        f"{OUTPUT_DIR}/tunnelling_overhead.png",
        dpi=300
    )

    plt.show()

    # Graph 2: Registration delay
    backhaul_delays = [10, 20, 40, 80, 120, 160, 200]

    registration_delays = [
        2 * (WIRELESS_DELAY + d) + HA_PROCESSING
        for d in backhaul_delays
    ]

    plt.figure(figsize=(8, 5))

    plt.plot(
        backhaul_delays,
        registration_delays,
        marker="o"
    )

    plt.title("Registration Delay versus FA-HA Delay")
    plt.xlabel("FA-HA One-way Delay (ms)")
    plt.ylabel("Registration Delay (ms)")
    plt.grid(True)

    plt.savefig(
        f"{OUTPUT_DIR}/registration_delay.png",
        dpi=300
    )

    plt.show()


# ==========================================
# 8. MAIN PROGRAM
# ==========================================


def draw_mobile_ip_architecture():

    fig, ax = plt.subplots(figsize=(12, 6))

    nodes = {
        "Correspondent\nNode (CN)\n30.3.3.7": (1, 3),
        "Home Agent\n(HA)\n10.1.1.1": (4, 3),
        "Foreign Agent\n(FA)\n20.2.2.1": (7, 3),
        "Mobile Node\n(MN)\n10.1.1.5": (10, 3)
    }

    for name, (x, y) in nodes.items():

        ax.text(
            x, y, name,
            ha="center",
            va="center",
            fontsize=10,
            bbox=dict(
                boxstyle="round,pad=0.8",
                fc="lightblue",
                ec="black"
            )
        )

    # Packet forwarding
    ax.annotate(
        "",
        xy=(3.4, 3),
        xytext=(1.8, 3),
        arrowprops=dict(arrowstyle="->", lw=2)
    )

    ax.annotate(
        "",
        xy=(6.4, 3),
        xytext=(4.8, 3),
        arrowprops=dict(
            arrowstyle="->",
            lw=2,
            color="green"
        )
    )

    ax.annotate(
        "",
        xy=(9.4, 3),
        xytext=(7.8, 3),
        arrowprops=dict(
            arrowstyle="->",
            lw=2,
            color="green"
        )
    )

    ax.text(
        5.5, 4.2,
        "IP-in-IP Tunnel",
        ha="center",
        color="green",
        fontsize=12
    )

    ax.text(
        5.5, 1.5,
        "Home Address: 10.1.1.5\n"
        "Care-of Address: 20.2.2.1\n"
        "Binding: HA maps Home Address to CoA",
        ha="center",
        fontsize=11,
        bbox=dict(
            boxstyle="round",
            fc="lightyellow",
            ec="black"
        )
    )

    ax.set_title(
        "Mobile IP Network Architecture",
        fontsize=15
    )

    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5)
    ax.axis("off")

    plt.tight_layout()

    plt.savefig(
        f"{OUTPUT_DIR}/mobile_ip_architecture.png",
        dpi=300
    )

    plt.show()


if __name__ == "__main__":
    draw_mobile_ip_architecture()
    run_mobile_ip()

    calculate_registration_delay()

    overhead_df = calculate_tunnelling_overhead()

    calculate_routing_delay()

    calculate_mobility_interruption()

    generate_graphs(overhead_df)

    print("\n================================")
    print(" MOBILE IP SIMULATION COMPLETED")
    print("================================")

    print("Check the outputs folder.")
