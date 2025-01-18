// Declare global variables
var outlets = 1; // Number of outlets in this JavaScript object

// Function called whenever a message is received
function anything() {
    var msg = messagename; // Get the received message
    var args = arrayfromargs(arguments); // Get the arguments, if any

    // Example: If the message is "/bang_toggle"
    if (msg === "/signal") {
        post("Received message: " + msg + "\n");
        bangToggle(); // Call a custom function to activate the toggle
    } else {
        post("Unrecognized message: " + msg + "\n");
    }
}

// Custom function to bang a toggle
function bangToggle() {
    outlet(0, "bang"); // Send a "bang" message through the outlet
}
