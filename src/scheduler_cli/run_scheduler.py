from scheduler import (
    CombinedConfig,
    Scheduler,
    load_config_from_file,
    
)
from scheduler.writers import JSONWriter, CSVWriter

def run_using_config(usr_config):
    # Create scheduler
    scheduler = Scheduler(usr_config)
    scheduleList = []

    # Prints schedules
    for schedule in scheduler.get_models():

        #adds to a list to not repeat calling get_models() if saved
        scheduleList.append(schedule)

        print("Schedule:")
        for course in schedule:
            print(f"{course.as_csv()}")
    return scheduleList

#write a schedule in json format to schedules folder
def write_as_json(slist, name):
    try:
        #make new file 
        path = 'data/' + name + '.json'
        file = open(path, 'w')
        #writing for json
        with JSONWriter(path) as writer:
            for schedule in slist:
                writer.add_schedule(schedule)
        file.close()
        print("Write Complete")
    except:
        #error 
        print('An error has occured.')

#write a schedule in json format to schedules folder
def write_as_csv(slist, name):
    try:
        #make new file 
        path = 'data/' + name + '.csv'
        file = open(path, 'w')
        #writing for csv
        with CSVWriter(path) as writer:
            for schedule in slist:
                writer.add_schedule(schedule)
        file.close()
        print("Write Complete")
    except:
        #error 
        print('An error has occured.')
