from flask import Flask, jsonify
import logging
import os
import random
import time

app = Flask(__name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

console_handler_info = logging.StreamHandler()
console_handler_info.setLevel(logging.INFO)

console_handler_error = logging.StreamHandler()
console_handler_error.setLevel(logging.ERROR)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler_info.setFormatter(formatter)
console_handler_error.setFormatter(formatter)

logger.addHandler(console_handler_info)
logger.addHandler(console_handler_error)

failure_count = {"count": 0}  # Глобальный счетчик

@app.route('/')
def index():
    logger.info("Endpoint / was hit")
    return "Shillo"

@app.route('/longtask')
def long_task():
    logger.info("Long task started!")
    time.sleep(5)
    logger.info("Long task ended!")
    return "Long task completed!"

@app.route('/fail')
def fail():
    if random.choice([True, False]):
        logger.error("Simulating a failure!")
        return "Component failed", 500
    else:
        return "Component succeeded"

@app.route('/crash5', methods=['POST'])
def crash5():
    """Роняет приложение ровно 5 раз"""
    if failure_count["count"] < 5:
        failure_count["count"] += 1
        logger.error(f"Crashing the app! Attempt {failure_count['count']}/5")
        os._exit(1)  # Роняет приложение
    else:
        return jsonify({"message": "App has already crashed 5 times"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
