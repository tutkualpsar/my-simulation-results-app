import xml.etree.ElementTree as ET
import pandas as pd

def process_simulation_output(xml_file):
    with open(xml_file, "r") as xml_contents:
        uploaded_xml_file = xml_contents.read()

    # Check if a file was uploaded
    if uploaded_xml_file is not None:
        # Parse the XML content from the string
        root = ET.fromstring(uploaded_xml_file)

        time_unit = root.find(".//configuration/time_unit").text

        process_data = []

        for process in root.findall(".//process"):
            process_id = process.find("id").text

            # Extract cost and time data as floats
            cost_min = float(process.find(".//cost/min").text)
            cost_max = float(process.find(".//cost/max").text)
            cost_median = float(process.find(".//cost/median").text)
            cost_Q1 = float(process.find(".//cost/Q1").text)
            cost_Q3 = float(process.find(".//cost/Q3").text)
            cost_avg = float(process.find(".//cost/avg").text)
            cost_total = float(process.find(".//cost/total").text)

            time_flow_min = float(process.find(".//time/flow_time/min").text)
            time_flow_max = float(process.find(".//time/flow_time/max").text)
            time_flow_median = float(process.find(".//time/flow_time/median").text)
            time_flow_Q1 = float(process.find(".//time/flow_time/Q1").text)
            time_flow_Q3 = float(process.find(".//time/flow_time/Q3").text)
            time_flow_avg = float(process.find(".//time/flow_time/avg").text)
            time_flow_total = float(process.find(".//time/flow_time/total").text)

            time_effective_min = float(process.find(".//time/effective/min").text)
            time_effective_max = float(process.find(".//time/effective/max").text)
            time_effective_median = float(process.find(".//time/effective/median").text)
            time_effective_Q1 = float(process.find(".//time/effective/Q1").text)
            time_effective_Q3 = float(process.find(".//time/effective/Q3").text)
            time_effective_avg = float(process.find(".//time/effective/avg").text)
            time_effective_total = float(process.find(".//time/effective/total").text)

            time_waiting_min = float(process.find(".//time/waiting/min").text)
            time_waiting_max = float(process.find(".//time/waiting/max").text)
            time_waiting_median = float(process.find(".//time/waiting/median").text)
            time_waiting_Q1 = float(process.find(".//time/waiting/Q1").text)
            time_waiting_Q3 = float(process.find(".//time/waiting/Q3").text)
            time_waiting_avg = float(process.find(".//time/waiting/avg").text)
            time_waiting_total = float(process.find(".//time/waiting/total").text)

            time_off_timetable_min = float(process.find(".//time/off_timetable/min").text)
            time_off_timetable_max = float(process.find(".//time/off_timetable/max").text)
            time_off_timetable_median = float(process.find(".//time/off_timetable/median").text)
            time_off_timetable_Q1 = float(process.find(".//time/off_timetable/Q1").text)
            time_off_timetable_Q3 = float(process.find(".//time/off_timetable/Q3").text)
            time_off_timetable_avg = float(process.find(".//time/off_timetable/avg").text)
            time_off_timetable_total = float(process.find(".//time/off_timetable/total").text)

            process_data.append({
                "Process ID": process_id,
                "Cost Min": cost_min,
                "Cost Max": cost_max,
                "Cost Median": cost_median,
                "Cost Q1": cost_Q1,
                "Cost Q3": cost_Q3,
                "Cost Avg": cost_avg,
                "Cost Total": cost_total,
                "Time Flow Min": time_flow_min,
                "Time Flow Max": time_flow_max,
                "Time Flow Median": time_flow_median,
                "Time Flow Q1": time_flow_Q1,
                "Time Flow Q3": time_flow_Q3,
                "Time Flow Avg": time_flow_avg,
                "Time Flow Total": time_flow_total,
                "Time Effective Min": time_effective_min,
                "Time Effective Max": time_effective_max,
                "Time Effective Median": time_effective_median,
                "Time Effective Q1": time_effective_Q1,
                "Time Effective Q3": time_effective_Q3,
                "Time Effective Avg": time_effective_avg,
                "Time Effective Total": time_effective_total,
                "Time Waiting Min": time_waiting_min,
                "Time Waiting Max": time_waiting_max,
                "Time Waiting Median": time_waiting_median,
                "Time Waiting Q1": time_waiting_Q1,
                "Time Waiting Q3": time_waiting_Q3,
                "Time Waiting Avg": time_waiting_avg,
                "Time Waiting Total": time_waiting_total,
                "Time Off Timetable Min": time_off_timetable_min,
                "Time Off Timetable Max": time_off_timetable_max,
                "Time Off Timetable Median": time_off_timetable_median,
                "Time Off Timetable Q1": time_off_timetable_Q1,
                "Time Off Timetable Q3": time_off_timetable_Q3,
                "Time Off Timetable Avg": time_off_timetable_avg,
                "Time Off Timetable Total": time_off_timetable_total,
            })

        # Create a DataFrame for process data
        process_df = pd.DataFrame(process_data)

        resource_data = []

        for resource in root.findall(".//resource"):
            resource_type = resource.find("type").text

            # Extract cost and time data as floats
            cost = float(resource.find(".//cost/total").text)
            time_in_use = float(resource.find(".//time/in_use/total").text)
            time_available = float(resource.find(".//time/available/total").text)
            time_workload = float(resource.find(".//time/workload/total").text)

            resource_data.append({
                "Resource Type": resource_type,
                "Cost": cost,
                "Time In Use": time_in_use,
                "Time Available": time_available,
                "Time Workload": time_workload,
            })

        # Create a DataFrame for resource data
        resource_df = pd.DataFrame(resource_data)
        
        activity_data = []
        for activity in root.findall(".//activity"):
            activity_id = int(activity.find("id").text)
            activity_name = activity.find("name").text

            # Extract cost and time data as floats
            cost_min = float(activity.find(".//cost/min").text)
            cost_max = float(activity.find(".//cost/max").text)
            cost_median = float(activity.find(".//cost/median").text)
            cost_Q1 = float(activity.find(".//cost/Q1").text)
            cost_Q3 = float(activity.find(".//cost/Q3").text)
            cost_avg = float(activity.find(".//cost/avg").text)
            cost_total = float(activity.find(".//cost/total").text)

            time_duration_min = float(activity.find(".//time/duration/min").text)
            time_duration_max = float(activity.find(".//time/duration/max").text)
            time_duration_median = float(activity.find(".//time/duration/median").text)
            time_duration_Q1 = float(activity.find(".//time/duration/Q1").text)
            time_duration_Q3 = float(activity.find(".//time/duration/Q3").text)
            time_duration_avg = float(activity.find(".//time/duration/avg").text)
            time_duration_total = float(activity.find(".//time/duration/total").text)

            time_waiting_min = float(activity.find(".//time/waiting/min").text)
            time_waiting_max = float(activity.find(".//time/waiting/max").text)
            time_waiting_median = float(activity.find(".//time/waiting/median").text)
            time_waiting_Q1 = float(activity.find(".//time/waiting/Q1").text)
            time_waiting_Q3 = float(activity.find(".//time/waiting/Q3").text)
            time_waiting_avg = float(activity.find(".//time/waiting/avg").text)
            time_waiting_total = float(activity.find(".//time/waiting/total").text)

            time_resources_idle_min = float(activity.find(".//time/resources_idle/min").text)
            time_resources_idle_max = float(activity.find(".//time/resources_idle/max").text)
            time_resources_idle_median = float(activity.find(".//time/resources_idle/median").text)
            time_resources_idle_Q1 = float(activity.find(".//time/resources_idle/Q1").text)
            time_resources_idle_Q3 = float(activity.find(".//time/resources_idle/Q3").text)
            time_resources_idle_avg = float(activity.find(".//time/resources_idle/avg").text)
            time_resources_idle_total = float(activity.find(".//time/resources_idle/total").text)

            activity_data.append({
                "Activity ID": activity_id,
                "Activity Name": activity_name,
                "Cost Min": cost_min,
                "Cost Max": cost_max,
                "Cost Median": cost_median,
                "Cost Q1": cost_Q1,
                "Cost Q3": cost_Q3,
                "Cost Avg": cost_avg,
                "Cost Total": cost_total,
                "Time Duration Min": time_duration_min,
                "Time Duration Max": time_duration_max,
                "Time Duration Median": time_duration_median,
                "Time Duration Q1": time_duration_Q1,
                "Time Duration Q3": time_duration_Q3,
                "Time Duration Avg": time_duration_avg,
                "Time Duration Total": time_duration_total,
                "Time Waiting Min": time_waiting_min,
                "Time Waiting Max": time_waiting_max,
                "Time Waiting Median": time_waiting_median,
                "Time Waiting Q1": time_waiting_Q1,
                "Time Waiting Q3": time_waiting_Q3,
                "Time Waiting Avg": time_waiting_avg,
                "Time Waiting Total": time_waiting_total,
                "Time Resources Idle Min": time_resources_idle_min,
                "Time Resources Idle Max": time_resources_idle_max,
                "Time Resources Idle Median": time_resources_idle_median,
                "Time Resources Idle Q1": time_resources_idle_Q1,
                "Time Resources Idle Q3": time_resources_idle_Q3,
                "Time Resources Idle Avg": time_resources_idle_avg,
                "Time Resources Idle Total": time_resources_idle_total,
            })

        # Create a DataFrame for activity data
        activity_df = pd.DataFrame(activity_data)


