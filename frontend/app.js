/* =========================================================
   AGRIBRIDGE AI
   Main JavaScript
   Step 7B - Improved AI Response Formatting
   ========================================================= */


/* =========================================================
   ASK AGRIBRIDGE AI
   ========================================================= */

async function askAI() {

    const button = document.getElementById("askButton");
    const buttonText = document.getElementById("buttonText");
    const loadingText = document.getElementById("loadingText");

    const responseBox = document.getElementById("aiResponse");
    const errorBox = document.getElementById("errorMessage");


    /* -----------------------------------------------------
       Get farmer information
       ----------------------------------------------------- */

    const farmerName =
        document.getElementById("farmerName").value.trim();

    const location =
        document.getElementById("location").value.trim();

    const state =
        document.getElementById("state").value.trim();

    const lga =
        document.getElementById("lga").value.trim();

    const cropType =
        document.getElementById("cropType").value.trim();

    const farmSize =
        Number(document.getElementById("farmSize").value);

    const cropAge =
        Number(document.getElementById("cropAge").value);

    const question =
        document.getElementById("question").value.trim();


    /* -----------------------------------------------------
       Clear previous error
       ----------------------------------------------------- */

    errorBox.classList.add("hidden");
    errorBox.textContent = "";


    /* -----------------------------------------------------
       Basic validation
       ----------------------------------------------------- */

    if (!question) {

        errorBox.textContent =
            "Please enter a question about your farm.";

        errorBox.classList.remove("hidden");

        return;
    }


    /* -----------------------------------------------------
       Show loading state
       ----------------------------------------------------- */

    button.disabled = true;

    buttonText.classList.add("hidden");
    loadingText.classList.remove("hidden");


    responseBox.innerHTML = `
        <div class="loading-response">
            <div class="loading-icon">🤖</div>

            <strong>
                AgriBridge AI is analyzing your farm...
            </strong>

            <p>
                Considering your crop, location, farm size and crop age.
            </p>
        </div>
    `;


    /* -----------------------------------------------------
       Create request
       ----------------------------------------------------- */

    const requestData = {

        question: question,

        farm: {

            farmer_name: farmerName,

            location: location,

            state: state,

            lga: lga,

            crop_type: cropType,

            farm_size: farmSize,

            crop_age_weeks: cropAge
        },

        conversation_history: []
    };


    /* -----------------------------------------------------
       Send request to FastAPI
       ----------------------------------------------------- */

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/ai/ask",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(requestData)
            }
        );


        /* -------------------------------------------------
           Check server response
           ------------------------------------------------- */

        if (!response.ok) {

            let errorMessage =
                `Server returned ${response.status}`;

            try {

                const errorData =
                    await response.json();

                if (errorData.detail) {
                    errorMessage =
                        errorData.detail;
                }

            } catch (e) {
                // Ignore JSON parsing error
            }

            throw new Error(errorMessage);
        }


        /* -------------------------------------------------
           Read AI response
           ------------------------------------------------- */

        const data =
            await response.json();


        /* -------------------------------------------------
           Display formatted AI response
           ------------------------------------------------- */

        responseBox.innerHTML =
            formatAIResponse(data.answer);


        /* -------------------------------------------------
           Scroll response into view
           ------------------------------------------------- */

        responseBox.scrollIntoView({
            behavior: "smooth",
            block: "nearest"
        });


    } catch (error) {

        console.error(
            "AgriBridge AI Error:",
            error
        );


        /* -------------------------------------------------
           Display friendly error
           ------------------------------------------------- */

        responseBox.innerHTML = `
            <div class="ai-error">

                <div class="ai-error-icon">
                    ⚠️
                </div>

                <strong>
                    AgriBridge AI could not complete the request.
                </strong>

                <p>
                    Please check that the FastAPI server is running
                    and try again.
                </p>

            </div>
        `;


        errorBox.textContent =
            "Could not connect to the AgriBridge AI server. Make sure FastAPI is running.";

        errorBox.classList.remove("hidden");

    } finally {

        /* -------------------------------------------------
           Restore button
           ------------------------------------------------- */

        button.disabled = false;

        buttonText.classList.remove("hidden");

        loadingText.classList.add("hidden");
    }
}


/* =========================================================
   FORMAT GEMINI RESPONSE
   =========================================================

   Gemini normally returns Markdown.

   This function converts common Markdown formatting
   into attractive HTML for the AgriBridge interface.
   ========================================================= */

