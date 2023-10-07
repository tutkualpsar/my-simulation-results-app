import streamlit as st
import pandas as pd
import plost
import xml.etree.ElementTree as ET
import numpy as np
from bpmn_viewer import bpmn_viewer
import os 
import matplotlib.pyplot as plt
from globalconfigfile_processing import process_simulation_output
from simulationfile_processing import parse_simulation_xml
from formatting import highlight_diff
from resourceinputfile_processing import parce_resource_input

# Call set_page_config as the first Streamlit command
st.set_page_config(layout='wide', initial_sidebar_state='expanded')

st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 150px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.header('Simulation Dashboard')

# Create a sidebar with file upload widget
#uploaded_xml_file = st.file_uploader("Upload an XML file", type=["xml"])
#uploaded_sim_file = st.file_uploader("Upload the simulastion file", type=["xml"])
#uploaded_xes_file = st.file_uploader("Upload XES file (Resource Data)", type=["xes"])
#bpmn_file = st.file_uploader("Upload a BPMN (XML) File", type=["bpmn", "xml"])


    # Example: Extract and display specific data from the XML
    #st.subheader("Extracted Data:")

    # Display the DataFrame for activity data
    #st.subheader("Activity Data:")
    #st.write(activity_df)
    
    # Display the DataFrame for resource data
    #st.subheader("Resource Data:")
    #st.write(resource_df)

    # Display the DataFrame for process data
    #st.subheader("Process Data:")
    #st.write(process_df)

# Load the first simulation output
process_df, resource_df, activity_df = process_simulation_output("retailer_global_resourceutilization.xml")
# Load the second simulation output
process_df2, resource_df2, activity_df2 = process_simulation_output("retailer_global_resourceutilization2.xml")
# Load the first simulation resources
simulation_df = parse_simulation_xml("retailer_sim.xml")
# Load the second simulation resources
simulation_df2 = parse_simulation_xml("retailer_sim2.xml")
# Load the first simulation resource inputs
simulation_input_df = parce_resource_input("retailer_sim_inputs.xml")
# Load the second simulation resource inputs
simulation_input_df2 = parce_resource_input("retailer_sim_inputs2.xml")


# Merge the dataframes to create the comparison table of resources
merged_resource_df = pd.merge(resource_df, resource_df2, on='Resource Type', suffixes=('_Scenario1', '_Scenario2'), how='outer')
merged_resource_df['Difference'] = merged_resource_df['Cost Total_Scenario1'] - merged_resource_df['Cost Total_Scenario2']
merged_resource_df['Difference Percentage'] = ((merged_resource_df['Cost Total_Scenario1'] - merged_resource_df['Cost Total_Scenario2']) / merged_resource_df['Cost Total_Scenario1']) * 100
resource_cost_comparison_df = merged_resource_df[['Resource Type', 'Cost Total_Scenario1', 'Cost Total_Scenario2', 'Difference', 'Difference Percentage']].copy()
resource_comparison_df = resource_cost_comparison_df.style.applymap(highlight_diff, subset=['Difference', 'Difference Percentage'])

# Merge the dataframes to create the comparison table of activities
merged_resource_input_df = pd.merge(simulation_input_df, simulation_input_df2, on='Resource Type', suffixes=('_Scenario1', '_Scenario2'), how='outer')
merged_resource_input_df['Cost Difference'] = merged_resource_input_df['Cost_Scenario1'] - merged_resource_input_df['Cost_Scenario2']
merged_resource_input_df['Quantity Difference'] = merged_resource_input_df['Quantity_Scenario1'] - merged_resource_input_df['Quantity_Scenario2']
merged_resource_input_df['Cost Difference Percentage'] = ((merged_resource_input_df['Cost_Scenario1'] - merged_resource_input_df['Cost_Scenario2']) / merged_resource_input_df['Cost_Scenario1']) * 100
resource_input_comparison_df = merged_resource_input_df.style.applymap(highlight_diff, subset=['Quantity Difference', 'Cost Difference', 'Cost Difference Percentage'])

