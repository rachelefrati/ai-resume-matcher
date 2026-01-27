// ---------------------------
// Elements
// ---------------------------
const cvInput = document.getElementById("cvInput");
const selectedFileName = document.getElementById("selectedFileName");

// Show selected CV file name in Step 2
cvInput.addEventListener("change", () => {
    if (cvInput.files.length > 0) {
        selectedFileName.textContent = `Selected file: ${cvInput.files[0].name}`;
    } else {
        selectedFileName.textContent = "";
    }
});

// ---------------------------
// Functions
// ---------------------------

// Send CV file + job description to backend
async function sendData() {
    const resultElement = document.getElementById("result");
    const jobDescription = document.getElementById("jobText").value.trim();
    const cvFile = cvInput.files[0];

    if (!cvFile) {
        resultElement.innerHTML = `<div class="text-danger">Please select a CV file first!</div>`;
        return;
    }
    if (!jobDescription) {
        resultElement.innerHTML = `<div class="text-danger">Please enter a job description!</div>`;
        return;
    }

    // Show Step 3 and hide Step 2
    document.getElementById('step2').style.display = 'none';
    document.getElementById('step3').style.display = 'block';

    // Show loading state
    resultElement.innerHTML = `<div class="text-center">Analyzing...</div>`;

    // Prepare FormData
    const formData = new FormData();
    formData.append("resume_file", cvFile);
    formData.append("job_description", jobDescription);

    try {
        const response = await fetch("http://127.0.0.1:8000/match-file", {
            method: "POST",
            body: formData
        });

        if (!response.ok) throw new Error(`Server error: ${response.status}`);

        const data = await response.json();

        // Determine card border based on overall similarity
        let borderClass = "border-danger";
        const scorePercent = data.match_score;
        if (scorePercent > 80) borderClass = "border-success";
        else if (scorePercent > 50) borderClass = "border-warning";

        // Build HTML with top chunks
        let html = `
            <div class="card ${borderClass} mb-3">
                <div class="card-body">
                    <h5 class="card-title">Match Score: ${scorePercent}%</h5>
                    <p class="card-text">${data.summary}</p>
                    <h6 class="card-subtitle mb-2 text-muted">Top Matching Resume Chunks</h6>
                    <ul>
        `;

        data.top_matches.forEach(chunkObj => {
            html += `<li>${chunkObj.chunk} <strong>(Similarity: ${Math.round(chunkObj.similarity * 100)}%)</strong></li>`;
        });

        html += `
                    </ul>
                </div>
            </div>
        `;

        resultElement.innerHTML = html;

    } catch (error) {
        console.error(error);
        resultElement.innerHTML = `<div class="text-danger">Error: ${error.message}</div>`;
    }
}

// ---------------------------
// Navigation functions (already in index.html)
// ---------------------------
function goToStep2() {
    document.getElementById('step1').style.display = 'none';
    document.getElementById('step2').style.display = 'block';

    // Show file name if already selected
    if (cvInput.files.length > 0) {
        selectedFileName.textContent = `Selected file: ${cvInput.files[0].name}`;
    }
}

function goToStep1() {
    document.getElementById('step3').style.display = 'none';
    document.getElementById('step1').style.display = 'block';
}
