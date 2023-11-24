import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime
import streamlit as st


def resource_responsibility(xml_file_path):
    # Load the XES file
     # Load the XES file
    with open(xml_file_path, "r") as xes_contents:
        uploaded_xes_file = xes_contents.read()

    if uploaded_xes_file is not None:
        # Parse the XES file content using ElementTree
        root = ET.fromstring(uploaded_xes_file)

        # Create a list to store unique tasks and resources
        tasks = []
        resources = []
        activity_counts = {}

        # Extract tasks and resources from XES file
        for trace in root.findall(".//trace"):
            for event in trace.findall(".//event"):
                resource_elem = event.find(".//string[@key='org:resource']")
                task_elem = event.find(".//string[@key='concept:name']")
                activity_name = event.find('string[@key="concept:name"]').attrib['value']
                transition = event.find('string[@key="lifecycle:transition"]').attrib['value']

                if resource_elem is not None and task_elem is not None:
                    resource = resource_elem.attrib.get('value')
                    task = task_elem.attrib.get('value')

                    tasks.append(task)
                    resources.append(resource)

                # Exclude special events
                if not activity_name.startswith("sid-"):
                    if activity_name not in activity_counts:
                        activity_counts[activity_name] = {"started": 0, "completed": 0}
                    
                    if transition == "start":
                        activity_counts[activity_name]["started"] += 1
                    elif transition == "complete":
                        activity_counts[activity_name]["completed"] += 1

        activity_count_data = []
            
        for activity_name, counts in activity_counts.items():
            activity_count_data.append({"Activity": activity_name, "Started": counts["started"], "Completed": counts["completed"]})

        activity_count_df = pd.DataFrame(activity_count_data)

        earliest_start_date = None
        latest_end_date = None

        for trace in root.findall(".//trace"):
            for event in trace.findall(".//event"):
                transition = event.find('string[@key="lifecycle:transition"]').attrib['value']
                timestamp_str = event.find("date[@key='time:timestamp']").attrib['value']

                if timestamp_str and timestamp_str.strip() != '':
                    try:
                        timestamp = datetime.fromisoformat(timestamp_str)
                    except ValueError:
                        st.warning(f"Ignoring invalid timestamp format: {timestamp_str}")
                        continue

                    if transition == 'start':
                        if earliest_start_date is None or timestamp < earliest_start_date:
                            earliest_start_date = timestamp

                    elif transition == 'complete':
                        if latest_end_date is None or timestamp > latest_end_date:
                            latest_end_date = timestamp


        # Calculate time difference in seconds if both start and end dates exist
        time_difference_seconds = (latest_end_date - earliest_start_date).total_seconds() if earliest_start_date and latest_end_date else None


        # Create a DataFrame to represent the resource-task matrix
        resource_matrix = pd.DataFrame(index=sorted(set(resources)), columns=sorted(set(tasks)), dtype=str)

        # Fill the resource-task matrix
        for trace in root.findall(".//trace"):
            resource = None
            for event in trace.findall(".//event"):
                resource_elem = event.find(".//string[@key='org:resource']")
                task_elem = event.find(".//string[@key='concept:name']")

                if resource_elem is not None and task_elem is not None:
                    resource = resource_elem.attrib.get('value')
                    task = task_elem.attrib.get('value')
                    resource_matrix.at[resource, task] = 'X'

        # Fill NaN values with empty strings
        resource_matrix = resource_matrix.fillna('')

        return resource_matrix, earliest_start_date, latest_end_date, time_difference_seconds, activity_count_df
