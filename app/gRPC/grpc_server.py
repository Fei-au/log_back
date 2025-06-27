import grpc
from concurrent import futures
import logging
from .services.log_service import log_service_pb2_grpc
from pathlib import Path
import os
from .services.log_service.log_service import LogAsyncTaskServiceServicer


BASE_DIR = Path(__file__).resolve().parent.parent.parent
logging.basicConfig(
        level=logging.INFO,
        filename=os.path.join(BASE_DIR, "log_back_gRPC.log"),
        filemode="a",
        format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
logger = logging.getLogger(__name__)

def serve():
    port = "50051"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    log_service_pb2_grpc.add_LogAsyncTaskServiceServicer_to_server(LogAsyncTaskServiceServicer(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    logger.info("gRPC server started on port 50051.")
    print("gRPC server started on port 50051.")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
