
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# Q1: WIRELESS NETWORK MOBILITY SIMULATION
# ==========================================

# Network configuration
AP_POSITIONS = np.array([0.0, 200.0, 400.0])
COVERAGE_RADIUS = 120.0
HYSTERESIS = 10.0

SIMULATION_TIME = 300.0
PACKETS_PER_SECOND = 20
HANDOFF_TIME = 0.250

DT = 1.0 / PACKETS_PER_SECOND
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==========================================
# PART A: NETWORK ARCHITECTURE
# ==========================================

def draw_network():

    fig, ax = plt.subplots(figsize=(12, 4))

    for i, ap in enumerate(AP_POSITIONS):

        ax.add_patch(
            plt.Circle(
                (ap, 0),
                COVERAGE_RADIUS,
                alpha=0.18
            )
        )

        ax.scatter(ap, 0, marker="^", s=180)

        ax.text(
            ap, 15,
            f"AP{i+1}",
            ha="center",
            fontsize=12
        )

    ax.scatter(200, -35, marker="o", s=100,
               label="Mobile Node")

    ax.annotate(
        "Movement direction",
        xy=(350, -35),
        xytext=(50, -35),
        arrowprops=dict(arrowstyle="->", lw=2)
    )

    ax.set_title("Wireless Network Architecture - Q1")
    ax.set_xlabel("Distance (metres)")
    ax.set_ylabel("Distance (metres)")
    ax.set_xlim(-130, 530)
    ax.set_ylim(-150, 150)
    ax.grid(True)
    ax.legend()

    plt.tight_layout()
    plt.savefig(
        f"{OUTPUT_DIR}/network_architecture.png",
        dpi=300
    )
    plt.show()


# ==========================================
# PART B: MOBILITY SIMULATION
# ==========================================

def simulate_mobility(speed, seed):

    rng = np.random.default_rng(seed)

    total_steps = int(SIMULATION_TIME / DT)

    position = 0.0
    direction = 1

    serving_ap = 0

    handoff_until = -1.0
    handoffs = 0

    total_packets = 0
    delivered_packets = 0
    handoff_drops = 0
    random_drops = 0

    delays = []
    time_values = []
    delay_values = []

    for step in range(total_steps):

        current_time = step * DT

        # 1. Move the mobile node
        position += direction * speed * DT

        # Reverse direction at corridor boundaries
        if position >= 400:
            position = 400
            direction = -1

        elif position <= 0:
            position = 0
            direction = 1

        # 2. Calculate distance to each AP
        distances = np.abs(AP_POSITIONS - position)

        best_ap = int(np.argmin(distances))

        # 3. Handoff decision using hysteresis
        if current_time >= handoff_until:

            current_distance = distances[serving_ap]
            new_distance = distances[best_ap]

            if (
                best_ap != serving_ap
                and new_distance + HYSTERESIS
                <= current_distance
            ):

                serving_ap = best_ap
                handoffs += 1

                handoff_until = (
                    current_time + HANDOFF_TIME
                )

        # 4. Generate one packet every 0.05 seconds
        total_packets += 1

        # Packet lost during handoff
        if current_time < handoff_until:

            handoff_drops += 1
            continue

        # 5. Calculate signal quality
        distance = distances[serving_ap]

        normalized_distance = min(
            distance / COVERAGE_RADIUS, 1.0
        )

        # Assumed packet loss:
        # 1% at AP centre, increasing to 5% at cell edge
        loss_probability = (
            0.01 + 0.04 * normalized_distance ** 2
        )

        if rng.random() < loss_probability:

            random_drops += 1
            continue

        # 6. Calculate one-way delay
        # 23 ms at AP centre, increasing to 55 ms
        # at the coverage edge
        delay = (
            23.0
            + 32.0 * normalized_distance ** 2
            + rng.normal(0, 1)
        )

        delay = max(delay, 0)

        delivered_packets += 1
        delays.append(delay)

        time_values.append(current_time)
        delay_values.append(delay)

    # 7. Calculate performance metrics
    packet_loss = (
        (total_packets - delivered_packets)
        / total_packets
    ) * 100

    handoff_loss = (
        handoff_drops / total_packets
    ) * 100

    average_delay = (
        np.mean(delays) if delays else 0
    )

    handoff_rate = (
        handoffs / SIMULATION_TIME
    ) * 60

    return {
        "Speed (m/s)": speed,
        "Handoffs/min": handoff_rate,
        "Packet Loss (%)": packet_loss,
        "Handoff Loss (%)": handoff_loss,
        "Average Delay (ms)": average_delay,
        "Total Packets": total_packets,
        "Delivered Packets": delivered_packets,
        "Handoffs": handoffs,
        "Time": time_values,
        "Delay": delay_values
    }


