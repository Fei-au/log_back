import grpc
import logging
from ..generated.log import common_async_log_pb2
from ..generated.log import common_async_log_pb2_grpc
import json
from google.protobuf.json_format import MessageToDict
from app.crud.task_logs import insert_task_log


logger = logging.getLogger(__name__)

class LogAsyncTaskServiceServicer(common_async_log_pb2_grpc.LogAsyncTaskServiceServicer):
    def __init__(self):
        super().__init__()
        
    def WriteLog(self, request, context):
        try:
            result = insert_task_log(MessageToDict(request))
            return common_async_log_pb2.LogAsyncTaskResponse(
                status="success",
                message="Log received",
                data=json.dumps({
                    "inserted_id": result
                })
            )
        except Exception as e:
            logger.error(f"Error processing log: {e}")
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return common_async_log_pb2.LogAsyncTaskResponse(
                status="error",
                message=str(e),
                data=json.dumps({})
            )