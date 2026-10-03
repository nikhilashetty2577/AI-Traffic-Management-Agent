async function analyzeTraffic() {

    const data = {

        north_vehicles:
            Number(
                document.getElementById(
                    "northVehicles"
                ).value
            ),

        south_vehicles:
            Number(
                document.getElementById(
                    "southVehicles"
                ).value
            ),

        east_vehicles:
            Number(
                document.getElementById(
                    "eastVehicles"
                ).value
            ),

        west_vehicles:
            Number(
                document.getElementById(
                    "westVehicles"
                ).value
            ),

        north_wait:
            Number(
                document.getElementById(
                    "northWait"
                ).value
            ),

        south_wait:
            Number(
                document.getElementById(
                    "southWait"
                ).value
            ),

        east_wait:
            Number(
                document.getElementById(
                    "eastWait"
                ).value
            ),

        west_wait:
            Number(
                document.getElementById(
                    "westWait"
                ).value
            ),

        emergency:
            document.getElementById(
                "emergency"
            ).value
    };


    try {

        // Send traffic data to Flask
        const response = await fetch(
            "/api/analyze",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify(data)
            }
        );


        const result =
            await response.json();


        let html = "";


        // Emergency result

        if (result.emergency_detected) {

            html += `

                <div class="emergency">

                    <h3>
                        🚨 Emergency Priority
                    </h3>

                    <h2>
                        ${result.selected_direction}
                    </h2>

                    <p>
                        ${result.reason}
                    </p>

                    <strong>
                        Green Signal:
                        ${result.green_time}
                        seconds
                    </strong>

                </div>

            `;

        }


        // Normal traffic result

        else {

            html += `

                <div class="priority">

                    <h3>
                        🚦 Recommended Priority
                    </h3>

                    <h2>
                        ${result.selected_direction}
                    </h2>

                    <p>
                        ${result.reason}
                    </p>

                    <strong>
                        Green Signal:
                        ${result.green_time}
                        seconds
                    </strong>

                </div>

            `;
        }


        // Traffic analysis table

        html += `

            <h3>
                📊 Traffic Analysis
            </h3>

            <table>

                <tr>

                    <th>
                        Direction
                    </th>

                    <th>
                        Vehicles
                    </th>

                    <th>
                        Waiting Time
                    </th>

                    <th>
                        Priority Score
                    </th>

                    <th>
                        Emergency
                    </th>

                </tr>

        `;


        for (
            const [direction, traffic]
            of Object.entries(
                result.traffic_analysis
            )
        ) {

            html += `

                <tr>

                    <td>
                        ${direction}
                    </td>

                    <td>
                        ${traffic.vehicles}
                    </td>

                    <td>
                        ${traffic.waiting_time}
                        sec
                    </td>

                    <td>
                        ${traffic.priority_score}
                    </td>

                    <td>

                        ${
                            traffic.emergency
                            ? "🚨 Yes"
                            : "No"
                        }

                    </td>

                </tr>

            `;
        }


        html += "</table>";


        // Send the AI agent result to Gemini

        try {

            const explanationResponse =
                await fetch(
                    "/api/explain",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            selected_direction:
                                result.selected_direction,

                            green_time:
                                result.green_time,

                            traffic_analysis:
                                result.traffic_analysis,

                            emergency_detected:
                                result.emergency_detected

                        })
                    }
                );


            const explanationResult =
                await explanationResponse.json();


            if (
                explanationResult.success
            ) {

                html += `

                    <div class="priority">

                        <h3>
                            🧠 AI Traffic Intelligence
                        </h3>

                        <p>
                            ${explanationResult.explanation}
                        </p>

                    </div>

                `;

            }

            else {

                html += `

                    <div class="emergency">

                        <h3>
                            ⚠️ AI Explanation
                        </h3>

                        <p>
                            Gemini explanation
                            could not be generated.
                        </p>

                    </div>

                `;

            }

        }

        catch (error) {

            console.error(
                "LLM explanation error:",
                error
            );

            html += `

                <div class="emergency">

                    <h3>
                        ⚠️ AI Explanation
                    </h3>

                    <p>
                        Traffic analysis worked,
                        but the Gemini explanation
                        could not be generated.
                    </p>

                </div>

            `;

        }


        // Display everything

        document.getElementById(
            "resultContent"
        ).innerHTML = html;


    }

    catch (error) {

        console.error(error);

        document.getElementById(
            "resultContent"
        ).innerHTML = `

            <div class="emergency">

                <h3>
                    ❌ Connection Error
                </h3>

                <p>
                    Make sure the Flask server
                    is running.
                </p>

            </div>

        `;
    }
}



// ========================================
// A* ROUTE PLANNING
// ========================================

async function findRoute() {

    const start =
        document.getElementById(
            "start"
        ).value;


    const destination =
        document.getElementById(
            "destination"
        ).value;


    try {

        const response =
            await fetch(
                "/api/route",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({
                            start,
                            destination
                        })
                }
            );


        const result =
            await response.json();


        const output =
            document.getElementById(
                "routeResult"
            );


        if (!result.success) {

            output.innerHTML = `

                <p>
                    ❌ No route found.
                </p>

            `;

            return;
        }


        output.innerHTML = `

            <h3>
                🚗 Best Route
            </h3>

            <p>
                ${result.route.join(
                    " → "
                )}
            </p>

            <p>

                <strong>
                    Route Cost:
                </strong>

                ${result.cost}

            </p>

        `;

    }

    catch (error) {

        console.error(error);

        document.getElementById(
            "routeResult"
        ).innerHTML = `

            <p>
                ❌ Error connecting
                to the Flask server.
            </p>

        `;
    }
}