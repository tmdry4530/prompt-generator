from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/health')
def health():
    return jsonify({"status": "ok", "message": "Test server is working"})

@app.route('/test')
def test():
    return "Test endpoint working"

@app.route('/')
def root():
    return "Root endpoint working"

if __name__ == '__main__':
    print("Starting test server on port 5001...")
    app.run(host='0.0.0.0', port=5001, debug=True) 