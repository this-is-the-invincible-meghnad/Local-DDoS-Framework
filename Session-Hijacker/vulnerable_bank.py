from flask import Flask, request, make_response
import base64

app = Flask(__name__)

# =====================================================================
# THE VULNERABILITY: Unsigned, Predictable Session Tokens
# =====================================================================
# This server does not use secure, randomized session IDs. 
# It simply takes the user's role, Base64 encodes it, and sets it as the cookie.

@app.route('/')
def index():
    # The bouncer checking for the wristband
    session_cookie = request.cookies.get('session_id')
    
    if not session_cookie:
        return "<h1>Welcome to SecureBank</h1><p>You are not logged in. No session token found.</p>"
        
    try:
        # The server decodes the wristband to see who you are
        decoded_session = base64.b64decode(session_cookie).decode('utf-8')
        
        if decoded_session == "role=admin":
            return "<h1>Admin Dashboard</h1><p>Welcome, Administrator. Financial records unlocked.</p><p>Secret Flag: {SESSION_HIJACK_SUCCESS}</p>"
        else:
            return f"<h1>User Dashboard</h1><p>Welcome to your standard account. Role recognized as: {decoded_session}</p>"
    except Exception:
        return "Invalid session token format."

@app.route('/login/<username>')
def login(username):
    # The server creates the weak wristband and hands it to the browser
    token = f"role={username}"
    encoded_token = base64.b64encode(token.encode('utf-8')).decode('utf-8')
    
    resp = make_response(f"Logged in as {username}. Your session token has been set in your browser cookies.")
    resp.set_cookie('session_id', encoded_token)
    return resp

if __name__ == '__main__':
    print("[*] Vulnerable Bank Server booting on port 5050...")
    app.run(port=5050)