# ==========================================
# RUN FIVE EXPERIMENTS PER SPEED
# ==========================================

def run_experiments():

    speeds = [0, 1.5, 5, 15, 30]

    results = []

    detailed_results = {}

    for speed in speeds:

        runs = []

        print(f"\nTesting speed: {speed} m/s")

        for run in range(5):

            result = simulate_mobility(
                speed,
                seed=100 + run
            )

            runs.append(result)

        # Average five runs
        summary = {
            "Speed (m/s)": speed,
            "Handoffs/min": np.mean(
                [r["Handoffs/min"] for r in runs]
            ),
            "Packet Loss (%)": np.mean(
                [r["Packet Loss (%)"] for r in runs]
            ),
            "Handoff Loss (%)": np.mean(
                [r["Handoff Loss (%)"] for r in runs]
            ),
            "Average Delay (ms)": np.mean(
                [r["Average Delay (ms)"] for r in runs]
            )
        }

        results.append(summary)
        detailed_results[speed] = runs

        print(summary)

    df = pd.DataFrame(results)

    df.to_csv(
        f"{OUTPUT_DIR}/q1_results.csv",
        index=False
    )

    print("\nFINAL SIMULATION RESULTS")
    print(df.round(2).to_string(index=False))

    return df, detailed_results


# ==========================================
# PERFORMANCE GRAPHS
# ==========================================

def draw_performance_graphs(df, detailed_results):

    # Graph 1: Packet loss versus speed
    plt.figure(figsize=(8, 5))

    plt.plot(
        df["Speed (m/s)"],
        df["Packet Loss (%)"],
        marker="o"
    )

    plt.title("Packet Loss versus Mobility Speed")
    plt.xlabel("Speed (m/s)")
    plt.ylabel("Packet Loss (%)")
    plt.grid(True)

    plt.savefig(
        f"{OUTPUT_DIR}/packet_loss.png",
        dpi=300
    )

    plt.show()

    # Graph 2: Delay versus speed
    plt.figure(figsize=(8, 5))

    plt.plot(
        df["Speed (m/s)"],
        df["Average Delay (ms)"],
        marker="o"
    )

    plt.title("Average Delay versus Mobility Speed")
    plt.xlabel("Speed (m/s)")
    plt.ylabel("Average Delay (ms)")
    plt.grid(True)

    plt.savefig(
        f"{OUTPUT_DIR}/average_delay.png",
        dpi=300
    )

    plt.show()

    # Graph 3: Handoffs versus speed
    plt.figure(figsize=(8, 5))

    plt.plot(
        df["Speed (m/s)"],
        df["Handoffs/min"],
        marker="o"
    )

    plt.title("Handoff Rate versus Mobility Speed")
    plt.xlabel("Speed (m/s)")
    plt.ylabel("Handoffs per minute")
    plt.grid(True)

    plt.savefig(
        f"{OUTPUT_DIR}/handoff_rate.png",
        dpi=300
    )

    plt.show()

    # Graph 4: Delay over time at 15 m/s
    sample = detailed_results[15][0]

    plt.figure(figsize=(11, 5))

    plt.plot(
        sample["Time"],
        sample["Delay"],
        linewidth=0.8
    )

    plt.title("Packet Delay over Time at 15 m/s")
    plt.xlabel("Simulation Time (seconds)")
    plt.ylabel("One-way Delay (ms)")
    plt.grid(True)

    plt.savefig(
        f"{OUTPUT_DIR}/delay_over_time.png",
        dpi=300
    )

    plt.show()


# ==========================================
# MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    print("Q1 WIRELESS NETWORK SIMULATION")
    print("--------------------------------")

    draw_network()

    df, detailed_results = run_experiments()

    draw_performance_graphs(
        df,
        detailed_results
    )

    print("\nSimulation completed successfully!")

    print("Check the outputs folder for graphs and CSV.")
