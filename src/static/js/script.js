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

    var inputIndex = document.getElementById("input-string");
    var inputMulti = document.getElementById("input-strings");

    if (inputIndex) {
        inputIndex.addEventListener("keydown", function(event) {
            if (event.key === "Tab") {
                var textarea = event.target;
                if (!textarea.value) {
                    event.preventDefault();
                    textarea.value = "000111";
                }
            }
        });
    }

    if (inputMulti) {
        inputMulti.addEventListener("keydown", function(event) {
            if (event.key === "Tab") {
                var textarea = event.target;
                if (!textarea.value) {
                    event.preventDefault();
                    textarea.value = "01\n000111\n0000000011111111";
                }
            }
        });
    }

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
    const mdContent = document.getElementById("machine-definition").getAttribute("data-md");
    preloadLineNumbers(mdContent ? mdContent.split("\n").length : 10);
    
    const inputContainer = document.getElementById("input-container");
    if (inputContainer) {
        const inputString = inputContainer.getAttribute("data-input-string") || "";
        let index = parseInt(inputContainer.getAttribute("data-index"), 10);

        updateInputDisplay(inputString, index);
    }

    function updateInputDisplay(input_string, index) {
        const beforeElement = document.getElementById("input-before");
        const highlightElement = document.getElementById("input-highlight");
        const afterElement = document.getElementById("input-after");
        if (!input_string) {
            beforeElement.innerHTML = "<b>##</b>";
            highlightElement.innerHTML = "";
            afterElement.innerHTML = "";
            return;
        }

        if (index >= input_string.length || index < 0) {
            beforeElement.innerHTML = input_string;
            highlightElement.innerHTML = "";
            afterElement.innerHTML = "";
            return;
        }
    
        beforeElement.innerHTML = input_string.slice(0, index);
        highlightElement.innerHTML = input_string.charAt(index);
        afterElement.innerHTML = input_string.slice(index + 1);
    }

    const eventSource = new EventSource("/stream");
    
    eventSource.onmessage = function(event) {
        try {
            const data = JSON.parse(event.data);
            
            updateInputDisplay(data.input_string, data.index);
            document.getElementById("memory_structures").innerHTML = data.memory_structures || "<b>[ ∅ ]</b>";
            document.getElementById("output").innerText = data.output || " ";
            document.getElementById("current_state").innerText = data.current_state || "∅";
            document.getElementById("step_count").innerText = data.step_count || "0";
            if (data.finished === true) {
                document.getElementById("status").innerText = data.accepted ? "halt-accept" : "halt-reject";
            }
            document.getElementById("message").innerText = data.message || "";
    
            if (data.finished) {
                eventSource.close();  // Stop listening when finished
            }
        } catch (error) {
            console.error("Error processing incoming data:", error);
        }
    };
    
    eventSource.onerror = function(error) {
        console.error("EventSource failed:", error);
        eventSource.close();
    };
    
});