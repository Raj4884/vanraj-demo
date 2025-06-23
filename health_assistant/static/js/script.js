document.addEventListener('DOMContentLoaded', function() {
    // Load medications on page load
    loadMedications();
    
    // Set up event listeners
    document.getElementById('diagnosis-form').addEventListener('submit', handleDiagnosis);
    document.getElementById('test-message-form').addEventListener('submit', sendTestMessage);
    document.getElementById('save-medication').addEventListener('click', saveMedication);
    document.getElementById('med-frequency').addEventListener('change', toggleDaysSelection);
});

// Toggle days selection based on frequency
function toggleDaysSelection() {
    const frequency = document.getElementById('med-frequency').value;
    const daysSelection = document.getElementById('days-selection');
    
    if (frequency === 'weekly') {
        daysSelection.classList.remove('d-none');
    } else {
        daysSelection.classList.add('d-none');
    }
}

// Load medications from the server
function loadMedications() {
    fetch('/api/medications')
        .then(response => response.json())
        .then(medications => {
            const medicationsList = document.getElementById('medications-list');
            
            if (medications.length === 0) {
                medicationsList.innerHTML = '<p>No medications added yet.</p>';
                return;
            }
            
            let html = '';
            medications.forEach(med => {
                html += `
                    <div class="medication-item">
                        <div class="d-flex justify-content-between">
                            <h3 class="h6 mb-1">${med.name}</h3>
                            <span class="delete-med" onclick="deleteMedication(${med.id})">×</span>
                        </div>
                        <p class="mb-1">${med.dosage || ''}</p>
                        <p class="mb-1">Time: ${med.time}</p>
                        <p class="mb-1">Frequency: ${med.frequency}</p>
                        <p class="mb-0 small text-muted">${med.instructions || ''}</p>
                    </div>
                `;
            });
            
            medicationsList.innerHTML = html;
        })
        .catch(error => {
            console.error('Error loading medications:', error);
            document.getElementById('medications-list').innerHTML = 
                '<p class="text-danger">Error loading medications. Please try again.</p>';
        });
}

// Save a new medication
function saveMedication() {
    const name = document.getElementById('med-name').value;
    const dosage = document.getElementById('med-dosage').value;
    const time = document.getElementById('med-time').value;
    const frequency = document.getElementById('med-frequency').value;
    const instructions = document.getElementById('med-instructions').value;
    
    if (!name || !time || !frequency) {
        alert('Please fill in all required fields');
        return;
    }
    
    // Get selected days if frequency is weekly
    let days = [];
    if (frequency === 'weekly') {
        const dayCheckboxes = document.querySelectorAll('#days-selection input[type="checkbox"]:checked');
        if (dayCheckboxes.length === 0) {
            alert('Please select at least one day of the week');
            return;
        }
        
        dayCheckboxes.forEach(checkbox => {
            days.push(checkbox.value);
        });
    }
    
    const medicationData = {
        name,
        dosage,
        time,
        frequency,
        instructions,
        days
    };
    
    fetch('/api/medications', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(medicationData)
    })
    .then(response => response.json())
    .then(data => {
        // Close modal and reload medications
        const modal = bootstrap.Modal.getInstance(document.getElementById('addMedicationModal'));
        modal.hide();
        
        // Reset form
        document.getElementById('add-medication-form').reset();
        
        // Reload medications
        loadMedications();
    })
    .catch(error => {
        console.error('Error saving medication:', error);
        alert('Error saving medication. Please try again.');
    });
}

// Delete a medication
function deleteMedication(id) {
    if (!confirm('Are you sure you want to delete this medication?')) {
        return;
    }
    
    fetch(`/api/medications/${id}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        loadMedications();
    })
    .catch(error => {
        console.error('Error deleting medication:', error);
        alert('Error deleting medication. Please try again.');
    });
}

// Handle diagnosis form submission
function handleDiagnosis(event) {
    event.preventDefault();
    
    const symptoms = document.getElementById('symptoms').value;
    
    if (!symptoms) {
        alert('Please enter your symptoms');
        return;
    }
    
    // Show loading state
    document.getElementById('diagnosis-content').innerHTML = '<p>Analyzing symptoms...</p>';
    document.getElementById('diagnosis-results').classList.remove('d-none');
    
    fetch('/api/diagnose', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ symptoms })
    })
    .then(response => response.json())
    .then(data => {
        let html = `<p><strong>Symptoms:</strong> ${data.symptoms}</p>`;
        
        html += '<p><strong>Possible conditions:</strong></p><ul>';
        data.possible_conditions.forEach(condition => {
            html += `<li>${condition}</li>`;
        });
        html += '</ul>';
        
        html += '<p><strong>Recommendations:</strong></p><ul>';
        data.recommendations.forEach(recommendation => {
            html += `<li>${recommendation}</li>`;
        });
        html += '</ul>';
        
        if (data.seek_medical_attention) {
            html += `
                <div class="urgent-warning">
                    <strong>Important:</strong> Your symptoms may require immediate medical attention. 
                    Please contact a healthcare provider or emergency services right away.
                </div>
            `;
        }
        
        html += `<div class="disclaimer">${data.disclaimer}</div>`;
        
        document.getElementById('diagnosis-content').innerHTML = html;
    })
    .catch(error => {
        console.error('Error getting diagnosis:', error);
        document.getElementById('diagnosis-content').innerHTML = 
            '<p class="text-danger">Error analyzing symptoms. Please try again.</p>';
    });
}

// Send a test message
function sendTestMessage(event) {
    event.preventDefault();
    
    const message = document.getElementById('test-message').value;
    
    if (!message) {
        alert('Please enter a message');
        return;
    }
    
    // Show loading state
    document.getElementById('message-status').innerHTML = '<p>Sending message...</p>';
    
    fetch('/api/send-test-message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            document.getElementById('message-status').innerHTML = 
                '<p class="success-message">Message sent successfully!</p>';
            document.getElementById('test-message').value = '';
        } else {
            document.getElementById('message-status').innerHTML = 
                `<p class="error-message">Error: ${data.message}</p>`;
        }
    })
    .catch(error => {
        console.error('Error sending message:', error);
        document.getElementById('message-status').innerHTML = 
            '<p class="error-message">Error sending message. Please try again.</p>';
    });
}