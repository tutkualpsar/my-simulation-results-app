import xml.etree.ElementTree as ET
import pandas as pd

def parce_resource_input(xml_file):
    with open(xml_file, "r") as xml_contents:
        uploaded_xml_file = xml_contents.read()

    if uploaded_xml_file is not None:
        # Parse the XML content from the string
        root = ET.fromstring(uploaded_xml_file)

        # Initialize lists to store data
        resource_types = []
        quantities = []
        costs = []
        business_hours = []

        # Iterate over each dynamicResource element
        for dynamic_resource in root.findall(".//{http://bsim.hpi.uni-potsdam.de/scylla/simModel}dynamicResource"):
            resource_type = dynamic_resource.get("id")
            quantity = float(dynamic_resource.get("defaultQuantity"))
            cost = float(dynamic_resource.get("defaultCost"))

            # Calculate business hours in seconds
            business_hours_in_seconds = sum(
                (int(item.get("endTime").split(":")[0]) * 3600 + int(item.get("endTime").split(":")[1]) * 60) -
                (int(item.get("beginTime").split(":")[0]) * 3600 + int(item.get("beginTime").split(":")[1]) * 60)
                for item in dynamic_resource.findall(".//{http://bsim.hpi.uni-potsdam.de/scylla/simModel}timetableItem")
            )

            resource_types.append(resource_type)
            quantities.append(quantity)
            costs.append(cost)
            business_hours.append(business_hours_in_seconds)

        # Create the DataFrame
        resource_input = pd.DataFrame({
            'Resource Type': resource_types,
            'Quantity': quantities,
            'Cost per Hour': costs
        })

        return resource_input

