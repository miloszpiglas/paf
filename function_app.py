import logging
import os

import azure.functions as func

from datetime import datetime

from azure.data.tables import TableServiceClient, UpdateMode

app = func.FunctionApp()

# handler is executed every two minutes
# timer: TimerRequest - object of type https://learn.microsoft.com/en-us/python/api/azure-functions/azure.functions.timerrequest
@app.function_name(name="handle")
@app.schedule(schedule="0 */2 * * * *",
              arg_name="timer",
              run_on_startup=True)
def handle(timer):
    now = datetime.now().isoformat()
    if timer.past_due:
        logging.info('The timer is past due!')
    logging.info('Python timer trigger function ran at %s', now)

    connection_str = os.environ.get("connection_string")
    table_name = os.environ.get("table_name")

    logging.info("Saving data to table {}".format(table_name))

    storage_cli = TableServiceClient.from_connection_string(connection_str)
    table_cli = storage_cli.get_table_client(table_name)
    pk = os.environ.get("function_name")

    logging.info("Read function {}".format(pk))

    entity = {
        "PartitionKey": pk,
        "RowKey": "execution",
        "Count": 0
    }
    try:
        saved = table_cli.get_entity(pk, "execution")
        logging.info("Execution entity {}".format(entity))
        entity["Count"] = saved.get("Count", 0) + 1
        
    except Exception as e:
        logging.error("Reading entity error {}".format(e))

    logging.info("Upsert entity {}".format(entity))
    table_cli.upsert_entity(entity)

    
    
    
