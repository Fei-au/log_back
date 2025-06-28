import grpc
import logging
from ..generated.log import void_shipping_log_pb2
from ..generated.log import void_shipping_log_pb2_grpc
import json
from google.protobuf.json_format import MessageToDict
from app.crud.task_logs import insert_void_shipping_log


logger = logging.getLogger(__name__)

class LogVoidShippingService(void_shipping_log_pb2_grpc.LogVoidShippingService):
    def __init__(self):
        super().__init__()
        
    def WriteLog(self, request, context):
        try:
            result = insert_void_shipping_log(MessageToDict(request))
            return void_shipping_log_pb2.LogVoidShippingResponse(
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
            return void_shipping_log_pb2.LogVoidShippingResponse(
                status="error",
                message=str(e),
                data=json.dumps({})
            )