from datetime import datetime
import logging
import azure.functions as func

app = func.FunctionApp()

# handler is executed every two minutes
# timer: TimerRequest - object of type https://learn.microsoft.com/en-us/python/api/azure-functions/azure.functions.timerrequest
@app.function_name(name="handle")
@app.schedule(schedule="0 */2 * * * *",
              arg_name="timer",
              run_on_startup=True)
def handle(timer):
    now = datetime.datetime.now().isoformat()
    if timer.past_due:
        logging.info('The timer is past due!')
    logging.info('Python timer trigger function ran at %s', now)
