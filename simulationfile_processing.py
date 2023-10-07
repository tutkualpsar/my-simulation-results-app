import xml.etree.ElementTree as ET
import pandas as pd

def parse_simulation_xml(xml_file_path):
    with open(xml_file_path, "r") as simulation_contents:
        uploaded_sim_file = simulation_contents.read()

        simulation_data = []
    
    if uploaded_sim_file:
        root = ET.fromstring(uploaded_sim_file)

        simulation_config = root.find('.//{http://bsim.hpi.uni-potsdam.de/scylla/simModel}simulationConfiguration')

        simulation_data.append({
            'processInstance': int(simulation_config.get('processInstances')),
            'startDateTime': simulation_config.get('startDateTime'),
            'randomSeed': int(simulation_config.get('randomSeed'))
        })

        for event in root.findall('.//{http://bsim.hpi.uni-potsdam.de/scylla/simModel}startEvent'):
            arrival_rate = event.find('.//{http://bsim.hpi.uni-potsdam.de/scylla/simModel}arrivalRate/{http://bsim.hpi.uni-potsdam.de/scylla/simModel}exponentialDistribution/{http://bsim.hpi.uni-potsdam.de/scylla/simModel}mean').text
            simulation_data.append({
                'Task': 'Start Event',
                'DistributionType': 'Exponential',
                'Mean': float(arrival_rate)
            })

        for task in root.findall('.//{http://bsim.hpi.uni-potsdam.de/scylla/simModel}Task'):
            task_name = task.get('name')
            duration = task.find('.//{http://bsim.hpi.uni-potsdam.de/scylla/simModel}duration')
            if duration is not None:
                distribution_type = duration[0].tag.split('}')[-1]

                # Extract distribution parameters based on distribution type
                distribution_params = {}
                if distribution_type == 'exponentialDistribution':
                    mean_element = duration.find('.//{http://bsim.hpi.uni-potsdam.de/scylla/simModel}mean')
                    distribution_params['Mean'] = float(mean_element.text) if mean_element is not None else None
                elif distribution_type == 'uniformDistribution':
                    lower_element = duration.find('.//{http://bsim.hpi.uni-potsdam.de/scylla/simModel}lower')
                    upper_element = duration.find('.//{http://bsim.hpi.uni-potsdam.de/scylla/simModel}upper')
                    distribution_params['Lower'] = float(lower_element.text) if lower_element is not None else None
                    distribution_params['Upper'] = float(upper_element.text) if upper_element is not None else None

                simulation_data.append({
                    'Task': task_name,
                    'DistributionType': distribution_type,
                    **distribution_params
                })
            else:
                simulation_data.append({
                    'Task': task_name,
                    'DistributionType': None,
                    'Mean': None,
                    'Lower': None,
                    'Upper': None
                })

        # Create a DataFrame for process data
        simulation_df = pd.DataFrame(simulation_data)
        return simulation_df
    else:
        return None