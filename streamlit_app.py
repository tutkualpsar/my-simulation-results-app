import streamlit as st
import pandas as pd
import seaborn as sns
import xml.etree.ElementTree as ET
import numpy as np
from bpmn_viewer import bpmn_viewer
import os 
import matplotlib.pyplot as plt
from globalconfigfile_processing import process_simulation_output
from simulationfile_processing import parse_simulation_xml
from formatting import highlight_diff
from resourceinputfile_processing import parce_resource_input
from matplotlib.ticker import FuncFormatter
from bpmn_file_processing import resource_responsibility
from download_function import download_button



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

############################################
#CREATING AND/OR CALLING NECESSARY DATAFRAMES
############################################

# Load the first simulation output
process_df, resource_df, activity_df, instance_df, process_instances_df, plot_data, time_unit= process_simulation_output("retailer_global_resourceutilization.xml")
# Load the second simulation output
process_df2, resource_df2, activity_df2, instance_df2, process_instances_df2, plot_data2, time_unit2 = process_simulation_output("retailer_global2_resourceutilization.xml")
# Load the first simulation resources
simulation_df = parse_simulation_xml("retailer_sim.xml")
# Load the second simulation resources
simulation_df2 = parse_simulation_xml("retailer_sim2.xml")
# Load the first simulation resource inputs
simulation_input_df = parce_resource_input("retailer_global.xml")
# Load the second simulation resource inputs
simulation_input_df2 = parce_resource_input("retailer_global2.xml")
# Load the first simulation resource inputs for utilization matrix

resource_matrix, start_date_str, end_date_str, time_difference_seconds, activity_count_df = resource_responsibility("retailer_bpmn.xes")
resource_matrix2, start_date_str2, end_date_str2, time_difference_seconds2, activity_count_df2= resource_responsibility("retailer_bpmn2.xes")
#res_ut_merged_df = pd.merge(resource_df, simulation_df, on='Resource Type', how='inner')

# Create resource_time_df
#resource_time_df = pd.DataFrame({
 #   'Resource Type': res_ut_merged_df['Resource Type'],
 #   'Time In Use': res_ut_merged_df['Time In Use'],
#  'Time Available': res_ut_merged_df['Time Available'],
#  'Time Workload': res_ut_merged_df['Time Workload'],
#    'Total Available Time': res_ut_merged_df['Time In Use'] + res_ut_merged_df['Time Available'],
#    'Utilization Ratio': (res_ut_merged_df['Time In Use'] / (res_ut_merged_df['Time In Use'] + res_ut_merged_df['Time Available'])) * 100,
#    'Utilization Ratio (Exc Off Time Table Hours)': (res_ut_merged_df['Time In Use'] / res_ut_merged_df['Business Hours']) * 100
#})


############################################
#CALCULATIONS FOR SIMULATION COMPARISON PAGE
############################################

process_ins = simulation_df['processInstance']
process_ins_value = process_ins.iloc[0]
process_ins2 = simulation_df2['processInstance']
process_ins_value2 = process_ins2.iloc[0]

# Merge the dataframes to create the comparison table of resources
merged_resource_df = pd.merge(resource_df, resource_df2, on='Resource Type', suffixes=('_Scenario1', '_Scenario2'), how='outer')
#for cost
merged_resource_df['CostperInstance_Scenario1'] = merged_resource_df['Cost_Scenario1'] / process_ins_value
merged_resource_df['CostperInstance_Scenario2'] = merged_resource_df['Cost_Scenario2'] / process_ins_value2


merged_resource_df['Difference Total Cost'] = merged_resource_df['Cost_Scenario1'] - merged_resource_df['Cost_Scenario2']
merged_resource_df['Difference CostperInstance'] = merged_resource_df['CostperInstance_Scenario1'] - merged_resource_df['CostperInstance_Scenario2']
merged_resource_df['Difference Percentage Total Cost'] = ((merged_resource_df['Cost_Scenario1'] - merged_resource_df['Cost_Scenario2']) / merged_resource_df['Cost_Scenario1']) * 100
merged_resource_df['Difference CostperInstance Percentage'] = ((merged_resource_df['CostperInstance_Scenario1'] - merged_resource_df['CostperInstance_Scenario2']) / merged_resource_df['CostperInstance_Scenario1']) * 100
resource_cost_comparison_df = merged_resource_df[['Resource Type', 'Cost_Scenario1', 'Cost_Scenario2', 'Difference Total Cost', 'Difference Percentage Total Cost', 'CostperInstance_Scenario1', 'CostperInstance_Scenario2', 'Difference CostperInstance', 'Difference CostperInstance Percentage']].copy()
resource_comparison_df = resource_cost_comparison_df.style.applymap(highlight_diff, subset=['Difference Total Cost', 'Difference Percentage Total Cost', 'Difference CostperInstance', 'Difference CostperInstance Percentage'])
rounded_resource_comparison_df = resource_comparison_df.format({'Cost_Scenario1': '{:.2f}', 'Cost_Scenario2': '{:.2f}', 'Difference Total Cost': '{:.2f}', 'Difference Percentage Total Cost': '{:.2f}', 'CostperInstance_Scenario1' : '{:.2f}' , 'CostperInstance_Scenario2': '{:.2f}', 'Difference CostperInstance': '{:.2f}', 'Difference CostperInstance Percentage': '{:.2f}'})