# To create dataframe for activity instance:
        instance_data = []
        activity_ids = []
        activity_names = []
        instance_numbers = []
        costs = []
        effective_times = []
        waiting_times = []
        resource_idles = []

# Iterate over each "activity" element
        for activity in root.findall(".//activity"):
            activity_id = activity.find("id").text
            activity_name = activity.find("name").text

            # Iterate over each "instance" element
            for i, instance in enumerate(activity.findall(".//instance")):
                instance_number = i + 1  # Instance number starts from 1
                cost = float(instance.find("cost").text)
                effective_time = float(instance.find(".//effective").text)
                waiting_time = float(instance.find(".//waiting").text)
                resource_idle = float(instance.find(".//resources_idle").text)

                # Append data to lists
                activity_ids.append(activity_id)
                activity_names.append(activity_name)
                instance_numbers.append(instance_number)
                costs.append(cost)
                effective_times.append(effective_time)
                waiting_times.append(waiting_time)
                resource_idles.append(resource_idle)

        # Create the DataFrame
        instance_data = {
            'Activity_Id': activity_ids,
            'Activity_Name': activity_names,
            'Instance_No': instance_numbers,
            'Cost': costs,
            'Effective_Time': effective_times,
            'Waiting_Time': waiting_times,
            'Resource_Idle': resource_idles
        }

        instance_df = pd.DataFrame(instance_data)


        # Calculate the total duration
        instance_df['Total_Duration'] = (
        instance_df['Effective_Time'] +
        instance_df['Waiting_Time'] +
        instance_df['Resource_Idle']
        )

        # Create a new DataFrame for plotting
        plot_data = instance_df.groupby(['Instance_No', 'Activity_Name'])['Total_Duration'].sum().unstack()

        # Sort the DataFrame by the total duration of each instance
        plot_data['Total'] = plot_data.sum(axis=1)
        plot_data = plot_data.sort_values(by='Total')

        # Drop the 'Total' column as it was only used for sorting
        plot_data = plot_data.drop('Total', axis=1)

        # Sort instances on the x-axis
        plot_data = plot_data.sort_index(axis=0)

        # Find instances only under <instances>
        instances = root.find('.//process/instances')

        # Initialize lists to store data
        instance_nos = []
        pi_costs = []
        pi_durations = []
        pi_effectives = []
        pi_waitings = []
        pi_off_times = []

        # Extract data from instances
        for idx, instance in enumerate(instances.findall('.//instance')):
            instance_nos.append(idx + 1)
            pi_costs.append(float(instance.find('costs').text))
            time = instance.find('time')
            pi_durations.append(int(time.find('duration').text))
            pi_effectives.append(int(time.find('effective').text))
            pi_waitings.append(int(time.find('waiting').text))
            pi_off_times.append(int(time.find('offTime').text))

        # Create DataFrame
        pi_data = {
            'Instance No': instance_nos,
            'Cost': pi_costs,
            'Duration': pi_durations,
            'Effective': pi_effectives,
            'Waiting': pi_waitings,
            'OffTime': pi_off_times
        }

        process_instances_df = pd.DataFrame(pi_data)



        return process_df, resource_df, activity_df, instance_df, process_instances_df, plot_data, time_unit