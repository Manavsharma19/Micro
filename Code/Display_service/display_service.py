import logging
from concurrent import futures
import grpc
import requests
from flask import Flask, render_template_string
import display_pb2
import display_pb2_grpc
import storage_pb2_grpc
import storage_pb2

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)

display_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Display Results</title>
</head>
<body>
    <h1>{{ message }}</h1>
</body>
</html>
"""

class DisplayService(display_pb2_grpc.DisplayServiceServicer):
    def GetDisplayData(self, request, context):
        logging.info("Received request to get display data.")
        try:
            with grpc.insecure_channel('storage_service:50053') as channel:  # Correct storage service channel
                stub = storage_pb2_grpc.StorageServiceStub(channel)
                data_response = stub.GetData(storage_pb2.DataRequest())
                if data_response.found:
                    logging.debug(f"Data found: {data_response.data}")
                    return display_pb2.DisplayResponse(message=data_response.data)
                else:
                    logging.info("No data found in storage.")
                    return display_pb2.DisplayResponse(message="No data found.")
        except Exception as e:
            logging.error(f"Failed to get display data: {e}")
            context.set_details(f"Failed to get display data: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return display_pb2.DisplayResponse(message="An error occurred.")

@app.route('/')
def display_data():
    logging.info("Received HTTP GET request for display data.")
    try:
        # Simulate gRPC call to display service's GetDisplayData method
        with grpc.insecure_channel('display_service:50054') as channel:
            stub = display_pb2_grpc.DisplayServiceStub(channel)
            response = stub.GetDisplayData(display_pb2.DisplayRequest())
            logging.debug(f"Response from DisplayService: {response.message}")
            return render_template_string(display_template, message=response.message)
    except Exception as e:
        logging.error(f"Failed to render display data: {e}")
        return render_template_string(display_template, message="An error occurred while displaying data.")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    display_pb2_grpc.add_DisplayServiceServicer_to_server(DisplayService(), server)
    server.add_insecure_port('[::]:50054')  # Correct port for display service
    logging.info("DisplayService is starting on port 50054.")
    server.start()
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    serve()
