// script.js

async function classifyText() {
    let text = document.getElementById("inputText").value;
    if (!text.trim()) {
        alert("Please enter a message to classify.");
        return;
    }

    try {
        let response = await fetch("http://127.0.0.1:5000/predict", {  // Local Flask API URL
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text: text })
        });

        let result = await response.json();
        document.getElementById("result").innerText = "Prediction: " + result.prediction;
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("result").innerText = "Error in classification. Try again!";
    }
}

async function classifyCSV() {
    let fileInput = document.getElementById("csvInput");
    if (fileInput.files.length === 0) {
        alert("Please select a CSV file to classify.");
        return;
    }

    let file = fileInput.files[0];
    let formData = new FormData();
    formData.append("file", file);

    try {
        let response = await fetch("http://127.0.0.1:5000/predict-csv", {  // Local Flask API URL
            method: "POST",
            body: formData
        });

        let result = await response.json();
        document.getElementById("result").innerText = "CSV processed. Check console for results.";
        console.log("CSV Classification Result:", result);
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("result").innerText = "Error in processing CSV file. Try again!";
    }
}
