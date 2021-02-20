from background_task import background
from background_task.models import Task
from datetime import datetime

from findyourngo.trustworthiness_calculator.TWUpdater import TWUpdater
from findyourngo.restapi.controllers.views import clearBackgroundTasks

today_date = datetime.today()
today_midnight = today_date.replace(hour=00, minute=00, second=1)


def start_background_tasks():
    clearBackgroundTasks('')  # delete all background tasks from db to ensure them running only once
    run_tw_update(repeat=3600, repeat_until=None)  # hourly update
    store_daily_tw(repeat=Task.DAILY)


@background(schedule=300)
def run_tw_update():
    print('Recalculate TW and PageRank')
    TWUpdater().update()
    print('TW and PageRank recalculated')


@background(schedule=today_midnight)
def store_daily_tw():
    print('Store daily TW')
    TWUpdater().store()
    print('Daily TW stored')


# If the database isn't migrated, this will lead to a chain of errors
try:
    start_background_tasks()
except Exception as e:
    print(e)
