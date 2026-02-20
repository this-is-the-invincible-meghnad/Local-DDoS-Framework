# Local DDoS C2 Framework

## Overview
A locally isolated Distributed Denial of Service (DDoS) Command and Control (C2) architecture. This framework demonstrates how threat actors orchestrate multi-node botnets to execute synchronized asymmetric resource exhaustion attacks against web infrastructure.

## Architecture
The framework is split into three distinct nodes:
* **The Master Node (`c2_master.py`):** The central command server. It utilizes standard Python sockets to bind to a control port, track incoming drone connections, and broadcast asynchronous execution orders.
* **The Worker Drones (`worker_node.py`):** The botnet payload delivery system. These nodes idle silently until they receive a broadcast command, at which point they utilize Python's `asyncio` event loop to flood the target with hundreds of slow keep-alive locks.
* **The Target Server (`target.py`):** A synchronous dummy HTTP server to act as the victim infrastructure.

## Features
* **Distributed Orchestration:** Synchronized attack execution across multiple disconnected terminal instances.
* **Asynchronous Payloads:** Bypasses standard GIL thread-blocking to maximize network socket saturation per worker node.
* **Live Botnet Telemetry:** The Master node actively tracks and logs worker drone connections and disconnections in real-time.

## Execution Protocol
*Disclaimer: This framework is built strictly for localized, defensive red-team research. It binds to localhost (127.0.0.1) to prevent accidental external deployment.*

1. Boot the Victim: `python target.py`
2. Boot the Command Center: `python c2_master.py`
3. Deploy Worker Drones (Run in multiple terminals): `python worker_node.py`
4. Orchestrate the Swarm (From the Master terminal):
   - Type `status` to verify botnet strength.
   - Type `attack 127.0.0.1 8080` to broadcast the execution order.

   ## Installation & Execution Protocol
*Disclaimer: This framework is built strictly for localized, defensive red-team research. It binds to localhost (127.0.0.1) to prevent accidental external deployment.*

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/this-is-the-invincible-meghnad/Local-DDoS-Framework.git](https://github.com/this-is-the-invincible-meghnad/Local-DDoS-Framework.git)
   cd Local-DDoS-Framework
   ```