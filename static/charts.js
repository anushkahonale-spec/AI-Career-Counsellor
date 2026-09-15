// =========================================
// AI Career Counsellor v5.0
// Dashboard Charts
// =========================================

// Career Distribution Pie Chart

const careerCtx = document.getElementById("careerChart");

if (careerCtx) {

    new Chart(careerCtx, {

        type: "pie",

        data: {

            labels: [
                "AI Engineer",
                "Web Developer",
                "Data Scientist",
                "Backend Developer"
            ],

            datasets: [{

                data: [35, 25, 20, 20],

                backgroundColor: [

                    "#3B82F6",
                    "#10B981",
                    "#F59E0B",
                    "#EF4444"

                ]

            }]

        },

        options: {

            responsive: true,

            plugins: {

                legend: {

                    position: "bottom"

                }

            }

        }

    });

}



// Match Score Bar Chart

const matchCtx = document.getElementById("matchChart");

if (matchCtx) {

    new Chart(matchCtx, {

        type: "bar",

        data: {

            labels: [

                "AI",

                "Web",

                "Data",

                "Backend"

            ],

            datasets: [{

                label: "Average Match %",

                data: [

                    92,

                    85,

                    88,

                    80

                ],

                backgroundColor: "#2563EB",

                borderRadius: 8

            }]

        },

        options: {

            responsive: true,

            scales: {

                y: {

                    beginAtZero: true,

                    max: 100

                }

            }

        }

    });

}