document.addEventListener("DOMContentLoaded", function () {

document.getElementById("machine-definition").addEventListener("keydown", function(event) {
    if (event.key === "Tab") {

        var textarea = event.target;
        if (!textarea.value) {
            event.preventDefault();
            let placeholderText = textarea.placeholder.trim().split("\n");
            placeholderText.pop(); // Remove the last line (comment)
            placeholderText.pop(); // Remove extra line
            textarea.value = placeholderText.join("\n");
            updateLineNumbers();
        }
    }
});

document.getElementById("input-string").addEventListener("keydown", function(event) {
    if (event.key === "Tab") {
        var textarea = event.target;
        if (!textarea.value) {
            event.preventDefault();
            textarea.value = "1110110101";
        }
    }
});

function updateLineNumbers() {
    const textarea = document.getElementById("machine-definition");
    const lineNumbers = document.getElementById("line-numbers");

    // Count lines
    const lines = textarea.value.split("\n").length;
    let lineNumbersHTML = "";
    for (let i = 1; i <= lines; i++) {
        lineNumbersHTML += i + "<br>";
    }

    lineNumbers.innerHTML = lineNumbersHTML;
}

function syncScroll() {
    const textarea = document.getElementById("machine-definition");
    const lineNumbers = document.getElementById("line-numbers");
    lineNumbers.scrollTop = textarea.scrollTop;
}

function preloadLineNumbers(count) {
    let lineNumbersHTML = "";
    for (let i = 1; i <= count; i++) {
        lineNumbersHTML += i + "<br>";
    }
    document.getElementById("line-numbers").innerHTML = lineNumbersHTML;
}

// Preload 15 lines for placeholder (adjust as needed)
preloadLineNumbers(10);

});