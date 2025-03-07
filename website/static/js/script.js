document.addEventListener("DOMContentLoaded", function () {

    // Tab key handling
    document.getElementById("machine-definition").addEventListener("keydown", function(event) {
        if (event.key === "Tab") {
            var textarea = event.target;
            if (!textarea.value) {
                event.preventDefault();
                let placeholderText = textarea.placeholder.trim().split("\n");
                placeholderText.pop(); // Remove last line (comment)
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

    // Textfield line numbers handling
    function updateLineNumbers() {
        const textarea = document.getElementById("machine-definition");
        const lineNumbers = document.getElementById("line-numbers");

        lines = textarea.value.split("\n").length;

        if (textarea.value.length === 0) {
            lines = 10;
        } else {
            lines = Math.max(lines, 1);
        }

        let lineNumbersText = "";
        for (let i = 1; i <= lines; i++) {
            lineNumbersText += i + "<br>";
        }

        lineNumbers.innerHTML = lineNumbersText;
    }

    function syncScroll() {
        const textarea = document.getElementById("machine-definition");
        const lineNumbers = document.getElementById("line-numbers");
        lineNumbers.scrollTop = textarea.scrollTop;
    }

    function preloadLineNumbers(count) {
        let lineNumbersText = "";
        for (let i = 1; i <= count; i++) {
            lineNumbersText += i + "<br>";
        }
        document.getElementById("line-numbers").innerHTML = lineNumbersText;
    }

    document.getElementById("machine-definition").addEventListener("input", updateLineNumbers);
    document.getElementById("machine-definition").addEventListener("scroll", syncScroll);
    preloadLineNumbers(10);
});