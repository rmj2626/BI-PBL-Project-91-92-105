document.addEventListener('DOMContentLoaded', function() {
    // Load default content for Dashboard
    loadDashboardContent();

    // Handle Dashboard button click
    document.querySelector('.dashboard_btn').addEventListener('click', function() {
        loadDashboardContent();
        setActiveButton(this);
        showGraphTypeButtons('dashboard-graph');
    });

    // Handle Predictive Analysis button click
    document.querySelector('.predictive_btn').addEventListener('click', function() {
        loadPredictiveContent();
        setActiveButton(this);
        showGraphTypeButtons('predictive-graph');
    });

    // Handle graph type selection for dashboard
    document.querySelectorAll('.dashboard-graph button').forEach(btn => {
        btn.addEventListener('click', function () {
            document.querySelectorAll('.dashboard-graph button').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            generateChart(); // Generate chart on graph type selection for dashboard
        });
    });

    // Handle graph type selection for predictive analysis
    document.querySelectorAll('.predictive-graph button').forEach(btn => {
        btn.addEventListener('click', function () {
            document.querySelectorAll('.predictive-graph button').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            predictChart(); // Generate chart on graph type selection for predictive analysis
        });
    });

    // Handle change of Visualization Type dropdown
    document.querySelector('#visual-select').addEventListener('change', function() {
        setDefaultYearsForViewsByDay(this.value);
    });    
});

// Set default years for "Views by Day Type" visualization
function setDefaultYearsForViewsByDay(visualizationType) {
    const fromSelect = document.querySelector('#from-select');
    const toSelect = document.querySelector('#to-select');
    
    if (visualizationType === 'views_by_day') {
        // Set default years when "Views by Day Type" is selected
        fromSelect.value = '2022';
        toSelect.value = '2024';
    } else {
        // Reset to empty values for other visualization types
        fromSelect.value = '';
        toSelect.value = '';
    }
}

function setActiveButton(button) {
    document.querySelectorAll('.sidebar button').forEach(btn => btn.classList.remove('active'));
    button.classList.add('active');
}

function showGraphTypeButtons(graphTypeClass) {
    document.querySelectorAll('.typeOfGraph').forEach(div => div.style.display = 'none');
    document.querySelector(`.${graphTypeClass}`).style.display = 'flex';
}

function loadDashboardContent() {
    const content = `
        <div class="filters">
            <div class="filter1">
                <p>Visualization Type</p>
                <select id="visual-select">
                    <option value="">--Choose an option--</option>
                    <option value="views">Views Over Time</option>
                    <option value="likes_vs_comments">Likes vs Comments</option>
                    <option value="duration">Video Duration</option>
                    <option value="view_to_like_ratio">View-to-Like Ratio Over Time</option>
                    <option value="tag_count">Tag Count Over Time</option>
                    <option value="words_in_title">Words in Title Over Time</option>
                    <option value="views_by_day">Views by Day Type</option>
                </select>
            </div>
            <span class="time">Time Range</span>
            <div class="filter2">
                <div>
                    <p>From</p>
                    <select id="from-select">
                        <option value="">--Select Year--</option>
                        <option value="2022">2022</option>
                        <option value="2023">2023</option>
                        <option value="2024">2024</option>
                    </select>
                </div>
                <div>
                    <p>To</p>
                    <select id="to-select">
                        <option value="">--Select Year--</option>
                        <option value="2022">2022</option>
                        <option value="2023">2023</option>
                        <option value="2024">2024</option>
                    </select>
                </div>
            </div>
        </div>
        <button class="submit" id="submit-btn">
            Submit
        </button>
        <div class="graphDiv">
            <img src="static/loading.gif" alt="Image will be loaded below" class="graph">
        </div>
    `;
    document.getElementById('content').innerHTML = content;

    // Set default years for "Views by Day Type" if selected
    setDefaultYearsForViewsByDay(document.querySelector('#visual-select').value);
    
    document.querySelector('.submit').addEventListener('click', generateChart);
}

function loadPredictiveContent() {
    const content = `
        <div class="filters">
            <div class="filter1">
                <p>Visualization Type</p>
                <select id="predict-visual-select">
                    <option value="">--Choose an option--</option>
                    <option value="views_prediction">Views Prediction</option>
                    <option value="like_count_prediction">Like Count Prediction</option>
                    <option value="comment_count_prediction">Comment Count Prediction</option>
                    <option value="views_per_minute_prediction">Views per Minute Prediction</option>
                </select>
            </div>
        </div>
        <button class="submit" id="submit-btn">
            Submit
        </button>
        <div class="graphDiv">
            <img src="static/loading.gif" alt="Image will be loaded below" class="graph">
        </div>
    `;
    document.getElementById('content').innerHTML = content;
    document.querySelector('.submit').addEventListener('click', predictChart);
}

function generateChart() {
    // Get values from form
    const visualizationType = document.getElementById('visual-select').value;
    const fromYear = document.getElementById('from-select').value;
    const toYear = document.getElementById('to-select') ? document.getElementById('to-select').value : null;

    // Graph type default is line
    let graphType = "line";

    if (document.querySelector('.dashboard-graph .bar').classList.contains('active')) {
        graphType = "bar";
    } else if (document.querySelector('.dashboard-graph .pie').classList.contains('active')) {
        graphType = "pie";
    } else if (document.querySelector('.dashboard-graph .line').classList.contains('active')) {
        graphType = "line";
    }

    // Prepare the data to send
    const data = {
        visualizationType: visualizationType,
        fromYear: fromYear,
        toYear: toYear,
        graphType: graphType
    };

    // Send data to Flask backend using fetch API
    fetch('/generate-chart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.blob()) // Expect image from server
    .then(imageBlob => {
        // Create image URL
        const imageURL = URL.createObjectURL(imageBlob);

        // Update the image on the frontend
        document.querySelector('.graph').src = imageURL;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function predictChart() {
    // Get values from form
    const visualizationType = document.getElementById('predict-visual-select').value;

    // Graph type default is line
    let graphType = "line";

    if (document.querySelector('.predictive-graph .bar').classList.contains('active')) {
        graphType = "bar";
    } else if (document.querySelector('.predictive-graph .pie').classList.contains('active')) {
        graphType = "pie";
    } else if (document.querySelector('.predictive-graph .line').classList.contains('active')) {
        graphType = "line";
    }

    // Prepare the data to send
    const data = {
        visualizationType: visualizationType,
        graphType: graphType
    };

    // Send data to Flask backend using fetch API
    fetch('/predict-chart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.blob()) // Expect image from server
    .then(imageBlob => {
        // Create image URL
        const imageURL = URL.createObjectURL(imageBlob);

        // Update the image on the frontend
        document.querySelector('.graph').src = imageURL;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
