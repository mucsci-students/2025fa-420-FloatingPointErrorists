# FloatingPointErrorists

## Scheduler Config Editor (SCE):

Program for managing faculty, courses, rooms, and labs. It also interfaces with the scheduler to generate, display, and save schedules.

## Getting Started:

1. Ensure you have Python 3.13 or higher installed. To check your version, run:
```python --version```
2. Check if git is installed by running: 
```git --version```. If it is not installed, download it from: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
3. Make sure to have uv installed:
https://docs.astral.sh/uv/getting-started/installation/. You can check your version with:
```uv --version```

### Installing

* Clone the repository using:
```git clone https://github.com/mucsci-students/2025fa-420-FloatingPointErrorists.git```, and navigate to the project directory.
* Install dependencies and create a virtual environment by running:
```uv sync```
* Activate the virtual environment:
   - On Windows:
   ```.\.venv\Scripts\activate```
   - On macOS/Linux:
   ```source .venv/bin/activate```
* If you want to deactivate the virtual environment later, simply run:
```deactivate```
* To use AI features, set up your OpenAI API key as an environment variable:
   - Create a `.env` from `.env.example` and add your OpenAI API key to it.
* To install development packages, run:
```uv pip install -e ".[dev]"```
* You can run tests using:
```pytest```
* You must have dev packages installed to run tests.

### Executing + Using the Program In CLI Mode

* To run the program in gui mode, use the command:
```sce``` (scheduler-config-editor)
* To run it in cli mode, add an argument:
```sce --cli```
* To load a specific configuration file, use:
```load-config <path-to-file>```
* To create a new configuration file, use:
```load-config <config-name>```. This will create a new file <config-name>.json in the configs directory of this project.
* Once a configuration file is loaded, you can use the following commands:
    * `help` to bring up a list of commands.
    * `exit`, `quit` or ctrl+c to exit the program.
    * `chat` to enter chat mode with the AI assistant who can modify the configuration for you.
    * `show` to display the current configuration.
    * `save` to save the current configuration to the loaded file.
    * `clear` to clear the terminal screen.
    * `run` to run the scheduler on the current configuration. (Generated schedules will be saved in the `schedules` directory.)
    * `faculty` to manage faculty members in the faculty shell.
    * `rooms` to manage rooms in the rooms shell.
    * `labs` to manage labs in the labs shell.
    * `courses` to manage courses in the courses shell.
    * Within the `faculty`, `rooms`, `labs`, and `courses` shells, you can use:
        * `add` to add a new item.
        * `delete` to remove an item.
        * `modify` to update an existing item.
        * `exit`, `quit` or ctrl+c to return to the main shell.
* To import generated schedules from a json or csv file, use:
```load-schedules <path-to-file>``` or ```load-schedules <schedule-name>``` if it is in the schedules directory.
* Once a set of schedules is loaded (either by importing or generating), you can invoke the schedule viewer with:
```view-schedules```. Inside the viewer, you can use:
    * ```show``` to display and navigate between the schedules.
    * ```show-faculty``` to display schedules for each faculty member.
    * ```show-room``` to display schedules for each room.

## Design Patterns:

* Model-View-Controller:
    * Keep files for separate features distinguished and also for organization. This allows us to keep separation of concerns present in our code.
    * Files: All the files in the labeled folders under the src/scheduler_config_editor directory
* Adapter: 
    * The schedules are either loaded as a JSON or CSV, but they are operated on as CourseInstanceJSON objects. So we have a class that will convert the schedules into lists of CourseInstanceJSON so they can be presented in a readable format.
    * File: scheduler_handler.py
* Command:
    * We needed to queue up multiple schedules to be created
    * File: generator_controller.py
* Memento:
    * When we open up the editor, we don't want the changes to be committed until we explicitly save them. So when we operate on the configuration, we do so on a copy of the original configuration. When we save, we overwrite the original configuration with the modified copy.
    * File: json.py
 
* Mediator:
    * An essential part to MVC is the mediator design pattern. It lets us enforce separation of concerns. We don't want, for example, the faculty_editor_gui.py to have the logic to edit the json file directly, so it'll communicate with faculty_controller.py, the mediator, which will tell the model to do what it needs to do in order to make those modifications. All controller files, by nature, are examples of a Mediator design pattern. 
    * File: all files under the src/scheduler_config_editor/controller directory

