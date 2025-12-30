async function sendData() {
    const resultElement = document.getElementById("result");
    const jobDescription = document.getElementById("jobText").value;
    const cvFile = document.getElementById("cvInput").files[0];

    if (!cvFile) {
        resultElement.textContent = "Please select a CV file first!";
        return;
    }

    const reader = new FileReader();
    reader.onload = async function() {
        const resumeText = reader.result;

        try {
            const response = await fetch("http://127.0.0.1:8000/match", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    resume_text: resumeText,
                    job_description: jobDescription
                })
            });

            if (!response.ok) throw new Error("Network response was not ok");

            const data = await response.json();

            // Build HTML for results
            let html = `<p><strong>Score:</strong> ${data.score}%</p>`;
            html += `<p><strong>Feedback:</strong> ${data.feedback}</p>`;
            if (data.missing_skills && data.missing_skills.length > 0) {
                html += `<p><strong>Missing Skills:</strong></p><ul>`;
                data.missing_skills.forEach(skill => {
                    html += `<li>${skill}</li>`;
                });
                html += `</ul>`;
            }

            resultElement.innerHTML = html;

            // Show Step 3
            document.getElementById('step2').style.display = 'none';
            document.getElementById('step3').style.display = 'block';

        } catch (error) {
            resultElement.textContent = "Error: " + error.message;
        }
    };

    reader.readAsText(cvFile);
}
