from background_task import background

from findyourngo.trustworthiness_calculator.TWUpdater import TWUpdater
from findyourngo.restapi.controllers.views import clearBackgroundTasks


def start_background_tasks():
    clearBackgroundTasks('')  # delete all background tasks from db to ensure them running only once
    run_tw_update(repeat=3600, repeat_until=None)  # hourly update


@background(schedule=300)
def run_tw_update():
    print('Recalculate TW and PageRank')
    TWUpdater().update()
    print('TW and PageRank recalculated')


# If the database isn't migrated, this will lead to a chain of errors
try:
    start_background_tasks()
except Exception as e:
    print(e)