# Merge the dataframes to create the comparison table of activities
merged_activity_df = pd.merge(activity_df, activity_df2, on='Activity Name', suffixes=('_Scenario1', '_Scenario2'), how='outer')
#for cost:
merged_activity_df['Difference'] = merged_activity_df['Cost Total_Scenario1'] - merged_activity_df['Cost Total_Scenario2']
merged_activity_df['Difference Percentage'] = ((merged_activity_df['Cost Total_Scenario1'] - merged_activity_df['Cost Total_Scenario2']) / merged_activity_df['Cost Total_Scenario1']) * 100
#for time:
merged_activity_df['Duration Difference'] = merged_activity_df['Time Duration Total_Scenario1'] - merged_activity_df['Time Duration Total_Scenario2']
merged_activity_df['Duration Difference Percentage'] = ((merged_activity_df['Time Duration Total_Scenario1'] - merged_activity_df['Time Duration Total_Scenario2']) / merged_activity_df['Time Duration Total_Scenario1']) * 100

#comparisons:
##cost:
activity_cost_comparison_df = merged_activity_df[['Activity Name', 'Cost Total_Scenario1', 'Cost Total_Scenario2', 'Difference', 'Difference Percentage']].copy()
activity_comparison_df = activity_cost_comparison_df.style.applymap(highlight_diff, subset=['Difference', 'Difference Percentage'])
##duration:
activity_duration_comparison_df = merged_activity_df[['Activity Name', 'Time Duration Total_Scenario1', 'Time Duration Total_Scenario2', 'Duration Difference', 'Duration Difference Percentage']].copy()
activity_duration_comparison = activity_duration_comparison_df.style.applymap(highlight_diff, subset=['Duration Difference', 'Duration Difference Percentage'])


# Define a function to display the first page
def page_management():
    st.title("Management Overview")
    st.write("This is the management overview page.")

# Define a function to display the second page
def page_domainexperts():
    st.title("Detailed Parameters")
    st.write("This is the detailed paramaters page.")

# Define a function to display the first page
def extract_management():
    st.title("Extracted Data")
    st.write("This page is to display all simulation data.")

def page_comparison():
    st.title("Scenario Comparisons")
    st.write("This is the scenario comparsion page.")

    


# Create a sidebar with two buttons
sidebar_option = st.sidebar.radio("Navigate to Page", ("Management Overview", "Detailed Parameters","Extract Data", "Scenario Comparisons"))

