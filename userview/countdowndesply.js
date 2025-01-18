// Save this file as countdown.js in your Max MSP search path

// Import Jitter objects
var jit_gl_render = new JitterObject("jit.gl.render", "countdown");
var jit_gl_text = new JitterObject("jit.gl.text", "countdown");
var jit_gl_window = new JitterObject("jit.window", "countdown");

// Set up rendering properties
jit_gl_text.fontsize = 150;
jit_gl_text.color = [1, 1, 1, 1];
jit_gl_text.align = "center";
jit_gl_text.position = [0, 0, 0];

jit_gl_window.size = [400, 400];
jit_gl_window.floating = 1;

// Countdown variables
var countdownNumbers = [3, 2, 1];
var index = 0;
var countdownInterval = 1000; // 1 second
var countdownTask;

// Function to display a number
function displayNumber(number) {
    jit_gl_render.erase();
    jit_gl_text.text = number.toString();
    jit_gl_render.drawclients();
    jit_gl_render.swap();
}

// Function to start the countdown
function startCountdown() {
    index = 0;

    // Stop any previous task
    if (countdownTask) countdownTask.cancel();

    // Create a new task for the countdown
    countdownTask = new Task(function () {
        if (index < countdownNumbers.length) {
            displayNumber(countdownNumbers[index]);
            index++;
        } else {
            countdownTask.cancel(); // Stop the task when done
        }
    });
    countdownTask.interval = countdownInterval;
    countdownTask.repeat();
}

// Handle messages from Max
function bang() {
    startCountdown();
}
