from flask import Flask, jsonify
import os
import mysql.connector

# flask app instance
app = Flask(__name__)

DB_HOST = os.getenv('DB_HOST', 'db')
DB_USER = os.getenv('DB_USER', 'appuser')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'changeme')
DB_NAME = os.getenv('DB_NAME', 'appdb')

@app.get('/api/health')
def health():
    return jsonify(message={'status': 'ok'})

@app.get('/api/time')
def time():
    # get server time from db
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )
    cur = conn.cursor()
    cur.execute("SELECT NOW()")
    row = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(message={'time': str(row[0])})

@app.get('/api')
def index():
    """Simple endpoint that greets from DB."""
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )
    cur = conn.cursor()
    cur.execute("SELECT 'Hello from MySQL via Testi!'")
    row = cur.fetchone()
    cur.close()
    conn.close()
    return jsonify(message=row[0])

# 🧪 Test endpoint: testaa backend‑endpointeja
@app.get('/api/run-tests')
def run_tests():
    results = {}
    errors = []

    # Test /api
    try:
        with app.test_client() as client:
            r1 = client.get('/api')
            if r1.status_code == 200:
                results['api'] = "Backend toimii"
            else:
                errors.append(f"/api returned status {r1.status_code}")
    except Exception as e:
        errors.append(f"/api error: {str(e)}")

    # Test /api/time
    try:
        with app.test_client() as client:
            r2 = client.get('/api/time')
            if r2.status_code == 200:
                results['time'] = "Backend toimii"
            else:
                errors.append(f"/api/time returned status {r2.status_code}")
    except Exception as e:
        errors.append(f"/api/time error: {str(e)}")

    # Koostetaan vastaus
    if errors:
        return jsonify({
            "message": "Backend testissä virheitä",
            "errors": errors,
            **results
        }), 500

    # Jos kaikki toimii
    return jsonify({
        "message": "Backend toimii",
        **results
    })

if __name__ == '__main__':
    # Dev-only fallback
    app.run(host='0.0.0.0', port=8000, debug=True)
