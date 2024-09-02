import logging
from concurrent import futures
import grpc
import text_reader_pb2
import text_reader_pb2_grpc

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class TextReaderService(text_reader_pb2_grpc.TextReaderServiceServicer):
    def ReadText(self, request, context):
        logging.info("Received request to read text from file.")
        try:
            with open('/app/pg74277.txt', 'r') as file:
                text = file.read()
                logging.debug(f"Text read from file: {text[:100]}...")  # Log only the first 100 characters
            return text_reader_pb2.TextReadResponse(text=text)
        except Exception as e:
            logging.error(f"Failed to read text from file: {e}")
            context.set_details(f"Failed to read text: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return text_reader_pb2.TextReadResponse(text="")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    text_reader_pb2_grpc.add_TextReaderServiceServicer_to_server(TextReaderService(), server)
    server.add_insecure_port('[::]:50051')
    logging.info("TextReaderService is starting on port 50051.")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()


