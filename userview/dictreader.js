 
// Initialize UDP connection

var udpPort = 8000; // Replace with your target port
var oscAddress = "/dictData"; // OSC address prefix

// Access the dict named "myDataDict"
function sendDictOSC() {
    // Load the existing dict in Max
    var myDict = new Dict("hands_landmarkdict");

    // Get keys in the dictionary
    var keys = myDict.getkeys();
    if (keys === null) {
        post("The dictionary is empty or does not exist.\n");
        return;
    }

    // Loop through each key-value pair and send it over OSC
    for (var i = 0; i < keys.length; i++) {
        var key = keys[i];
        var value = myDict.get(key);

        // Create OSC message
        outlet(0, oscAddress, key, value);
    }
}

function sendDictAsJSON() {
    // Load the existing dict in Max
    var myDict = new Dict("posedict");

    // Convert the dictionary to JSON
    var jsonString = myDict.stringify();
	//post("jsonString: " + jsonString+ "\n");

    // Send the JSON string as a single OSC message
    outlet(0, "/dictData", jsonString);
}

// Trigger the function from Max
function bang() {
    //sendDictOSC();
	sendDictAsJSON();
}
