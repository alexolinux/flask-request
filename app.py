from flask import Flask, render_template, jsonify
import time

app = Flask(__name__)

request_count = 0

@app.route('/')
def index():
    global request_count
    request_count += 1

    # Simulate some processing time (you may adjust this based on your API's typical processing time)
    time.sleep(0.1)

    # Check health status based on response time
    health_status = "OK" if response_time() < 0.2 else "Unhealthy"

    return render_template('index.html', count=request_count, health_status=health_status)

@app.route('/health')
def health_check():
    # Check health status based on response time
    health_status = "OK" if response_time() < 0.2 else "Unhealthy"
    return jsonify({"status": health_status})

def response_time():
    # Simulate some processing time (you may adjust this based on your API's typical processing time)
    start_time = time.time()
    time.sleep(0.1)
    end_time = time.time()
    return end_time - start_time

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

