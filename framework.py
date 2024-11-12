import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional, Tuple


class ScenarioFramework:
    """Sets up a framework for using scenarios in a simulation model."""

    def __init__(self, scenario_folder_path: str, runs_folder_path: str):
        """Initialize with paths for scenarios and runs folders."""
        self.scenarios_folder_path = Path(scenario_folder_path)
        self.simulation_folder_path = Path(runs_folder_path)
        self.scenario_path = None
        self.simulation_run_path = None

    def pick_scenario(self, scenario_name: Optional[str] = None) -> Optional[Tuple[Path, Path, Path]]:
        """
        Allows selection of a scenario folder, either by name or by user input.

        Parameters:
        - scenario_name (str, optional): Direct name of the scenario folder to select.

        Returns:
        - Optional[Tuple[Path, Path, Path]]: Paths to the selected scenario, input data, and output data folders,
          or None if selection fails.
        """
        if not self.scenarios_folder_path.exists():
            print(f"Scenarios folder '{self.scenarios_folder_path}' does not exist.")
            return None

        # Handle direct selection by scenario name
        if scenario_name:
            selected_scenario_path = self.scenarios_folder_path / scenario_name
            if selected_scenario_path.is_dir():
                self.scenario_path = selected_scenario_path
                print(f"'{scenario_name}' scenario selected.")
                return self._setup_simulation_folders()
            else:
                print(f"Scenario '{scenario_name}' does not exist.")
                return None

        # Prompt the user for scenario selection if no name was given
        scenarios = self._list_scenarios()
        if not scenarios:
            print("No scenarios found in the scenario folder.")
            return None

        scenario_index = self._prompt_scenario_selection(scenarios)
        if scenario_index is None:
            return None

        self.scenario_path = self.scenarios_folder_path / scenarios[scenario_index]
        print(f"'{scenarios[scenario_index]}' scenario selected.")
        return self._setup_simulation_folders()

    def _setup_simulation_folders(self) -> Tuple[Path, Path, Path]:
        """
        Sets up a new run directory, copying input files and creating an output directory.

        Returns:
            Tuple[Path, Path, Path]: Paths to scenario, input, and output directories.
        """
        # Ensure base simulation folder exists and create run directory
        self.simulation_run_path = self._create_run_directory()
        input_data_path = self._copy_input_files()
        output_data_path = self._create_output_directory()
        return self.scenario_path, input_data_path, output_data_path

    def _create_run_directory(self) -> Path:
        """Creates a unique run directory with a timestamp."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H-%M-%S')
        run_folder_path = self.simulation_folder_path / f'{timestamp}_{self.scenario_path.name}'
        run_folder_path.mkdir(parents=True, exist_ok=True)
        return run_folder_path

    def _copy_input_files(self) -> Path:
        """Copies all data from scenario folder to the 'Input data' folder in the run directory."""
        scenario_input_path = self.scenario_path
        new_input_path = self.simulation_run_path / 'Input data'

        shutil.copytree(scenario_input_path, new_input_path)

        if not scenario_input_path.is_dir():
            raise FileNotFoundError(f"Expected input directory '{scenario_input_path}' not found.")

        return new_input_path

    def _create_output_directory(self) -> Path:
        """Creates an 'Output data' directory in the run directory."""
        output_path = self.simulation_run_path / 'Output data'
        output_path.mkdir()
        return output_path

    def _list_scenarios(self) -> list:
        """Returns a list of scenario directories available in the scenarios folder."""
        return [d.name for d in self.scenarios_folder_path.iterdir() if d.is_dir()]

    @staticmethod
    def _prompt_scenario_selection(scenarios: list) -> Optional[int]:
        """Prompts the user to select a scenario from the available options."""
        print("Available scenarios:")
        for idx, scenario in enumerate(scenarios):
            print(f"{idx}: {scenario}")

        # Keep prompting until a valid selection is made
        while True:
            try:
                choice = int(input(f"Select a scenario by number (0-{len(scenarios) - 1}): "))
                if 0 <= choice < len(scenarios):
                    return choice
                print("Invalid selection. Please try again.")
            except ValueError:
                print("Please enter a valid number.")
