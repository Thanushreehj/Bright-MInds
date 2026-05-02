# run.py - Single server with auto-open

import subprocess
import sys
import os
import webbrowser
import threading
import time

def open_browser(url, delay=2):
    """Open browser after delay"""
    time.sleep(delay)
    print(f"\n🌐 Opening browser at: {url}")
    webbrowser.open(url)

def run_server():
    """Run the Flask server"""
    port = 5000
    url = f"http://localhost:{port}"
    
    print("="*60)
    print("🧠 Bright Minds - AI Learning Platform")
    print("="*60)
    print(f"\n🚀 Starting server on port {port}...")
    print(f"📍 Access at: {url}")
    print("\n⚠️  Keep this terminal open!")
    print("⚠️  Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    # Open browser automatically
    threading.Thread(target=open_browser, args=(url,), daemon=True).start()
    
    # Import and run app
    sys.path.insert(0, os.path.dirname(__file__))
    from backend.app import app
    
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)

if __name__ == '__main__':
    try:
        run_server()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)