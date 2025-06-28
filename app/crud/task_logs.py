from app.db.mongodb import sync_db_task_logs


def insert_task_log(task_log):
    result = sync_db_task_logs.async_events.insert_one(task_log)
    return str(result.inserted_id)

def insert_void_shipping_log(void_shipping_log):
    result = sync_db_task_logs.void_shipping_logs.insert_one(void_shipping_log)
    return str(result.inserted_id)