
# ==========================================
# Q7: EMERGENCY COMMUNICATION NETWORK
# CONFIGURATION
# ==========================================

import os

# Output directory
OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Network configuration
NETWORK_AREA = (1000, 1000)
RADIO_RANGE = 250

# Mobile nodes
RESPONDERS = [
    "Ambulance",
    "Police",
    "Rescue_Team",
    "Medical_Team"
]

DRONE_RELAYS = [
    "Drone_1",
    "Drone_2"
]

GATEWAYS = [
    "Gateway_A",
    "Gateway_B"
]

# Mobile IP configuration
HOME_ADDRESS = "10.0.0.10"

CARE_OF_ADDRESSES = {
    "Gateway_A": "20.0.0.1",
    "Gateway_B": "30.0.0.1"
}

HOME_AGENT = "Command_Centre_HA"
CORRESPONDENT_NODE = "Command_Centre_Server"

# Backhaul delays (one-way)
MICROWAVE_DELAY = 40
SATELLITE_DELAY = 270

# Registration parameters
WIRELESS_DELAY = 10
HA_PROCESSING_DELAY = 10

# Handoff parameters
LAYER2_HANDOFF = 50
AGENT_DISCOVERY = 20

# Network parameters
PACKET_RATE = 50
TUNNEL_HEADER = 20
PAYLOAD_SIZE = 200

# Simulation configuration
SIMULATION_DURATION = 150
TIME_STEP = 0.5

# Routing configuration
DSDV_UPDATE_INTERVAL = 15
AODV_HELLO_INTERVAL = 1
NUMBER_OF_FLOWS = 8

print("Q7 configuration loaded successfully.")
