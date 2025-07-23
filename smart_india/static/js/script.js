async function loadDashboard() {
    if (document.getElementById('dashboard-content')) {
        const response = await fetch('/dashboard_data');
        const data = await response.json();
        const dashboardContent = document.getElementById('dashboard-content');
        dashboardContent.innerHTML = `
            <p><strong>User ID:</strong> ${data.user_id}</p>
            <p><strong>Username:</strong> ${data.username}</p>
            <h4>Recommendations:</h4>
            <ul>
                ${data.recommendations.map(rec => `<li>${rec}</li>`).join('')}
            </ul>
            <h4>Progress:</h4>
            <p><strong>Courses Completed:</strong> ${data.progress.courses_completed}</p>
            <p><strong>Skills Acquired:</strong> ${data.progress.skills_acquired.join(', ')}</p>
            <p><strong>Resume Score:</strong> ${data.progress.resume_score}</p>
        `;
    }
}

document.addEventListener('DOMContentLoaded', loadDashboard);

if (document.getElementById('send-btn')) {
    document.getElementById('send-btn').addEventListener('click', async () => {
        const userInput = document.getElementById('user-input');
        const message = userInput.value;
        if (message.trim() === '') {
            return;
        }

        const chatBox = document.getElementById('chat-box');
        const userMessage = document.createElement('div');
        userMessage.textContent = "You: " + message;
        chatBox.appendChild(userMessage);

        const response = await fetch('/get_advice', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();
        const botMessage = document.createElement('div');
        botMessage.textContent = "Bot: " + data.advice;
        chatBox.appendChild(botMessage);

        userInput.value = '';
    });
}

if (document.getElementById('analyze-skills-btn')) {
    document.getElementById('analyze-skills-btn').addEventListener('click', async () => {
        const userSkillsInput = document.getElementById('user-skills');
        const desiredCareerInput = document.getElementById('desired-career');

        const userSkills = userSkillsInput.value.split(',').map(s => s.trim());
        const desiredCareer = desiredCareerInput.value;

        const response = await fetch('/analyze_skills', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_skills: userSkills,
                desired_career: desiredCareer
            })
        });

        const data = await response.json();
        const resultDiv = document.getElementById('skill-analysis-result');
        resultDiv.innerHTML = `
            <h3>Analysis for ${desiredCareer}</h3>
            <p><strong>Required Skills:</strong> ${data.required_skills.join(', ')}</p>
            <p><strong>Missing Skills:</strong> ${data.missing_skills.join(', ')}</p>
        `;
    });
}

if (document.getElementById('screen-resume-btn')) {
    document.getElementById('screen-resume-btn').addEventListener('click', async () => {
        const resumeFileInput = document.getElementById('resume-file');
        const resumeFile = resumeFileInput.files[0];

        if (!resumeFile) {
            alert('Please select a resume file.');
            return;
        }

        const formData = new FormData();
        formData.append('resume', resumeFile);

        const response = await fetch('/screen_resume', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        const resultDiv = document.getElementById('resume-screening-result');
        resultDiv.innerHTML = `
            <h3>Resume Screening Result</h3>
            <p><strong>Filename:</strong> ${data.filename}</p>
            <p><strong>Content Length:</strong> ${data.content_length}</p>
            <p><strong>Feedback:</strong> ${data.feedback}</p>
        `;
    });
}

if (document.getElementById('get-local-opportunities-btn')) {
    document.getElementById('get-local-opportunities-btn').addEventListener('click', () => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(async (position) => {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;

                const response = await fetch('/get_local_opportunities', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ latitude, longitude })
                });

                const data = await response.json();
                const resultDiv = document.getElementById('local-opportunities-result');
                resultDiv.innerHTML = `
                    <h3>Local Opportunities</h3>
                    <p><strong>Local Job Market:</strong> ${data.local_job_market}</p>
                    <p><strong>Government Schemes:</strong> ${data.government_schemes}</p>
                `;
            });
        } else {
            alert("Geolocation is not supported by this browser.");
        }
    });
}