function formatAIResponse(text) {

    /* -----------------------------------------------------
       Empty response
       ----------------------------------------------------- */

    if (!text) {

        return `
            <div class="empty-response">
                No response was received from AgriBridge AI.
            </div>
        `;
    }


    /* -----------------------------------------------------
       Escape HTML first for safety
       ----------------------------------------------------- */

    let formatted = text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");


    /* -----------------------------------------------------
       Convert bold text
       Example:
       **Most Likely Cause**
       ----------------------------------------------------- */

    formatted = formatted.replace(
        /\*\*(.*?)\*\*/g,
        "<strong>$1</strong>"
    );


    /* -----------------------------------------------------
       Convert H4 headings FIRST
       Example:
       #### Nitrogen Loss
       ----------------------------------------------------- */

    formatted = formatted.replace(
        /^####\s+(.*)$/gm,
        '<h5 class="ai-heading">$1</h5>'
    );


    /* -----------------------------------------------------
       Convert H3 headings
       ----------------------------------------------------- */

    formatted = formatted.replace(
        /^###\s+(.*)$/gm,
        '<h4 class="ai-heading">$1</h4>'
    );


    /* -----------------------------------------------------
       Convert H2 headings
       ----------------------------------------------------- */

    formatted = formatted.replace(
        /^##\s+(.*)$/gm,
        '<h3 class="ai-heading">$1</h3>'
    );


    /* -----------------------------------------------------
       Convert H1 headings
       ----------------------------------------------------- */

    formatted = formatted.replace(
        /^#\s+(.*)$/gm,
        '<h2 class="ai-heading">$1</h2>'
    );


    /* -----------------------------------------------------
       Convert horizontal lines
       ----------------------------------------------------- */

    formatted = formatted.replace(
        /^---$/gm,
        '<hr class="ai-divider">'
    );


    /* -----------------------------------------------------
       Convert numbered lists
       Example:
       1. Check the soil
       ----------------------------------------------------- */

    formatted = formatted.replace(
        /^\s*(\d+)\.\s+(.*)$/gm,
        '<div class="ai-list-item">' +
            '<span class="ai-number">$1</span>' +
            '<span>$2</span>' +
        '</div>'
    );


    /* -----------------------------------------------------
       Convert bullet lists
       ----------------------------------------------------- */

    formatted = formatted.replace(
        /^\s*[-*]\s+(.*)$/gm,
        '<div class="ai-bullet">' +
            '<span>•</span>' +
            '<span>$1</span>' +
        '</div>'
    );


    /* -----------------------------------------------------
       Convert line breaks
       ----------------------------------------------------- */

    formatted = formatted.replace(
        /\n\n/g,
        '<div class="ai-space"></div>'
    );


    formatted = formatted.replace(
        /\n/g,
        '<br>'
    );


    /* -----------------------------------------------------
       Return finished HTML
       ----------------------------------------------------- */

    return formatted;
}


/* =========================================================
   FARM SNAPSHOT
   =========================================================

   Updates the farm summary while the farmer enters
   information into the form.
   ========================================================= */

function updateFarmSnapshot() {

    const farmerName =
        document.getElementById("farmerName")?.value.trim() || "—";

    const cropType =
        document.getElementById("cropType")?.value.trim() || "—";

    const farmSize =
        document.getElementById("farmSize")?.value || "—";

    const cropAge =
        document.getElementById("cropAge")?.value || "—";

    const location =
        document.getElementById("location")?.value.trim() || "—";

    const state =
        document.getElementById("state")?.value.trim() || "—";


    const snapshotFarmer =
        document.getElementById("snapshotFarmer");

    const snapshotCrop =
        document.getElementById("snapshotCrop");

    const snapshotSize =
        document.getElementById("snapshotSize");

    const snapshotAge =
        document.getElementById("snapshotAge");

    const snapshotLocation =
        document.getElementById("snapshotLocation");


    if (snapshotFarmer) {
        snapshotFarmer.textContent = farmerName;
    }

    if (snapshotCrop) {
        snapshotCrop.textContent = cropType;
    }

    if (snapshotSize) {
        snapshotSize.textContent =
            `${farmSize} hectares`;
    }

    if (snapshotAge) {
        snapshotAge.textContent =
            `${cropAge} weeks`;
    }

    if (snapshotLocation) {
        snapshotLocation.textContent =
            `${location}, ${state}`;
    }
}


/* =========================================================
   CONNECT FORM FIELDS TO FARM SNAPSHOT
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const fields = [

            "farmerName",
            "location",
            "state",
            "lga",
            "cropType",
            "farmSize",
            "cropAge"
        ];


        fields.forEach(
            function (fieldId) {

                const field =
                    document.getElementById(fieldId);


                if (field) {

                    field.addEventListener(
                        "input",
                        updateFarmSnapshot
                    );

                    field.addEventListener(
                        "change",
                        updateFarmSnapshot
                    );
                }
            }
        );


        /* ---------------------------------------------
           Initial snapshot
           --------------------------------------------- */

        updateFarmSnapshot();
    }
);