import http.server
import socketserver
import subprocess
import os
import sys
import threading
import webbrowser
import time
# Necessary imports for the server functionality

# Configurations

PORT = 8000
HTML_FILE_PATH = "TwistedWizard.html" 
PYGAME_SCRIPT_PATH = "Main.py" 
# Port and paths to the HTML menu and Pygame script

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Handles get reqeuest
        if self.path == '/start-game': # Matches the href="/start-game" in your menu.html
            print(f"[{time.strftime('%H:%M:%S')}] Received /start-game request. Launching Pygame...")
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*') # Allow CORS for fetch
            self.end_headers()
            self.wfile.write(b"Launching the game")

            try:
                subprocess.Popen([sys.executable, PYGAME_SCRIPT_PATH],
                                 cwd=os.path.dirname(os.path.abspath(PYGAME_SCRIPT_PATH)))
            except Exception as e:
                self.wfile.write(f"Error to launch game: {e}".encode())
        
        # Requests for html page
        elif self.path == '/' or self.path == '/index.html':
            self.path = HTML_FILE_PATH # Serve the menu.html file
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        
        else:
            # Serve like other static files (assets)
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

def run_server():
    # TCP server listens on PORT and uses MyHandler to handle requests
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        httpd.serve_forever() 

if __name__ == "__main__":
    # Change the current working directory to where this script is located.
    # This ensures relative paths (like "menu.html", "Main.py", "assets/") are found correctly.
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # Start the HTTP server in a separate thread
    # This allows the main program to continue 
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True # Daemon thread will exit when the main program exits
    server_thread.start()

    time.sleep(1)

    # Opens page in user web browser
    webbrowser.open_new_tab(f"http://127.0.0.1:{PORT}/{HTML_FILE_PATH}")

    # Keeps main thread alive
    try:
        while True:
            time.sleep(1) # Keep the main thread sleeping
    except KeyboardInterrupt:
        sys.exit()