## Authors:

* Andrew Elko
* Ian Oister
* Norah Ellis
* Paige Althoff
* Tommy Nguyen
* Valentino Pirocchi
* Zac Tawfick

⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣤⣾⠿⣻⣿⠟⠁⠀⠀⠀⠀⣠⣾⡆⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⡿⠟⢉⣴⣾⠟⠁⠀⠀⠀⢀⣴⡿⠋⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣾⠟⠉⢀⣴⣿⠟⠁⠀⠀⠀⢀⣴⡿⠋⠀⣸⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⡿⠟⠁⠀⣠⣾⠟⠁⠀⠀⠀⢀⣴⡿⠋⠀⠀⢠⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⡿⠋⠀⠀⢀⣾⡿⠁⠀⠀⠀⢀⣴⡿⠋⠀⠀⠀⢀⣾⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⠟⠁⠀⠀⣰⣿⠏⠀⠀⠀⢀⣴⡿⠋⠀⠀⠀⠀⠀⣼⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⡿⠃⠀⠀⠀⣴⡿⠁⠀⠀⢀⣴⣿⠟⠁⠀⠀⠀⠀⠀⣼⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⠟⠁⠀⠀⠀⣸⡿⠁⠀⠀⣴⣿⠟⠁⠀⠀⠀⠀⠀⠀⣸⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⠏⠀⠀⠀⠀⢠⣿⠃⢀⣴⣾⠟⠁⠀⠀⠀⠀⠀⠀⠀⣼⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠏⠀⠀⠀⠀⠀⠸⣿⣶⡿⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⣼⡿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⡟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣿⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⣿⣷⡀⠀⠀⠀⣠⣴⣶⣶⠀⠀⠀⣠⣾⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣧⢻⣿⡇⠀⢀⣾⣿⣿⣿⡟⠀⣠⣾⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣮⡙⠃⠀⠈⠻⠿⠟⣋⣴⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⠿⣿⣿⣿⣿⣅⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⣿⣦⡘⠀⠀⠀⢠⣾⡿⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣶⡶⣶⡄
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣇⡀⣀⢀⣼⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣾⠏⣿⣿⢎⣷
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⡟⣸⡇⢿⣆⢻⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⡶⢟⣫⣵⡶⣶⡿⠿⠃
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⠃⣿⡇⠸⣿⡎⢻⣿⣿⣿⣶⣄⡀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⡶⢟⣫⣽⠾⠛⠉⠁⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⡿⣿⣿⠃⠀⣿⡇⠀⢻⣿⡄⠘⠿⣿⣿⣿⣿⣦⣄⠀⢀⣠⣴⡾⢟⣫⣵⠾⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⡿⢋⣼⡿⠃⠀⢸⣿⠃⠀⠀⠻⣿⣆⠀⠈⠻⣿⣷⣝⠻⣿⣿⣯⣴⠾⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣼⡿⠋⣠⣿⡿⠁⠀⠀⢸⣿⠀⠀⠀⠀⠹⣿⣧⡀⠀⠈⠙⢿⣷⣮⡻⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⡿⠁⣰⣿⠟⠀⠀⠀⠀⣿⡟⢿⠀⠀⠀⠀⠈⢿⣷⣄⠀⠀⠀⠙⢿⣿⣌⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣧⣴⣿⡟⠀⠀⠀⠀⢸⣿⠃⠀⠀⠀⠀⠀⠀⠀⠻⣿⣦⠀⠀⣠⣾⣿⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠻⣿⣤⣄⣀⠀⠀⣿⡿⠠⠀⠀⠀⠀⠀⣀⣤⣤⣿⣿⣷⣾⠿⢿⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣽⡿⠿⠿⠿⣿⣿⣶⣶⣶⣶⣶⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣴⠾⠛⠉⣀⣤⡶⠟⠛⠉⠉⢿⣿⣇⠀⠀⢹⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⡶⠟⢋⣡⣴⠶⠟⠋⠁⠀⠀⠀⠀⠀⠘⣿⣿⡀⠀⠸⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣴⠾⢛⣡⣴⠾⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⡇⠀⠀⣿⣿⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⣠⡴⣚⣭⡶⠟⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⠀⠀⢹⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⣀⣤⣶⣿⠷⠛⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⠀⠀⢸⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢀⣴⡾⠿⠛⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⡆⠀⢸⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡇⠀⢸⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠃⠀⠈⠟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀



