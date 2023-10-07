import streamlit as st

# Define the custom component
def bpmn_viewer(parsed_bpmn_xml):
    # Use st.components to create the custom component
    bpmn_component = st.components.v1.html(
        f"""
        <!-- Your BPMN diagram rendering code using bpmn-js goes here -->
        <div id="bpmn-diagram" style="margin: 0 auto; text-align: center;"></div>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/bpmn-js/11.3.2/bpmn-viewer.min.js"></script>
        <script>
            var viewer = new BpmnJS({{ container: "#bpmn-diagram" }});

            // Replace this with your BPMN XML data
            var bpmnXml = `{parsed_bpmn_xml}`;

            viewer.importXML(bpmnXml, function(err) {{
                if (!err) {{
                    console.log('BPMN diagram displayed.');

                    // Add click event listener to BPMN elements
                    viewer.get('canvas').on('element.click', function(event) {{
                        var element = event.element;
                        if (element.type === 'bpmn:Task') {{
                            // Send the activity ID to Streamlit
                            parent.postMessage({{ activityId: element.id }}, '*');
                        }}
                    }});
                }} else {{
                    console.error('Error displaying BPMN diagram:', err);
                }}
            }});
        </script>
        """,
        height=600,  # Set the height of the component
    )
    return bpmn_component