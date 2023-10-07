import xml.etree.ElementTree as ET
import pandas as pd

def process_simulation_output(xml_file):
    with open(xml_file, "r") as xml_contents:
        uploaded_xml_file = xml_contents.read()

    # Check if a file was uploaded
    if uploaded_xml_file is not None:
        # Parse the XML content from the string
        root = ET.fromstring(uploaded_xml_file)

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
            cost_min = float(resource.find(".//cost/min").text)
            cost_max = float(resource.find(".//cost/max").text)
            cost_median = float(resource.find(".//cost/median").text)
            cost_Q1 = float(resource.find(".//cost/Q1").text)
            cost_Q3 = float(resource.find(".//cost/Q3").text)
            cost_avg = float(resource.find(".//cost/avg").text)
            cost_total = float(resource.find(".//cost/total").text)

            time_in_use_min = float(resource.find(".//time/in_use/min").text)
            time_in_use_max = float(resource.find(".//time/in_use/max").text)
            time_in_use_median = float(resource.find(".//time/in_use/median").text)
            time_in_use_Q1 = float(resource.find(".//time/in_use/Q1").text)
            time_in_use_Q3 = float(resource.find(".//time/in_use/Q3").text)
            time_in_use_avg = float(resource.find(".//time/in_use/avg").text)
            time_in_use_total = float(resource.find(".//time/in_use/total").text)

            time_available_min = float(resource.find(".//time/available/min").text)
            time_available_max = float(resource.find(".//time/available/max").text)
            time_available_median = float(resource.find(".//time/available/median").text)
            time_available_Q1 = float(resource.find(".//time/available/Q1").text)
            time_available_Q3 = float(resource.find(".//time/available/Q3").text)
            time_available_avg = float(resource.find(".//time/available/avg").text)
            time_available_total = float(resource.find(".//time/available/total").text)

            time_workload_min = float(resource.find(".//time/workload/min").text)
            time_workload_max = float(resource.find(".//time/workload/max").text)
            time_workload_median = float(resource.find(".//time/workload/median").text)
            time_workload_Q1 = float(resource.find(".//time/workload/Q1").text)
            time_workload_Q3 = float(resource.find(".//time/workload/Q3").text)
            time_workload_avg = float(resource.find(".//time/workload/avg").text)
            time_workload_total = float(resource.find(".//time/workload/total").text)

            resource_data.append({
                "Resource Type": resource_type,
                "Cost Min": cost_min,
                "Cost Max": cost_max,
                "Cost Median": cost_median,
                "Cost Q1": cost_Q1,
                "Cost Q3": cost_Q3,
                "Cost Avg": cost_avg,
                "Cost Total": cost_total,
                "Time In Use Min": time_in_use_min,
                "Time In Use Max": time_in_use_max,
                "Time In Use Median": time_in_use_median,
                "Time In Use Q1": time_in_use_Q1,
                "Time In Use Q3": time_in_use_Q3,
                "Time In Use Avg": time_in_use_avg,
                "Time In Use Total": time_in_use_total,
                "Time Available Min": time_available_min,
                "Time Available Max": time_available_max,
                "Time Available Median": time_available_median,
                "Time Available Q1": time_available_Q1,
                "Time Available Q3": time_available_Q3,
                "Time Available Avg": time_available_avg,
                "Time Available Total": time_available_total,
                "Time Workload Min": time_workload_min,
                "Time Workload Max": time_workload_max,
                "Time Workload Median": time_workload_median,
                "Time Workload Q1": time_workload_Q1,
                "Time Workload Q3": time_workload_Q3,
                "Time Workload Avg": time_workload_avg,
                "Time Workload Total": time_workload_total,
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

        return process_df, resource_df, activity_df