#for time
merged_resource_df['Time In Use Difference'] = merged_resource_df['Time In Use_Scenario1'] - merged_resource_df['Time In Use_Scenario2']
merged_resource_df['Time In Use Difference Percentage'] = ((merged_resource_df['Time In Use_Scenario1'] - merged_resource_df['Time In Use_Scenario2']) / merged_resource_df['Time In Use_Scenario1']) * 100
merged_resource_df['Time Available Difference'] = merged_resource_df['Time Available_Scenario1'] - merged_resource_df['Time Available_Scenario2']
merged_resource_df['Time Available Difference Percentage'] = ((merged_resource_df['Time Available_Scenario1'] - merged_resource_df['Time Available_Scenario2']) / merged_resource_df['Time Available_Scenario1']) * 100
merged_resource_df['Time Workload Difference'] = merged_resource_df['Time Workload_Scenario1'] - merged_resource_df['Time Workload_Scenario2']
merged_resource_df['Time Workload Difference Percentage'] = ((merged_resource_df['Time Workload_Scenario1'] - merged_resource_df['Time Workload_Scenario2']) / merged_resource_df['Time Workload_Scenario1']) * 100


resource_time_comparison_df = merged_resource_df[['Resource Type', 'Time In Use_Scenario1', 'Time In Use_Scenario2', 'Time In Use Difference', 'Time In Use Difference Percentage', 
                                                'Time Available_Scenario1', 'Time Available_Scenario2', 'Time Available Difference', 'Time Available Difference Percentage',
                                                'Time Workload_Scenario1', 'Time Workload_Scenario2', 'Time Workload Difference', 'Time Workload Difference Percentage']].copy()
resource_t_comparison_df = resource_time_comparison_df.round(2).style.applymap(highlight_diff, subset=['Time In Use Difference', 'Time In Use Difference Percentage', 'Time Available Difference', 'Time Available Difference Percentage', 'Time Workload Difference', 'Time Workload Difference Percentage'])
rounded_resource_t_comparison_df = resource_t_comparison_df.format({'Time In Use_Scenario1': '{:.2f}', 'Time In Use_Scenario2': '{:.2f}', 'Time In Use Difference': '{:.2f}', 'Time In Use Difference Percentage': '{:.2f}', 
                                                'Time Available_Scenario1': '{:.2f}', 'Time Available_Scenario2': '{:.2f}', 'Time Available Difference': '{:.2f}', 'Time Available Difference Percentage': '{:.2f}',
                                                'Time Workload_Scenario1': '{:.2f}', 'Time Workload_Scenario2': '{:.2f}', 'Time Workload Difference': '{:.2f}', 'Time Workload Difference Percentage': '{:.2f}'})

# Merge the dataframes to create the comparison table of activities
merged_resource_input_df = pd.merge(simulation_input_df, simulation_input_df2, on='Resource Type', suffixes=('_Scenario1', '_Scenario2'), how='outer')
merged_resource_input_df['Cost per Hour Difference'] = merged_resource_input_df['Cost per Hour_Scenario1'] - merged_resource_input_df['Cost per Hour_Scenario2']
merged_resource_input_df['Quantity Difference'] = merged_resource_input_df['Quantity_Scenario1'] - merged_resource_input_df['Quantity_Scenario2']
merged_resource_input_df['Cost per Hour Difference Percentage'] = ((merged_resource_input_df['Cost per Hour_Scenario1'] - merged_resource_input_df['Cost per Hour_Scenario2']) / merged_resource_input_df['Cost per Hour_Scenario1']) * 100
merged_resource_input_df = merged_resource_input_df.style.applymap(highlight_diff, subset=['Quantity Difference', 'Cost per Hour Difference', 'Cost per Hour Difference Percentage'])
rounded_resource_input_comparison_df = merged_resource_input_df.format({'Cost per Hour_Scenario1': '{:.2f}', 'Cost per Hour_Scenario2': '{:.2f}', 'Quantity_Scenario1' : '{:.2f}', 'Quantity_Scenario2' : '{:.2f}', 'Quantity Difference' : '{:.2f}' , 'Cost per Hour Difference' : '{:.2f}', 'Cost per Hour Difference Percentage': '{:.2f}'})


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
activity_comparison_df = activity_cost_comparison_df.round(2).style.applymap(highlight_diff, subset=['Difference', 'Difference Percentage'])
rounded_activity_comparison_df = activity_comparison_df.format({'Cost Total_Scenario1': '{:.2f}', 'Cost Total_Scenario2': '{:.2f}', 'Difference': '{:.2f}', 'Difference Percentage': '{:.2f}'})

##duration:
activity_duration_comparison_df = merged_activity_df[['Activity Name', 'Time Duration Total_Scenario1', 'Time Duration Total_Scenario2', 'Duration Difference', 'Duration Difference Percentage']].copy()
activity_duration_comparison = activity_duration_comparison_df.round(2).style.applymap(highlight_diff, subset=['Duration Difference', 'Duration Difference Percentage'])
rounded_activity_duration_comparison = activity_duration_comparison.format({'Time Duration Total_Scenario1': '{:.2f}', 'Time Duration Total_Scenario2': '{:.2f}', 'Duration Difference': '{:.2f}', 'Duration Difference Percentage': '{:.2f}'})


#for graphs: 
#rounded_resource_comparison_df = rounded_resource_comparison_df.data
#rounded_resource_input_comparison_df = rounded_resource_input_comparison_df.data
#merged_df_resource_cost = pd.merge(rounded_resource_comparison_df, rounded_resource_input_comparison_df, on='Resource Type', suffixes=('_Instance', '_Hourly'))

############################################
#DEFINING NAVIGATION PAGES AND THE SIDEBAR
############################################
# Define a function to display the first page
def page_management():
    st.title("Management Overview")
    st.write("""This is the management overview page. Here you may find the summarized Key Performance Indicators 
    (KPIs) of the simulated process. This page is designed for stakeholders, managers, and decision-makers seeking 
    a comprehensive understanding of the simulated business processes. This management overview page serves as a 
    valuable tool for strategic planning, process optimization, and decision-making based on the outcomes of the 
    simulation.""")

# Define a function to display the second page
def page_domainexperts():
    st.title("Detailed Parameters")
    st.write("""This is the Detailed Parameters page, meticulously crafted for domain experts, including Simulation
    Experts, Simulation Consultants, and BPM (Business Process Management) Specialists. On this page, you will find
    detailed Key Performance Indicators (KPIs) specific to the simulated business processes. Tailored for those with
    a throughout understanding of simulations, this detailed parameters page offers a granular breakdown of 
    simulation insights, enabling deep analysis, fine-tuning, and strategic decision-making for process optimization
    and informed decision support.""")

