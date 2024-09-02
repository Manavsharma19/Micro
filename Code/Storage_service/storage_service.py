import logging
from concurrent import futures
import grpc
import redis
import storage_pb2
import storage_pb2_grpc
import analysis_pb2_grpc
import analysis_pb2

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class StorageService(storage_pb2_grpc.StorageServiceServicer):
    def __init__(self, archaic_words):
        self.archaic_words = archaic_words  # List of archaic words to track

        logging.info("Connecting to Redis.")
        try:
            self.redis_client = redis.Redis(host='redis', port=6379, db=0)
            logging.info("Connected to Redis.")
        except Exception as e:
            logging.error(f"Failed to connect to Redis: {e}")

    def GetData(self, request, context):
        logging.info("Received request to get data.")
        try:
            data = self.redis_client.get('analysis_data')
            if data:
                logging.debug(f"Data found in Redis: {data.decode('utf-8')}")
                return storage_pb2.DataResponse(found=True, data=data.decode('utf-8'))
            else:
                logging.info("No data found in Redis. Triggering analysis service.")
                return self.trigger_analysis_service()
        except Exception as e:
            logging.error(f"Failed to get data from Redis: {e}")
            context.set_details(f"Failed to get data: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return storage_pb2.DataResponse(found=False)

    def trigger_analysis_service(self):
        logging.info("Connecting to analysis service to retrieve new data.")
        try:
            with grpc.insecure_channel('analysis_service:50052') as channel:
                stub = analysis_pb2_grpc.AnalysisServiceStub(channel)
                response = stub.AnalyzeText(analysis_pb2.TextRequest(text="Your text to analyze here", archaic_words=self.archaic_words))
                analyzed_data = f"Avg Word Length: {response.avg_word_length}, Avg Sentence Length: {response.avg_sentence_length}, Frequencies: {response.word_frequencies}"
                logging.debug(f"Received analyzed data: {analyzed_data}")
                
                # Store the result in Redis
                self.redis_client.set('analysis_data', analyzed_data)
                logging.info("Stored analyzed data in Redis.")
                
                return storage_pb2.DataResponse(found=True, data=analyzed_data)
        except Exception as e:
            logging.error(f"Failed to connect to analysis service: {e}")
            return storage_pb2.DataResponse(found=False)

def serve():
    archaic_words = ["thou", "thee", "hast", "hath", "ye", "whilst", "wherefore", "betwixt", "hither", "thither"]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    storage_pb2_grpc.add_StorageServiceServicer_to_server(StorageService(archaic_words), server)
    server.add_insecure_port('[::]:50053')
    logging.info("StorageService is starting on port 50053.")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