# Display the selected page based on the button clicked
if sidebar_option == "Management Overview":
    page_management()

    min_cost_process = process_df['Cost Min']
    max_cost_process = process_df['Cost Max']
    avg_cost_process = process_df['Cost Avg']
    total_cost_process = process_df['Cost Total']
    total_cost_value = total_cost_process.iloc[0]
    min_cost_value = min_cost_process.iloc[0]  
    max_cost_value = max_cost_process.iloc[0] 
    avg_cost_value = avg_cost_process.iloc[0]

    time_flow_min =  process_df['Time Flow Min']
    time_flow_max = process_df['Time Flow Max']
    time_flow_avg = process_df['Time Flow Avg']
    time_flow_total = process_df['Time Flow Total']
    total_time_value = time_flow_total.iloc[0]
    min_time_value = time_flow_min.iloc[0]  
    max_time_value = time_flow_max.iloc[0] 
    avg_time_value = time_flow_avg.iloc[0]

    process_ins = simulation_df['processInstance']
    process_ins_value = process_ins.iloc[0]

    # Row A

    st.markdown(
        """
        <div style="background-color:#D2E0FB; padding: 8px; border-radius: 8px;">
            <h3 style="color: #FFFFFF;">Scenario Parameters</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    col1, col2, col3 = st.columns(3)
    col1.metric("Process Instance", process_ins_value)
    col2.metric("Process Cost", f"Total: {total_cost_value:.2f}", f"Min: {min_cost_value:.2f} | Max: {max_cost_value:.2f} | Avg: {avg_cost_value:.2f}" )
    col3.metric("Process Cycle Time", f"Total: {total_time_value:.2f}", f"Min: {min_time_value:.2f} | Max: {max_time_value:.2f} | Avg: {avg_time_value:.2f}" )

    # Row B
    st.markdown(
        """
        <div style="background-color:#D2E0FB; padding: 10px; border-radius: 10px;">
            <h3 style="color: #FFFFFF;">Process Overview</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    bpmn_file_path = "retailer_bpmn_copy.xml"

    # Load a specific BPMN file
    with open(bpmn_file_path, "r") as bpmn_contents:
        bpmn_file = bpmn_contents.read()

    if bpmn_file:
        # Process the uploaded BPMN file (you can continue with steps 5 and 6)
        # For now, you can print some information about the file
        #st.write("Uploaded BPMN file:", bpmn_file.name)
        #st.write("File size:", bpmn_file.size)
        #st.write("File size:", len(bpmn_file))  # Display file size instead
        
        bpmn_file_name = os.path.basename(bpmn_file_path)

        try:
            # Read the BPMN XML data as text
            bpmn_xml_text = bpmn_file

            # Remove any leading or trailing whitespace, including newlines
            bpmn_xml_text = bpmn_xml_text.strip()

            # Generate a unique identifier for the iframe
            iframe_id = f"bpmn_diagram_{bpmn_file_name}"

            # Calculate the height based on BPMN diagram content height
            content_height = 800  # You may need to adjust this based on your content
            iframe_height = content_height + 50  # Adding some padding

            # Display the BPMN diagram in an iframe with centered content and dynamic height
            st.write(
                f'<iframe id="{iframe_id}" srcdoc=\'<html><head><style>#bpmn-diagram {{ display: block; margin: 0 auto; }}</style></head><body><div id="bpmn-diagram"></div><script src="https://cdn.jsdelivr.net/npm/bpmn-js@8.6.0/dist/bpmn-viewer.production.min.js"></script><script>var bpmnViewer = new BpmnJS({{container: "#bpmn-diagram"}}); bpmnViewer.importXML(`{bpmn_xml_text}`);</script></body></html>\' width="100%" height="{iframe_height}px"></iframe>',
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"Error processing BPMN file: {str(e)}")


    st.markdown(
        """
        <div style="background-color:#D2E0FB; padding: 8px; border-radius: 8px;">
            <h3 style="color: #FFFFFF;">Resource Parameters</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Load a specific XES file
    with open("retailer_bpmn.xes", "r") as xes_contents:
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

                if activity_name not in activity_counts:
                    activity_counts[activity_name] = {"started": 0, "completed": 0}
        
                if transition == "start":
                    activity_counts[activity_name]["started"] += 1
                elif transition == "complete":
                    activity_counts[activity_name]["completed"] += 1

        activity_count_data = []
        
        for activity_name, counts in activity_counts.items():
            activity_count_data.append({"Activity": activity_name, "Started": counts["started"], "Completed": counts["completed"]})

        act_count_df = pd.DataFrame(activity_count_data)

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


    # Add subheaders for "Responsibility Matrix" and "Utilisation Matrix"
    selected_matrix = st.radio("Select matrix to display:", ("Responsibility Matrix", "Utilisation Matrix"))

    ##st.write(act_count_df) --- display these numbers when you make bpmn interactive

    if selected_matrix == "Responsibility Matrix":
        # Display the resource-task matrix
        st.subheader("Responsibility Matrix:")
        st.write(resource_matrix)

    elif selected_matrix == "Utilisation Matrix":
        # Create the utilization table
        utilization_table = resource_df[["Resource Type", "Time In Use Total", "Cost Total", "Time Workload Total"]]
        utilization_table.columns = ["Resource Type", "Total Working Time", "Cost", "Utilisation Ratio"]

        # Display the utilization table
        st.subheader("Utilisation Matrix:")
        st.write(utilization_table)

    st.markdown(
        """
        <div style="background-color:#D2E0FB; padding: 8px; border-radius: 8px;">
            <h3 style="color: #FFFFFF;">Activity Parameters</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Create a bar chart
    st.subheader("Bar Chart of Started and Completed Activities")
    fig, ax = plt.subplots()
    # Define the positions for the bars on the x-axis
    x = range(len(act_count_df['Activity']))
    # Plot the bars for started and completed activities
    ax.bar(x, act_count_df['Started'], width=0.4, label='Started', align='center', color='blue')
    ax.bar(x, act_count_df['Completed'], width=0.4, label='Completed', align='edge', color='green')
    # Set labels and title
    ax.set_xlabel('Activity')
    ax.set_ylabel('Count')
    ax.set_title('Started and Completed Activities by Activity')
    # Set the x-axis labels to be the activity names
    ax.set_xticks(x)
    ax.set_xticklabels(act_count_df['Activity'], rotation=45, ha='right')
    # Add a legend
    ax.legend()

    # Set up the colors for the bars
    colors = ['blue', 'green', 'red']
    # Create a figure and axis
    fig_b, ax_b = plt.subplots()
    # Get the number of activities
    num_activities = len(activity_df)
    # Set the width of the bars
    bar_width = 0.2
    # Set the positions of the bars on the x-axis
    r1 = np.arange(num_activities)
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]
    # Plot the bars for each column
    ax_b.bar(r1, activity_df['Time Duration Avg'], color=colors[0], width=bar_width, edgecolor='grey', label='Time Duration Avg')
    ax_b.bar(r2, activity_df['Time Waiting Avg'], color=colors[1], width=bar_width, edgecolor='grey', label='Time Waiting Avg')
    ax_b.bar(r3, activity_df['Time Resources Idle Avg'], color=colors[2], width=bar_width, edgecolor='grey', label='Time Resources Idle Avg')
    # Set labels and title
    ax_b.set_xlabel('Activity')
    ax_b.set_ylabel('Average Time')
    ax_b.set_title('Average Time Metrics by Activity')
    ax_b.set_xticks([r + bar_width for r in range(num_activities)])
    ax_b.set_xticklabels(activity_df['Activity Name'])
    # Add a legend
    ax_b.legend()


    c1, c2 = st.columns((7,3))
    with c1:
        st.markdown('### Activity Counts')
        st.pyplot(fig)
    with c2:
        st.markdown('### Activity Duration - Mean')
        st.pyplot(fig_b)


elif sidebar_option == "Detailed Parameters":
    page_domainexperts()

elif sidebar_option == "Extract Data" :
    extract_management()

    # Navigate to the new view to display the dataframes
    st.markdown("## Extracted Data:")
    
    # Display the first set of DataFrames
    st.markdown("### First Set of Dataframes:")
    st.markdown("#### Activity Data:")
    st.write(activity_df)

    st.markdown("#### Resource Data:")
    st.write(resource_df)

    st.markdown("#### Process Data:")
    st.write(process_df)

    st.markdown("#### Simulation Parameters:")
    st.write(simulation_df)

    # Display the second set of DataFrames
    st.markdown("### Second Set of Dataframes:")
    st.markdown("#### Activity Data:")
    st.write(activity_df2)

    st.markdown("#### Resource Data:")
    st.write(resource_df2)

    st.markdown("#### Process Data:")
    st.write(process_df2)

    st.markdown("#### Simulation Parameters:")
    st.write(simulation_df2)

elif sidebar_option == "Scenario Comparisons" :
    page_comparison()

    comparison_choice = st.sidebar.selectbox("Select Comparison Type", ["Cost", "Time"])

    if comparison_choice == "Cost":
         # Display the resource inputs of simulation
        st.markdown("Simulation Inputs of Resource:")
        st.write(resource_input_comparison_df)
        
        # Display the comparison table with conditional formatting
        st.markdown("Resource Cost Comparison Table:")
        st.write(resource_comparison_df)

        # Display the comparison table with conditional formatting
        st.markdown("Activity Cost Comparison Table:")
        st.write(activity_comparison_df)
        
    elif comparison_choice == "Time":
         # Display the comparison table with conditional formatting
        st.markdown("Activity Duration Comparison Table:")
        st.write(activity_duration_comparison)

        


