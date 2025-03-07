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

    lines = textarea.value.split("\n").length;

    // If the textarea is truly empty (no characters at all), set it to 10 lines
    if (textarea.value.length === 0) {
        lines = 10;
    } else {
        // Ensure at least 1 line is always displayed
        lines = Math.max(lines, 1);
    }

    let lineNumbersHTML = "";
    for (let i = 1; i <= lines; i++) {
        lineNumbersHTML += i + "<br>";
    }

    lineNumbers.innerHTML = lineNumbersHTML;
}

// Update line numbers on input change
document.getElementById("machine-definition").addEventListener("input", updateLineNumbers);

// Ensure scrolling syncs properly
function syncScroll() {
    const textarea = document.getElementById("machine-definition");
    const lineNumbers = document.getElementById("line-numbers");
    lineNumbers.scrollTop = textarea.scrollTop;
}

// Attach event listeners
document.getElementById("machine-definition").addEventListener("scroll", syncScroll);

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