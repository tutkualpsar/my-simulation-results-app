// bpmn_viewer.js

// Import bpmn-js library
import BpmnViewer from 'bpmn-js';

// Initialize bpmn-js
var viewer = new BpmnViewer({
    container: '#bpmn-diagram'
});

// Load and display the uploaded BPMN XML
viewer.importXML(parsedBpmnXml, function(err) {
    if (!err) {
        console.log('BPMN diagram displayed.');
        
        // Add click event listener to BPMN elements
        viewer.get('canvas').on('element.click', function(event) {
            var element = event.element;
            if (element.type === 'bpmn:Task') {
                // Send the activity ID to Streamlit
                parent.postMessage({ activityId: element.id }, '*');
            }
        });
    } else {
        console.error('Error displaying BPMN diagram:', err);
    }
});



