// Simple search functionality for the patient list
document.addEventListener('DOMContentLoaded', function() {
    
    document.querySelectorAll('.sortable').forEach(header => {
        header.addEventListener('click', function() {
            const sortBy = this.dataset.sort;
            let sortOrder = 'asc';
            
            if (this.classList.contains('sorted-asc')) {
                sortOrder = 'desc';
            } else if (this.classList.contains('sorted-desc')) {
                sortOrder = 'asc';
            }
            
            const url = new URL(window.location.href);
            url.searchParams.set('sort', sortBy);
            url.searchParams.set('order', sortOrder);
            window.location.href = url.toString();
        });
    });
    
    const searchInput = document.getElementById('searchInput');
    
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value.toLowerCase();
            const rows = document.querySelectorAll('.patient-row');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(searchTerm) ? '' : 'none';
            });
        });
    }
    
    // Simple feedback button interactions
    const feedbackButtons = document.querySelectorAll('.feedback-button');
    feedbackButtons.forEach(button => {
        button.addEventListener('click', function() {
            feedbackButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
        });
    });

    // Make feedback buttons interactive
    document.querySelectorAll('.feedback-buttons button').forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from siblings
            this.parentNode.querySelectorAll('button').forEach(btn => {
                btn.classList.remove('active');
            });
            // Add to clicked button
            this.classList.add('active');
        });
    });
    
    function calculateBMI() {
    const weight = parseFloat(document.getElementById('weight').value);
    const height = parseFloat(document.getElementById('height').value) / 100; // Convert cm to m
    
    if (weight && height) {
        const bmi = weight / (height * height);
        document.getElementById('bmi').value = bmi.toFixed(1);
    } else {
        alert('Please enter both weight and height first');
    }
}


});
