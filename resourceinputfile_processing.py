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
        resource_input= []

        # Iterate over each dynamicResource element
        for dynamic_resource in root.findall(".//{http://bsim.hpi.uni-potsdam.de/scylla/simModel}dynamicResource"):
            resource_type = dynamic_resource.get("id")
            quantity = float(dynamic_resource.get("defaultQuantity"))
            cost = float(dynamic_resource.get("defaultCost"))

            resource_types.append(resource_type)
            quantities.append(quantity)
            costs.append(cost)

        # Create the DataFrame
        resource_input = pd.DataFrame({
            'Resource Type': resource_types,
            'Quantity': quantities,
            'Cost': costs
        })

        return resource_input