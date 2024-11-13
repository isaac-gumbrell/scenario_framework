Read article for better explanation: https://medium.com/@isaacgumbrell_61100/streamline-your-modelling-workflow-small-efforts-now-big-productivity-gains-later-8b4afc47292a

The Scenario Framework Manager is designed to streamline scenario management by automatically organizing input and output data for each model run. 
The base folder has two folders: Results and Scenarios. Within Scenarios are multiple folders, one for each scenario. Each scenario folder contains input data for a single execution of the model.
        
After importing the scenario framework module, initialize a ScenarioFramework object while providing the paths of the Scenarios and Results folders as inputs.
from scenario_framework import ScenarioFramework

scenario = ScenarioFramework(scenario_folder_path='<ScenarioFolderPath>',
                             results_folder_path='<ResultsFolderPath>')

scenario_path, inputs_path, outputs_path = scenario.pick_scenario()
After initializing the ScenarioFramework object, call the pickscenario function, and assign the function's output to inputs_path and outputs_path variables. The console window will now prompt you to pick a scenario. 

C:\Users\User\miniconda3\envs\Basic\python.exe "C:\Users\User\Documents\Tests\doing_a_thing.py" 
Available scenarios:
0: Scenario_A
1: Scenario_B
2: Scenario_C
Select a scenario by number (0-2): 

Choose the scenario you wish to run by entering its corresponding number and press enter. 
You now have paths for both outputs and inputs which can be used throughout the rest of your model without worrying about overwriting data or saving results in the correct place. Both folders are contained within a parent folder representing a single execution of the model. Its name is a combination of the scenario folder's name, and timestamp of when the scenario was executed. This folder is contained within the Results folder. 
            
The Inputs folder has a fresh copy of all data in the Scenario folder, this is where you will import data from while you continue the rest of the model.
The Outputs folder is a fresh directory ready for any outputs. 
If you want to make a slight variation of a scenario, you can simply copy the scenario folder. 
