import logging
from concurrent import futures
import grpc
import re
import analysis_pb2
import analysis_pb2_grpc
import text_reader_pb2_grpc
import text_reader_pb2

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class AnalysisService(analysis_pb2_grpc.AnalysisServiceServicer):
    def AnalyzeText(self, request, context):
        logging.info("Received text for analysis.")
        try:
            # Assume `text_reader_service` will provide the full text
            with grpc.insecure_channel('text_reader_service:50051') as channel:
                text_stub = text_reader_pb2_grpc.TextReaderServiceStub(channel)
                text_response = text_stub.ReadText(text_reader_pb2.TextReadRequest())
                text = text_response.text
                logging.debug(f"Text received from TextReaderService: {text[:100]}...")  # Log first 100 characters

            words = re.findall(r'\b\w+\b', text)
            word_count = len(words)
            sentence_count = len(re.split(r'[.!?]', text))
            avg_word_length = sum(len(word) for word in words) / word_count if word_count > 0 else 0
            avg_sentence_length = sum(len(sentence.split()) for sentence in re.split(r'[.!?]', text)) / sentence_count if sentence_count > 0 else 0

            word_frequencies = {word: text.lower().split().count(word.lower()) for word in request.archaic_words}
            logging.debug(f"Analysis complete: Avg Word Length: {avg_word_length}, Avg Sentence Length: {avg_sentence_length}, Frequencies: {word_frequencies}")

            return analysis_pb2.TextAnalysisResponse(
                avg_word_length=avg_word_length,
                avg_sentence_length=avg_sentence_length,
                word_frequencies=word_frequencies
            )
        except Exception as e:
            logging.error(f"Failed to analyze text: {e}")
            context.set_details(f"Failed to analyze text: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            return analysis_pb2.TextAnalysisResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    analysis_pb2_grpc.add_AnalysisServiceServicer_to_server(AnalysisService(), server)
    server.add_insecure_port('[::]:50052')
    logging.info("AnalysisService is starting on port 50052.")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
