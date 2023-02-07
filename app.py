from flask import Flask, request, jsonify
import docker

app = Flask(__name__)
client = docker.from_env()


@app.route('/computation', methods=['POST'])
def handle_computation_request():
    data = request.get_json()
    # Extract the necessary information from the data
    image = data['image']
    env_vars = data['env_vars']
    input_data = data['input_data']
    if not all([image, input_data, env_vars]):
        return jsonify({'error': 'Invalid request data'}), 400
    try:
        mounts = [docker.types.Mount(source=input_data['mount_source'], target=input_data['mount_target'],
                                     type="bind")]

        container = client.containers.run(image,
                                          mounts=mounts,
                                          environment=env_vars,
                                          detach=True)
        return jsonify({'container_id': container.id})
    except Exception as e:
        # Return an error response
        expn_type = type(e).__name__.lower()
        if expn_type == "notfound":
            return jsonify('Please provide correct image name'), 400
        return jsonify({'error': str(e)}), 500


@app.route('/containers', methods=['GET'])
def get_containers_status():
    # Get a list of all running containers
    containers = client.containers.list(all=True)
    # Create a list to store the container status
    container_status = []
    # Iterate through the containers and get their status
    for container in containers:
        container_status.append({'name': container.name, 'id': container.id, 'status': container.status})
    # Return the container status
    return jsonify({'containers': container_status})


@app.route('/containers/<container_id>', methods=['DELETE'])
def stop_container(container_id):
    try:
        # Stop and remove the container
        container = client.containers.get(container_id)
        container.stop()
        container.remove()
        # Return a successful response
        return jsonify({'status': 'success'})
    except Exception as e:
        # Return an error response
        expn_type = type(e).__name__.lower()
        if expn_type == "notfound":
            return jsonify('Please provide correct container id to delete'), 400
        else:
            return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(port=8000, debug=True)