# Define a function to display the first page
def extract_management():
    st.title("Extracted Data")
    st.write("""This is the Extract Data page, designed to provide users with access to all data used within the 
    dashboard in a straightforward manner. Here, you'll discover information related to two distinct simulation 
    scenarios, encompassing data on activities, resources, processes, and simulation parameters. Additionally, 
    detailed data on activity instances and process instances is available. Moreover, users have the option to 
    download this data in CSV format.""")

def page_comparison():
    st.title("Scenario Comparisons")
    st.write("""This is the Scenario Comparisons page, dedicated to providing an insightful analysis of two distinct
    simulation scenarios for the same process. The page is divided into two comprehensive sections: Cost and Time. 
    Throughout the comparison tables, differences in percentages are visually emphasized, with negative variances 
    highlighted in red and positive ones in green. It's important to note that the comparison process considers the 
    first scenario as the baseline. Therefore, a negative difference indicates that the values of the first scenario
    are smaller than those of the second scenario.""")


# Create a sidebar with two buttons
sidebar_option = st.sidebar.radio("Navigate to Page", ("Management Overview", "Detailed Parameters","Extract Data", "Scenario Comparisons"))


############################################
#MANAGEMENT OVERVIEW PAGE
############################################

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

    process_ins2 = simulation_df2['processInstance']
    process_ins_value2 = process_ins2.iloc[0]

    # Row A
    st.markdown(
        """
        <div style="background-color:#D2E0FB; padding: 10px; border-radius: 10px; margin-top: 20px;">
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
                f'<iframe id="{iframe_id}" srcdoc=\'<html><head><style>#bpmn-diagram {{ display: block; margin: 0 auto; margin-left: -200px;}}</style></head><body><div id="bpmn-diagram"></div><script src="https://cdn.jsdelivr.net/npm/bpmn-js@8.6.0/dist/bpmn-viewer.production.min.js"></script><script>var bpmnViewer = new BpmnJS({{container: "#bpmn-diagram"}}); bpmnViewer.importXML(`{bpmn_xml_text}`);</script></body></html>\' width="100%" height="200px"></iframe>',
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"Error processing BPMN file: {str(e)}")

    #Row B
    st.markdown(
        """
        <div style="background-color:#D2E0FB; padding: 10px; border-radius: 10px; margin-top: 20px;">
            <h3 style="color: #FFFFFF;">Simulation Parameters</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write(f"❗ Time units of this process are in {time_unit}.")

    # Create an expander for the info section of simulation parameters
    with st.expander("ℹ️ Access detailed information on simulation parameters."):
        st.write("""
        Simulation parameters are the configurable and influential factors that define the 
        characteristics and conditions of a simulation model. Below you may find the definition of each metric: \n
        - Process Instance: Number of replications that is executed before running the simulation. 
        - Process Cost: Process cost refers to the total cost incurred in the simulated process. 
        - Processing Cycle Time: Cycle time is the duration it takes to complete a simulated business process.
        It includes the time spent on each activity, waiting time, and any delays in the process. 
        - Total Duration: Process total duration is the elapsed time required for the completion of an entire process, 
        encompassing all its individual steps and activities.
        """)


    style = """
        <style>
            .custom-metric {
                background-color: #EEEEEE;
                border: 1px solid #DCDCDC;
                padding: 5% 5% 5% 10%;
                border-radius: 10px;
                border-left: 0.5rem solid #9AD8E1 !important;
                box-shadow: 0 0.15rem 1.75rem 0 rgba(58, 59, 69, 0.15) !important;
            }
            .metric-title {
                color: #36b9cc !important;
                font-weight: 700 !important;
                text-transform: uppercase !important;
            }
        </style>
    """

    st.markdown(style, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    # Metric for Process Instance
    col1.markdown('<div class="metric-title">Process Instance</div>', unsafe_allow_html=True)
    col1.markdown(f'<div class="custom-metric">{process_ins_value}</div>', unsafe_allow_html=True)

    # Metric for Process Cost
    col2.markdown('<div class="metric-title">Process Cost</div>', unsafe_allow_html=True)
    col2.markdown(f'<div class="custom-metric">Total: {total_cost_value:.2f}<br>Min: {min_cost_value:.2f} | Max: {max_cost_value:.2f} | Per Instance: {avg_cost_value:.2f}</div>', unsafe_allow_html=True)

    # Calculate days, hours, minutes, and seconds
    days = avg_time_value // (24 * 3600)
    hours = (avg_time_value % (24 * 3600)) // 3600
    minutes = (avg_time_value % 3600) // 60
    seconds = avg_time_value % 60
    days_total = total_time_value // (24 * 3600)
    hours_total = (total_time_value % (24 * 3600)) // 3600
    minutes_total = (total_time_value % 3600) // 60
    seconds_total = total_time_value % 60


    # Metric for Process Cycle Time
    col3.markdown('<div class="metric-title">Process Cycle Time</div>', unsafe_allow_html=True)
    ##col3.markdown(f'<div class="custom-metric">Average:{avg_time_value:.2f}<br>Min: {min_time_value:.2f} | Max: {max_time_value:.2f} | Total: {total_time_value:.2f}</div>', unsafe_allow_html=True)
    col3.markdown(f'<div class="custom-metric">Average: {avg_time_value:.2f} seconds<br>'
              f'( {days:.2f} days, {hours:.2f} hours, {minutes:.2f} minutes, {seconds:.2f} seconds)<br>'
              f'Min: {min_time_value:.2f} | Max: {max_time_value:.2f} | Total: {total_time_value:.2f} ( {days_total:.2f} days, {hours_total:.2f} hours, {minutes_total:.2f} minutes, {seconds_total:.2f} seconds) </div>',
              unsafe_allow_html=True)
              
 
    # Additional Metrics
    colc1, colc2, colc3 = st.columns(3)

    # Metric for Process Start Date
    colc1.markdown('<div class="metric-title">Process Start Date</div>', unsafe_allow_html=True)
    colc1.markdown(f'<div class="custom-metric">{start_date_str.strftime("%Y-%m-%d")}<br>{start_date_str.strftime("%H:%M:%S%z") if start_date_str else ""}</div>', unsafe_allow_html=True)

    # Metric for Process End Date
    colc2.markdown('<div class="metric-title">Process End Date</div>', unsafe_allow_html=True)
    colc2.markdown(f'<div class="custom-metric">{end_date_str.strftime("%Y-%m-%d")}<br>{end_date_str.strftime("%H:%M:%S%z") if end_date_str else ""}</div>', unsafe_allow_html=True)

    days_sim = time_difference_seconds // (24 * 3600)
    hours_sim = (time_difference_seconds % (24 * 3600)) // 3600
    minutes_sim = (time_difference_seconds % 3600) // 60
    seconds_sim = time_difference_seconds % 60
    # Metric for Process Duration
    colc3.markdown('<div class="metric-title">Total Simulated Time</div>', unsafe_allow_html=True)
    colc3.markdown(f'<div class="custom-metric">{time_difference_seconds} ({days_sim:.2f} days, {hours_sim:.2f} hours, {minutes_sim:.2f} minutes, {seconds_sim:.2f} seconds) </div>', unsafe_allow_html=True)

    melted_df_res = pd.melt(resource_df, id_vars='Resource Type', var_name='Parameter', value_name='Value')
    cost_df = melted_df_res[melted_df_res['Parameter'].str.contains('Cost')]
    time_df = melted_df_res[melted_df_res['Parameter'].str.contains('Time')]
    total_cost = cost_df.groupby('Resource Type')['Value'].sum().reset_index()
    # Create a pie chart for the percentage of each resource's total cost
    
    st.markdown(
        """
        <div style="background-color:#D2E0FB; padding: 10px; border-radius: 10px; margin-top: 20px;">
            <h3 style="color: #FFFFFF;">Cost Parameters</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("ℹ️ Access detailed information on simulation parameters."):
        st.write("""
        - Cost Distribution Amonng Resources: Provides an overview of the total cost associated with each resource and the percentage contribution of each resource 
        to the overall cost. Here you can identify resources with significant cost contributions.
         - Cost Distribution Among Activities: Provides an overview of the total cost associated with each activity and the percentage contribution of each activity 
         to the overall cost. Here you can identify activities with significant cost contributions.

        """)
    
    fig, axes = plt.subplots(1, 2, figsize=(18, 6))
    wedges, texts, autotexts = axes[0].pie(
        cost_df['Value'],
        labels=cost_df['Resource Type'],
        #pctdistance = 1.2,
        #labeldistance = 1.4,
        autopct=lambda x: f'{x:.1f}%\n({(x/100)*sum(cost_df["Value"]):.0f} Cost Unit)',
        #radius = 2,
        colors=["#B2A4FF", "#1640D6", "#AAE3E2"]
    )   
    axes[0].set_title('Cost Distribution Among Resources')
    # Create a pie chart for the percentage of each activity's total cost
    wedges, texts, autotexts = axes[1].pie(
        activity_df['Cost Total'],
        labels=activity_df['Activity Name'],
        autopct=lambda x: f'{x:.1f}%\n({(x/100)*sum(activity_df["Cost Total"]):.0f} Cost Unit)',
        colors=['#A25772', '#ffc7c7', '#61A3BA', '#F5E8C7']
    )
    axes[1].set_title('Cost Distribution Among Activities')
    plt.tight_layout()
    st.pyplot(fig)


    st.markdown(
        """
        <div style="background-color:#D2E0FB; padding: 10px; border-radius: 10px; margin-top: 20px;">
            <h3 style="color: #FFFFFF;">Roles Overview</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

        # Create an expander for the info section
    with st.expander("ℹ️ Access detailed information on roles overview."):
        st.write("""
        A resource refers to individuals or entities assigned to specific roles within a process. 
        Resources play a crucial role in the successful execution of activities and contribute to the overall 
        efficiency of the simulated business environment. Below you may find the definition of each table: 
        - __Responsibility Matrix:__ The Responsibility Matrix provides a clear overview of roles and their associated 
        responsibilities within the simulated process.
            - Roles: Identifies the different positions or functions involved in the process simulation.
            - Responsibilities: Outlines the specific activities and tasks assigned to each role.
        - __Utilization Matrix:__ The Utilization Matrix offers insights into the performance and efficiency of each 
        resource within the simulated business scenario.
            - Total Working Time: Indicates the actual time each resource spends actively working on assigned tasks.
            - Cost: Represents the associated cost of utilizing each resource in the simulation.
            - Utilization Ratio (Workload): Calculated as "Time In Use" divided by "Available Time," providing a 
        measure of how efficiently each resource is utilized.    
        """)

    table_style = """
        <style>
            table {
                font-size: 18px;
                border-collapse: collapse;
                width: 100%;
                margin-bottom: 10px;
            }
            th, td {
                padding: 12px;
                border: 2px solid #ffffff; /* Set border color to white */
                text-align: left;
            }
            th {
                background-color: #D1D9D9;
                color: white;
            }
            tr:nth-child(even) {
                background-color: #f2f2f2;
            }
        </style>
    """
    
    utilization_table = resource_df[["Resource Type", "Time In Use", "Cost", "Time Workload"]]
    utilization_table.columns = ["Resource Type", "Total Working Time", "Cost", "Utilisation Ratio"]
    merged_df = pd.merge(utilization_table, simulation_input_df, on='Resource Type', suffixes=('_Utilization', '_ResourceInput'))
    
    # Add subheaders for "Responsibility Matrix" and "Utilisation Matrix"
    selected_matrix = st.radio("Select matrix to display:", ("Responsibility Matrix", "Utilisation Matrix"))
    st.markdown(table_style, unsafe_allow_html=True)
    if selected_matrix == "Responsibility Matrix":
        # Display the resource-task matrix
        st.table(resource_matrix)
    elif selected_matrix == "Utilisation Matrix":
        st.table(merged_df)
       


############################################
#DETAILED PARAMETERS PAGE
############################################

elif sidebar_option == "Detailed Parameters":
    page_domainexperts()

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
        
        bpmn_file_name = os.path.basename(bpmn_file_path)

        try:
            # Read the BPMN XML data as text
            bpmn_xml_text = bpmn_file
            # Remove any leading or trailing whitespace, including newlines
            bpmn_xml_text = bpmn_xml_text.strip()
            # Generate a unique identifier for the iframe
            iframe_id = f"bpmn_diagram_{bpmn_file_name}"
            # Calculate the height based on BPMN diagram content height
            content_height = 800  
            iframe_height = content_height + 50  # Adding some padding
            # Display the BPMN diagram in an iframe with centered content and dynamic height
            st.write(
                f'<iframe id="{iframe_id}" srcdoc=\'<html><head><style>#bpmn-diagram {{ display: block; margin: 0 auto; margin-left: -200px;}}</style></head><body><div id="bpmn-diagram"></div><script src="https://cdn.jsdelivr.net/npm/bpmn-js@8.6.0/dist/bpmn-viewer.production.min.js"></script><script>var bpmnViewer = new BpmnJS({{container: "#bpmn-diagram"}}); bpmnViewer.importXML(`{bpmn_xml_text}`);</script></body></html>\' width="100%" height="200px"></iframe>',
                unsafe_allow_html=True
            )
        except Exception as e:
            st.error(f"Error processing BPMN file: {str(e)}")

    st.markdown(
        """
        <div style="background-color:#D2E0FB; padding: 10px; border-radius: 10px;">
            <h3 style="color: #FFFFFF;">Process Instances</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write(f"❗ Time units of this process are in {time_unit}.")

    with st.expander("ℹ️ Access detailed information on process instances."):
        st.write("""
        An instance refers to a specific occurrence or execution of a process within the simulated environment. 
        Each instance represents a unique journey through the defined workflow, capturing the duration, activities, 
        and associated costs. Below you may find the following tables offering detailed breakdowns and valuable 
         insights on process instance: 
         - __Duration of Process Instances:__ Bar chart illustrating the total duration of each instance and the percentage of waiting
        time. Here, you can identify time distribution patterns within instances, pinpointing areas for optimization in terms of waiting 
        time.
        - __Cost of Process Instances__: Bar chart showcasing the cost associated with each process instance. Here youc can 
        analyze cost variations among instances, enabling to optimize resource allocation and reduce overall expenses.
        - __Waiting Percentages Among Process Instances__: Histogram illustrating distribution of waiting time percentages in the duration of each process instance. This allows 
        you to understand the waiting time patterns across instances.
        - __Distribution of Instance Cost__: Histogram illustrating the distribution of costs across instances. 
        This helps in identifying the frequency of different cost intervals.
        - __Total Duration of Process Instances per Activity__: Stacked bar chart presenting the total duration of process 
        instances broken down by activity type. Here you can understand which activity types contribute the most to 
        overall instance durations, guiding process improvement efforts.
        - __Total Cost of Process Instances per Activit__: Stacked bar chart depicting the total cost of process instances 
        categorized by activity type. Here you can identify cost-intensive activities.""")

       

    # Plot the bar chart for process instance duration
    process_instances_df = process_instances_df.sort_values(by='Instance No')
    fig_pi, ax_pi = plt.subplots(figsize=(10, 6))
    ax_pi.bar(process_instances_df['Instance No'], process_instances_df['Duration'], color='#427D9D', label='Total Duration')
    ax_pi2 = ax_pi.twinx()
    waiting_percentage = (process_instances_df['Waiting'] / process_instances_df['Duration']) * 100
    ax_pi2.plot(process_instances_df['Instance No'], waiting_percentage, color='red', marker='o', label='Waiting Percentage')
    ax_pi.set_xlabel('Instance No')
    ax_pi.set_ylabel('Duration')
    ax_pi2.set_ylabel('Waiting Percentage (%)')
    ax_pi.set_title('Duration and Waiting Percentage Breakdown by Instance')
    ax_pi.legend(loc='upper left')
    ax_pi2.legend(loc='upper right')

    # # Plot the bar chart for Cost
    process_instances_df = process_instances_df.sort_values(by='Cost')
    fig_pi_c, ax_pi_c = plt.subplots(figsize=(10, 6))
    ax_pi_c.bar(process_instances_df['Instance No'], process_instances_df['Cost'], color='#9eb8d9')
    ax_pi_c.set_xlabel('Instance No')
    ax_pi_c.set_ylabel('Cost')
    ax_pi_c.set_title('Cost of Each Instance')

    c1, c2 = st.columns((1,1))
    with c1:
        st.markdown('### Duration of Process Instances')
        st.pyplot(fig_pi)
    with c2:
        st.markdown('### Cost of Process Instances')
        st.pyplot(fig_pi_c)

    # # Plot the waiting time percentage distribution
    waiting_percentage = (process_instances_df['Waiting'] / process_instances_df['Duration']) * 100

    # Replace infinity values with NaN in the waiting percentage column
    waiting_percentage.replace([np.inf, -np.inf], np.nan, inplace=True)

    # Drop rows with NaN values in the waiting percentage column
    waiting_percentage.dropna(inplace=True)
    bins = [i for i in range(0, 101, 10)]
    fig_dist_time, ax_dist_time = plt.subplots(figsize=(10, 6))
    sns.histplot(waiting_percentage, bins=bins, kde=False, color='#427D9D')
    ax_dist_time.set_xlabel('Waiting Percentage Intervals (%)')
    ax_dist_time.set_ylabel('Count of Instances')

    process_instances_df = process_instances_df.sort_values(by='Cost')
    process_instances_df['Cost'].replace([np.inf, -np.inf], np.nan, inplace=True)
    process_instances_df.dropna(subset=['Cost'], inplace=True)

    # Plot the instances cost distribution
    bins = [i for i in range(0, int(process_instances_df['Cost'].max()) + 10, 10)]
    fig_dist_cost, ax_dist_cost = plt.subplots(figsize=(10, 6))
    sns.histplot(process_instances_df['Cost'], bins=bins, kde=False, color='#9eb8d9')
    ax_dist_cost.set_xlabel('Cost Intervals')
    ax_dist_cost.set_ylabel('Count of Instances')

    e1, e2 = st.columns((1,1))
    with e1:
        st.markdown('### Waiting Percentages Among Instances')
        st.pyplot(fig_dist_time)
    with e2:
        st.markdown('### Distribution of Instance Cost')
        st.pyplot(fig_dist_cost)


    # Create a bar chart for activity instances duration
    fig_activity_duration, ax_activity_duration = plt.subplots(figsize=(10, 6))
    colors = ['#F5E8C7', '#ffc7c7', '#61A3BA', '#A25772']
    grouped_data = instance_df.groupby('Activity_Name')
    for (activity_name, group), color in zip(grouped_data, colors):
        total_durations = group.groupby('Instance_No')['Total_Duration'].sum()
        total_durations = total_durations.sort_index()
        total_durations.plot(kind='bar', ax=ax_activity_duration, color=color, label= activity_name)

        ax_activity_duration.set_xlabel('Instance No')
        ax_activity_duration.set_ylabel('Total Duration')
        ax_activity_duration.set_title('Total Duration of Each Activity Instance')
        ax_activity_duration.legend()


    # Create a bar chart for activity instances cost
    instance_df['Cost'] = pd.to_numeric(instance_df['Cost'])
    sorted_instances = instance_df.sort_values(by='Instance_No')
    grouped_data_c = sorted_instances.groupby('Activity_Name')
    fig_cost_breakdown, ax_cost_breakdown = plt.subplots(figsize=(10, 6))
    colors_c = ['#F5E8C7', '#ffc7c7', '#61A3BA', '#A25772']
    bottom = pd.Series(0, index=sorted_instances['Instance_No'].unique())
    for (activity_name, group), color in zip(grouped_data_c, colors_c):
        instance_nos = group['Instance_No'].values
        costs = group['Cost'].values
        ax_cost_breakdown.bar(instance_nos, costs, bottom=bottom[instance_nos], color=color, label=activity_name)
        bottom[instance_nos] += costs

    ax_cost_breakdown.set_xlabel('Instance No')
    ax_cost_breakdown.set_ylabel('Cost')
    ax_cost_breakdown.set_title('Stacked Bar Chart of Costs for Each Activity and Instance')
    ax_cost_breakdown.legend()

    d1, d2 = st.columns((1,1))
    with d1:
        st.markdown('### Duration of Process Instances per Activity')
        st.pyplot(fig_activity_duration)
    with d2:
        st.markdown('### Cost of Process Instances per Activity')
        st.pyplot(fig_cost_breakdown)


    st.markdown(
        """
        <div style="background-color:#D2E0FB; padding: 8px; border-radius: 8px;">
            <h3 style="color: #FFFFFF;">Activity Parameters</h3>
        </div>
        """,
        unsafe_allow_html=True
    ) 

    st.write(f"❗ Time units of this process are in {time_unit}.")

    with st.expander("ℹ️ Access detailed information on process instances."):
        st.write("""
        An activity refers to a specific task, operation, or step within a process that contributes to the overall 
        workflow. Activities are fundamental units that shape the simulation dynamics, influencing costs, durations, 
        and overall process efficiency. Below you may find the following tables offering detailed breakdowns and 
        valuable insights on process activities: 
        - __Cost Parameters of Activities:__ 
            - Total Cost Bar Chart: Bar chart illustrating the total cost associated with each activity. Here you can
            identify cost variations among different activities. 
            - Pointplot of Costs: Pointplot displaying key cost metrics for each activity, including minimum, 
            maximum, median, Q1, Q3, and average values. Here you can assess the variability in cost metrics 
            for each activity.
            - Cost Metric Distribution Box Plot:
            Box plot presenting the distribution of cost metrics for each activity, providing insights into 
            variability and central tendency. Here you can assess the variability in cost metrics 
            for each activity.
        - __Activity Counts and Durations__: 
            - Activity Count Bar Chart: Bar chart displaying the frequency of each activity, indicating how many 
            times each activity is performed. Here you can understand the frequency of each activity. 
            - Boxplot of Total Duration: Box plot presenting the distribution of total duration for each activity, 
            offering insights into the variability of time taken. Here you can identify activities with consistent 
            or varying durations for targeted improvements.
        """)

    sns.set_theme()
    activity_df = activity_df.sort_values(by='Cost Total', ascending=False)
    activity_df_filtered = activity_df.dropna(subset=["Activity Name"])
    activity_df_filtered = activity_df_filtered.sort_values(by='Cost Total', ascending=False)
    st.markdown('### Cost Parameters of Activities')
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    # Bar plot for Total Cost
    axes[0].bar(activity_df_filtered['Activity Name'], activity_df_filtered['Cost Total'], color='#9eb8d9')
    axes[0].set_xlabel('Activity Name')
    axes[0].set_ylabel('Total Cost')
    axes[0].set_title('Total Cost of Each Activity')
    # Pointplot for Cost Metrics
    selected_columns = ['Activity Name', 'Cost Min', 'Cost Max', 'Cost Median', 'Cost Q1', 'Cost Q3', 'Cost Avg']
    selected_df = activity_df[selected_columns].copy()
    melted_df = selected_df.melt(id_vars='Activity Name', var_name='Cost Type', value_name='Cost')
    melted_df['Cost'] = pd.to_numeric(melted_df['Cost'], errors='coerce')
    # Pointplot
    sns.pointplot(x='Activity Name', y='Cost', hue='Cost Type', data=melted_df, dodge=True, ax=axes[1], palette='bwr')
    axes[1].set_title('Pointplot of Costs for Each Activity')
    axes[1].set_xlabel('Activity Name')
    axes[1].set_ylabel('Cost')

    # Boxplot for Cost Metrics
    sns.boxplot(data=instance_df, x="Activity_Name", y="Cost", ax=axes[2], palette={'Ship order':'#A25772', 'Pack order': '#ffc7c7', 'Prepare order for shipment':'#61A3BA', 'Archive order': '#F5E8C7'})
    axes[2].set_title('Cost Metrics Distribution for Each Activity')
    axes[2].set_ylabel('Cost')
    axes[2].set_xlabel('Activity Name')

    # Adjust layout
    plt.tight_layout()
    st.pyplot(fig)

    fig, axes = plt.subplots(1, 2, figsize=(18, 6))
    st.markdown('### Activity Counts and Durations')

    melted_df = pd.melt(activity_count_df, id_vars=["Activity"], var_name="Status", value_name="Count")

    sns.barplot(x="Activity", y="Count", hue="Status", data=melted_df, ax=axes[0], palette='bwr')
    axes[0].set_title("Started and Completed Counts for Each Activity")
    axes[0].set_xlabel("Activity Name")
    axes[0].set_ylabel("Count")
    axes[0].legend(title="Status", loc="upper right")
    sns.boxplot(data=instance_df, x="Activity_Name", y="Total_Duration",  ax=axes[1], palette={'Ship order':'#A25772', 'Pack order': '#ffc7c7', 'Prepare order for shipment':'#61A3BA', 'Archive order': '#F5E8C7'})
    axes[1].set_title('Boxplot of Total Duration for Each Activity')
    axes[1].set_xlabel("Activity Name")
    axes[1].set_ylabel("Total Duration")
    plt.tight_layout()
    st.pyplot(fig)
    

    st.markdown(
        """
        <div style="background-color:#D2E0FB; padding: 8px; border-radius: 8px;">
            <h3 style="color: #FFFFFF;">Resource Parameters</h3>
        </div>
        """,
        unsafe_allow_html=True
    ) 

    st.write(f"❗ Time units of this process are in {time_unit}.")

    with st.expander("ℹ️ Access detailed information on resource parameters."):
        st.write("""
        A resource refers to individuals or entities assigned to specific roles within a process. 
        Resources play a crucial role in the successful execution of activities and contribute to the overall 
        efficiency of the simulated business environment. Below you may find the definition of each table:  
        - __Time Distribution Amoung Resources:__ Illustrates the Time In Use and Time Available for each
        resource. Overlaying line graph indicates the percentage of workload (utilization) for each resource. Here youc can 
        identify underutilized or highly efficient resources for targeted improvements.
        - __Cost Efficiencyvs. Utilization Ratio for Different Resource Types:__ 
        """)

    st.markdown('### Cost and Duration of the Resources')
    fig, axes = plt.subplots(1, 2, figsize=(18, 6))
    # Melt the DataFrame
    melted_df_res = pd.melt(resource_df, id_vars='Resource Type', var_name='Parameter', value_name='Value')
    time_df = melted_df_res[melted_df_res['Parameter'].str.contains('Time')]
    resource_df['Time Workload Perc'] = resource_df['Time Workload'] * 100
    melted_df_res = pd.melt(resource_df, id_vars='Resource Type', var_name='Parameter', value_name='Value')   
    # Bar plot for Time In Use, Time Available, and Workload Perc
    time_data = melted_df_res[melted_df_res['Parameter'].isin(['Time In Use', 'Time Available', 'Time Workload Perc'])]
    sns.barplot(x='Resource Type', y='Value', hue='Parameter', data=time_data, ax=axes[0], palette={'Time In Use':'#AAE3E2', 'Time Available':'#ACB1D6', 'Time Workload Perc':'#BB2525'} )
    # Set y-axis label for the left (bar) y-axis
    axes[0].set_ylabel('Duration')
    ax2 = axes[0].twinx()
    workload_data = melted_df_res[melted_df_res['Parameter'] == 'Time Workload Perc']
    sns.lineplot(x='Resource Type', y='Value', data=workload_data, ax=ax2, marker='o', linestyle='--', color='r')
    ax2.set_ylabel('Workload Perc (%)')
    axes[0].set_title('Time Distribution Amoung Resources')
    axes[0].set_xlabel('Resource Type')

    utilization_table = resource_df[["Resource Type", "Time In Use", "Cost", "Time Workload"]]
    utilization_table.columns = ["Resource Type", "Total Working Time", "Cost", "Utilisation Ratio"]
    merged_df = pd.merge(utilization_table, simulation_input_df, on='Resource Type', suffixes=('_Utilization', '_ResourceInput'))
    scatter_plot = sns.scatterplot(data=merged_df, x='Utilisation Ratio', y='Cost per Hour', ax=axes[1], size='Cost', hue='Resource Type', sizes=(80, 250), palette={'Worker':'#B2A4FF', 'System': '#AAE3E2', 'Robot':'#1640D6'}, legend=False)
    scatter_plot.set(xlabel='Utilization Ratio', ylabel='Cost per Hour')
    axes[1].set_title('Cost Efficiency vs. Utilization Ratio for Different Resource Types')
    axes[1].set_xlabel('Utilization Ratio')
    axes[1].set_ylabel('Cost per Hour')
    for index, row in merged_df.iterrows():
        cost_formatted = '{:.2f}'.format(row['Cost'])  # Format cost with two decimal places
        axes[1].annotate(cost_formatted, (row['Utilisation Ratio'], row['Cost per Hour']), textcoords="offset points", xytext=(5, 0), ha='left')

    unique_resources = merged_df['Resource Type'].unique()
    handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor={'Worker': '#B2A4FF', 'System': '#AAE3E2', 'Robot': '#1640D6'}.get(resource, 'grey'), markersize=10) for resource in unique_resources]
    custom_legend = axes[1].legend(handles, unique_resources, title='Resource Type', loc='upper right')


    st.pyplot(fig)

############################################
#EXTRACT DATA PAGE
############################################

elif sidebar_option == "Extract Data" :
    extract_management()

    st.write(f"❗ Time units of this process are in {time_unit}.")

    # Navigate to the new view to display the dataframes
    st.markdown("## Extracted Data:")
    
    # Display the first set of DataFrames
    st.markdown("### First Set of Dataframes:")
    st.markdown("#### Activity Data:")
    st.write(activity_df)
    st.markdown(download_button(activity_df, "Download Activity Data", "activity_data"), unsafe_allow_html=True)


    st.markdown("#### Resource Data:")
    st.write(resource_df)
    st.markdown(download_button(resource_df, "Download Resource Data", "resource_data"), unsafe_allow_html=True)


    st.markdown("#### Process Data:")
    st.write(process_df)
    st.markdown(download_button(process_df, "Download Process Data", "process_data"), unsafe_allow_html=True)


    st.markdown("#### Simulation Parameters:")
    st.write(simulation_df)
    st.markdown(download_button(simulation_df, "Download Simulation Data", "simulation_data"), unsafe_allow_html=True)


    st.markdown("#### Activity Instances:")
    st.write(instance_df)
    st.markdown(download_button(instance_df, "Download Activity Instance Data", "activity_instance_data"), unsafe_allow_html=True)


    st.markdown("#### Process Instances:")
    st.write(process_instances_df)
    st.markdown(download_button(process_instances_df, "Download Process Instance Data", "process_instance_data"), unsafe_allow_html=True)


    # Display the second set of DataFrames
    st.markdown("### Second Set of Dataframes:")
    st.markdown("#### Activity Data:")
    st.write(activity_df2)
    st.markdown(download_button(activity_df2, "Download Activity Data", "activity_data_2"), unsafe_allow_html=True)


    st.markdown("#### Resource Data:")
    st.write(resource_df2)
    st.markdown(download_button(resource_df2, "Download Resource Data", "resource_data2"), unsafe_allow_html=True)


    st.markdown("#### Process Data:")
    st.write(process_df2)
    st.markdown(download_button(process_df2, "Download Process Data", "process_data2"), unsafe_allow_html=True)


    st.markdown("#### Simulation Parameters:")
    st.write(simulation_df2)
    st.markdown(download_button(simulation_df2, "Download Simulation Data", "simulation_data2"), unsafe_allow_html=True)


    st.markdown("#### Activity Instances:")
    st.write(instance_df2)
    st.markdown(download_button(instance_df2, "Download Activity Instance Data", "activity_instance_data2"), unsafe_allow_html=True)


    st.markdown("#### Process Instances:")
    st.write(process_instances_df2)
    st.markdown(download_button(process_instances_df2, "Download Process Instance Data", "process_instance_data2"), unsafe_allow_html=True)



############################################
#SCENARIO COMPARISON PAGE
############################################

elif sidebar_option == "Scenario Comparisons" :
    page_comparison()

    comparison_choice = st.sidebar.selectbox("Select Comparison Type", ["Cost", "Time"])

    if comparison_choice == "Cost":
         # Display the resource inputs of simulation
        st.markdown("Simulation Inputs of Resource:")
        st.write(rounded_resource_input_comparison_df)
        # Display the resource cost comparison table with conditional formatting
        st.markdown("Resource Cost Comparison Table:")
        st.write(rounded_resource_comparison_df)
        # Display the activity cost comparison table with conditional formatting
        st.markdown("Activity Cost Comparison Table:")
        st.write(rounded_activity_comparison_df)

        #st.title('Cost Efficiency Comparison by Resource Type and Scenario')
        #fig, ax = plt.subplots(figsize=(12, 8))
        #bar_width = 0.35
        #index = range(len(merged_df_resource_cost))
        #bar_instance = ax.bar(index, merged_df_resource_cost['CostperInstance_Scenario1'], bar_width, label='Scenario 1 - Cost per Instance', color= '#AAE3E2')
        #bar_instance = ax.bar(index, merged_df_resource_cost['CostperInstance_Scenario2'], bar_width, label='Scenario 2 - Cost per Instance', bottom=merged_df_resource_cost['CostperInstance_Scenario1'], color= '#ACB1D6')
        #bar_hourly = ax.bar([i + bar_width for i in index], merged_df_resource_cost['Cost per Hour_Scenario1'], bar_width, label='Scenario 1 - Cost per Hour', color= '#B2A4FF')
        #bar_hourly = ax.bar([i + bar_width for i in index], merged_df_resource_cost['Cost per Hour_Scenario2'], bar_width, label='Scenario 2 - Cost per Hour', bottom=merged_df_resource_cost['Cost per Hour_Scenario1'], color= '#CE5A67')
        #ax.set_xlabel('Resource Type')
        #ax.set_ylabel('Cost')
        #ax.set_title('Cost Efficiency by Resource Type and Scenario')
        #ax.set_xticks([i + bar_width / 2 for i in index])
        #ax.set_xticklabels(merged_df_resource_cost['Resource Type'])
        #ax.legend()
        #st.pyplot(fig)
        
    elif comparison_choice == "Time":
        st.write(f"❗ Time units of this process are in {time_unit}.")
         # Display the resource duration comparison table with conditional formatting
        st.markdown("Resource Duration Comparison Table:")
        st.write(rounded_resource_t_comparison_df)
        # Display the activity duration comparison table with conditional formatting
        st.markdown("Activity Duration Comparison Table:")
        st.write(rounded_activity_duration_comparison)

        
