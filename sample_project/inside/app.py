from flask import Flask, request, jsonify
from test_utils import compute_stuff
from test_folder.test_1 import fast_function
app = Flask(__name__)

@app.route('/test/<int:id>', methods=['POST'])
def test_endpoint(id):
    # Path parameter
    path_id = id

    # Query parameters
    query_params = request.args.to_dict()

    # JSON body
    try:
        json_body = request.get_json() or {}
    except:
        json_body = {}

    # Headers
    headers = dict(request.headers)

    # Simulate a function you want to profile
    result = dummy_processing(path_id, query_params, json_body)
    compute_stuff()
    fast_function()
    return jsonify({
        "path_id": path_id,
        "query_params": query_params,
        "json_body": json_body,
        "headers": headers,
        "processed_result": result
    })


def dummy_processing(id, query, body):
    # Simulate CPU/memory work
    total = sum([id * i for i in range(10000)])
    return {"total": total, "status": "processed"}


if __name__ == "__main__":
    app.run(debug=True)
