/* =========================================================
   AGRIBRIDGE AI
   Frontend Application
   Step 10D - Final AI Response Formatting
========================================================= */


/* =========================================================
   CONVERSATION MEMORY
========================================================= */

let conversationHistory = [];


/* =========================================================
   ASK AGRIBRIDGE AI
========================================================= */

async function askAI() {

    const button =
        document.getElementById("askButton");

    const buttonText =
        document.getElementById("buttonText");

    const loadingText =
        document.getElementById("loadingText");

    const responseBox =
        document.getElementById("aiResponse");

    const errorBox =
        document.getElementById("errorMessage");


    /* -----------------------------------------------------
       GET FARM INFORMATION
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
        Number(
            document.getElementById("farmSize").value
        );

    const cropAge =
        Number(
            document.getElementById("cropAge").value
        );

    const question =
        document.getElementById("question").value.trim();


    /* -----------------------------------------------------
       CLEAR ERROR
    ----------------------------------------------------- */

    errorBox.classList.add("hidden");
    errorBox.textContent = "";


    /* -----------------------------------------------------
       VALIDATION
    ----------------------------------------------------- */

    if (!question) {

        errorBox.textContent =
            "Please enter a question about your farm.";

        errorBox.classList.remove("hidden");

        return;
    }


    if (
        !farmerName ||
        !location ||
        !state ||
        !lga ||
        !cropType
    ) {

        errorBox.textContent =
            "Please complete your farm information before asking AgriBridge AI.";

        errorBox.classList.remove("hidden");

        return;
    }


    if (
        !Number.isFinite(farmSize) ||
        farmSize <= 0
    ) {

        errorBox.textContent =
            "Please enter a valid farm size.";

        errorBox.classList.remove("hidden");

        return;
    }


    /* -----------------------------------------------------
       SHOW THINKING
    ----------------------------------------------------- */

    button.disabled = true;

    buttonText.classList.add("hidden");

    loadingText.classList.remove("hidden");


    responseBox.innerHTML = `
        <div class="loading-response">

            <div class="loading-icon">
                🤖
            </div>

            <strong>
                AgriBridge AI is analyzing your farm...
            </strong>

            <p>
                Considering your crop, location,
                farm size and crop age.
            </p>

        </div>
    `;


    /* -----------------------------------------------------
       REQUEST DATA
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

            crop_age_weeks:
                Number.isFinite(cropAge) &&
                cropAge > 0
                    ? cropAge
                    : null
        },

        conversation_history:
            conversationHistory.slice(-10)
    };


    console.log(
        "Sending request to AgriBridge AI:",
        requestData
    );


    /* =====================================================
       SEND REQUEST TO FASTAPI
    ===================================================== */

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/ai/ask",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body:
                    JSON.stringify(requestData)
            }
        );


        /* -------------------------------------------------
           READ SERVER RESPONSE
        ------------------------------------------------- */

        let data = {};

        try {

            data = await response.json();

        } catch (jsonError) {

            console.warn(
                "Could not read server response:",
                jsonError
            );

            data = {};
        }


        /* =================================================
           SUCCESS
        ================================================= */

        if (response.ok) {

            const answer =
                data.answer ||
                "AgriBridge AI did not return an answer.";


            /* -------------------------------------------------
               SAVE CONVERSATION
            ------------------------------------------------- */

            conversationHistory.push({
                role: "farmer",
                content: question
            });


            conversationHistory.push({
                role: "ai",
                content: answer
            });


            /* Keep latest 10 messages */

            conversationHistory =
                conversationHistory.slice(-10);


            /* -------------------------------------------------
               DISPLAY
            ------------------------------------------------- */

            displayConversation();


            /* -------------------------------------------------
               CLEAR QUESTION
            ------------------------------------------------- */

            document.getElementById(
                "question"
            ).value = "";


            /* -------------------------------------------------
               SCROLL TO RESPONSE
            ------------------------------------------------- */

            responseBox.scrollIntoView({
                behavior: "smooth",
                block: "nearest"
            });


            return;
        }


        /* =================================================
           422 VALIDATION ERROR
        ================================================= */

        if (response.status === 422) {

            console.error(
                "422 Validation Error:",
                data
            );

            showError(
                getServerMessage(
                    data,
                    "Some farm information is not in the expected format."
                ),
                "⚠️",
                "AgriBridge AI could not process the farm information.",
                "Please check the information entered and try again."
            );

            return;
        }


        /* =================================================
           429 GEMINI LIMIT
        ================================================= */

        if (response.status === 429) {

            console.warn(
                "Gemini quota exceeded:",
                data
            );

            showError(
                getServerMessage(
                    data,
                    "AgriBridge AI has temporarily reached the available AI request limit. Please wait a little while and try again."
                ),
                "🕐",
                "AgriBridge AI is temporarily busy",
                "The current AI request limit has been reached. Please wait a little while and try again."
            );

            return;
        }


        /* =================================================
           503 AI UNAVAILABLE
        ================================================= */

        if (response.status === 503) {

            console.warn(
                "AI temporarily unavailable:",
                data
            );

            showError(
                getServerMessage(
                    data,
                    "AgriBridge AI is temporarily unavailable. Please try again shortly."
                ),
                "🔄",
                "AgriBridge AI is temporarily unavailable",
                "The AI service is experiencing high demand. Please try again shortly."
            );

            return;
        }


        /* =================================================
           400 BAD REQUEST
        ================================================= */

        if (response.status === 400) {

            console.warn(
                "Bad request:",
                data
            );

            showError(
                getServerMessage(
                    data,
                    "AgriBridge AI could not process this request."
                ),
                "⚠️",
                "Invalid farm information",
                "Please check the information entered and try again."
            );

            return;
        }


        /* =================================================
           500 SERVER ERROR
        ================================================= */

        if (response.status === 500) {

            console.error(
                "Server error:",
                data
            );

            showError(
                getServerMessage(
                    data,
                    "AgriBridge AI encountered an unexpected problem."
                ),
                "⚠️",
                "AgriBridge AI encountered a problem",
                "Please try again in a moment."
            );

            return;
        }


        /* =================================================
           OTHER ERRORS
        ================================================= */

        console.error(
            "Unexpected server response:",
            response.status,
            data
        );

        showError(
            `AgriBridge AI returned an unexpected error (${response.status}).`,
            "⚠️",
            "AgriBridge AI could not complete the request.",
            "Please try again shortly."
        );


    } catch (error) {

        /* =================================================
           CONNECTION ERROR
        ================================================= */

        console.error(
            "Connection error:",
            error
        );

        showError(
            "Could not connect to the AgriBridge AI server.",
            "🔌",
            "AgriBridge AI server connection problem",
            "Please make sure FastAPI is running and try again."
        );


    } finally {

        /* -------------------------------------------------
           RESTORE BUTTON
        ------------------------------------------------- */

        button.disabled = false;

        buttonText.classList.remove("hidden");

        loadingText.classList.add("hidden");
    }
}


/* =========================================================
   DISPLAY CONVERSATION
========================================================= */

function displayConversation() {

    const responseBox =
        document.getElementById("aiResponse");


    if (!conversationHistory.length) {

        responseBox.innerHTML = `
            <div class="empty-response">

                Your AI-generated agricultural
                advice will appear here.

            </div>
        `;

        return;
    }


    let html = `

        <div class="conversation-container">

            <div class="conversation-header">

                🤖 AgriBridge AI Conversation

            </div>
    `;


    /* -----------------------------------------------------
       DISPLAY EACH MESSAGE
    ----------------------------------------------------- */

    conversationHistory.forEach(
        function(message) {

            /* =============================================
               FARMER MESSAGE
            ============================================= */

            if (message.role === "farmer") {

                html += `

                    <div class="conversation-message farmer-message">

                        <div class="message-role">

                            👨‍🌾 You

                        </div>

                        <div class="message-content">

                            ${escapeHTML(message.content)}

                        </div>

                    </div>
                `;
            }


            /* =============================================
               AI MESSAGE
            ============================================= */

            if (message.role === "ai") {

                html += `

                    <div class="conversation-message ai-message">

                        <div class="message-role">

                            🤖 AgriBridge AI

                        </div>

                        <div class="message-content">

                            ${formatAIResponse(
                                message.content
                            )}

                        </div>

                    </div>
                `;
            }

        }
    );


    html += `

        </div>
    `;


    /* -----------------------------------------------------
       DISPLAY
    ----------------------------------------------------- */

    responseBox.innerHTML =
        html;


    /* -----------------------------------------------------
       SCROLL TO BOTTOM
    ----------------------------------------------------- */

    responseBox.scrollTop =
        responseBox.scrollHeight;
}


/* =========================================================
   GET SERVER MESSAGE
========================================================= */

function getServerMessage(
    data,
    fallback
) {

    if (
        data &&
        data.detail &&
        typeof data.detail === "object" &&
        data.detail.message
    ) {

        return data.detail.message;
    }


    if (
        data &&
        typeof data.detail === "string"
    ) {

        return data.detail;
    }


    if (
        data &&
        data.message
    ) {

        return data.message;
    }


    return fallback;
}


/* =========================================================
   SHOW ERROR
========================================================= */

function showError(
    message,
    icon,
    title,
    description
) {

    const errorBox =
        document.getElementById("errorMessage");

    const responseBox =
        document.getElementById("aiResponse");


    errorBox.textContent =
        message;

    errorBox.classList.remove("hidden");


    responseBox.innerHTML = `

        <div class="ai-error">

            <div class="ai-error-icon">

                ${icon}

            </div>

            <strong>

                ${escapeHTML(title)}

            </strong>

            <p>

                ${escapeHTML(description)}

            </p>

        </div>
    `;
}


/* =========================================================
   FINAL AI RESPONSE FORMATTER
========================================================= */

function formatAIResponse(text) {

    if (!text) {

        return `
            <div class="empty-response">

                No response was received from
                AgriBridge AI.

            </div>
        `;
    }


    /* -----------------------------------------------------
       CLEAN AI RESPONSE
    ----------------------------------------------------- */

    let cleanText =
        String(text);


    /*
       Remove accidental backslashes before markdown
       headings.
    */

    cleanText =
        cleanText.replace(
            /^\\+(#{1,6})/gm,
            "$1"
        );


    /*
       Remove known bad placeholder characters
       from previous Gemini responses.
    */

    cleanText =
        cleanText
            .replace(/\*\*•\*\*\$2/g, "•")
            .replace(/\*\*(\d+)\*\*\1/g, "$1")
            .replace(/\$2/g, "");


    /*
       Convert Windows line endings.
    */

    cleanText =
        cleanText.replace(
            /\r\n/g,
            "\n"
        );


    /* -----------------------------------------------------
       ESCAPE HTML
    ----------------------------------------------------- */

    let formatted =
        escapeHTML(cleanText);


    /* -----------------------------------------------------
       HEADINGS
    ----------------------------------------------------- */

    formatted =
        formatted.replace(
            /^######\s+(.*?)$/gm,
            '<h6 class="ai-heading">$1</h6>'
        );


    formatted =
        formatted.replace(
            /^#####\s+(.*?)$/gm,
            '<h5 class="ai-heading">$1</h5>'
        );


    formatted =
        formatted.replace(
            /^####\s+(.*?)$/gm,
            '<h4 class="ai-heading">$1</h4>'
        );


    formatted =
        formatted.replace(
            /^###\s+(.*?)$/gm,
            '<h4 class="ai-heading">$1</h4>'
        );


    formatted =
        formatted.replace(
            /^##\s+(.*?)$/gm,
            '<h3 class="ai-heading">$1</h3>'
        );


    formatted =
        formatted.replace(
            /^#\s+(.*?)$/gm,
            '<h2 class="ai-heading">$1</h2>'
        );


    /* -----------------------------------------------------
       HORIZONTAL RULE
    ----------------------------------------------------- */

    formatted =
        formatted.replace(
            /^\s*---+\s*$/gm,
            '<hr class="ai-divider">'
        );


    /* -----------------------------------------------------
       BOLD
    ----------------------------------------------------- */

    formatted =
        formatted.replace(
            /\*\*(.*?)\*\*/g,
            "<strong>$1</strong>"
        );


    /* -----------------------------------------------------
       ITALIC
    ----------------------------------------------------- */

    formatted =
        formatted.replace(
            /(?<!\*)\*([^*\n]+)\*(?!\*)/g,
            "<em>$1</em>"
        );


    /* -----------------------------------------------------
       PROCESS LINES
    ----------------------------------------------------- */

    const lines =
        formatted.split("\n");


    let output = "";

    let inBulletList = false;

    let inNumberList = false;


    function closeLists() {

        if (inBulletList) {

            output += "</ul>";

            inBulletList = false;
        }


        if (inNumberList) {

            output += "</ol>";

            inNumberList = false;
        }
    }


    lines.forEach(
        function(line) {

            const trimmed =
                line.trim();


            /* =============================================
               EMPTY LINE
            ============================================= */

            if (!trimmed) {

                closeLists();

                output +=
                    '<div class="ai-space"></div>';

                return;
            }


            /* =============================================
               HEADING
            ============================================= */

            if (
                trimmed.startsWith("<h2") ||
                trimmed.startsWith("<h3") ||
                trimmed.startsWith("<h4") ||
                trimmed.startsWith("<h5") ||
                trimmed.startsWith("<h6")
            ) {

                closeLists();

                output +=
                    trimmed;

                return;
            }


            /* =============================================
               HORIZONTAL RULE
            ============================================= */

            if (
                trimmed.startsWith("<hr")
            ) {

                closeLists();

                output +=
                    trimmed;

                return;
            }


            /* =============================================
               NUMBERED LIST
            ============================================= */

            const numberedMatch =
                trimmed.match(
                    /^(\d+)\.\s+(.*)$/
                );


            if (numberedMatch) {

                if (!inNumberList) {

                    if (inBulletList) {

                        output += "</ul>";

                        inBulletList = false;
                    }


                    output +=
                        '<ol class="ai-number-list">';

                    inNumberList = true;
                }


                output += `

                    <li>

                        ${numberedMatch[2]}

                    </li>
                `;

                return;
            }


            /* =============================================
               BULLET LIST
            ============================================= */

            const bulletMatch =
                trimmed.match(
                    /^[-*•]\s+(.*)$/
                );


            if (bulletMatch) {

                if (!inBulletList) {

                    if (inNumberList) {

                        output += "</ol>";

                        inNumberList = false;
                    }


                    output +=
                        '<ul class="ai-bullet-list">';

                    inBulletList = true;
                }


                output += `

                    <li>

                        ${bulletMatch[1]}

                    </li>
                `;

                return;
            }


            /* =============================================
               NORMAL PARAGRAPH
            ============================================= */

            closeLists();


            output += `

                <p class="ai-paragraph">

                    ${trimmed}

                </p>
            `;
        }
    );


    closeLists();


    return output;
}


/* =========================================================
   ESCAPE HTML
========================================================= */

function escapeHTML(value) {

    return String(value)

        .replace(
            /&/g,
            "&amp;"
        )

        .replace(
            /</g,
            "&lt;"
        )

        .replace(
            />/g,
            "&gt;"
        )

        .replace(
            /"/g,
            "&quot;"
        )

        .replace(
            /'/g,
            "&#039;"
        );
}


/* =========================================================
   CLEAR CONVERSATION
========================================================= */

function clearConversation() {

    conversationHistory = [];


    const responseBox =
        document.getElementById("aiResponse");


    const errorBox =
        document.getElementById("errorMessage");


    if (errorBox) {

        errorBox.classList.add("hidden");

        errorBox.textContent = "";
    }


    if (responseBox) {

        responseBox.innerHTML = `

            <div class="empty-response">

                Your AI-generated agricultural
                advice will appear here.

            </div>
        `;
    }


    console.log(
        "AgriBridge AI conversation cleared."
    );
}


/* =========================================================
   UPDATE FARM SNAPSHOT
========================================================= */

function updateFarmSnapshot() {

    const farmerName =
        document
            .getElementById("farmerName")
            ?.value
            .trim() ||
        "Not provided";


    const location =
        document
            .getElementById("location")
            ?.value
            .trim() ||
        "Not provided";


    const state =
        document
            .getElementById("state")
            ?.value
            .trim() ||
        "";


    const cropType =
        document
            .getElementById("cropType")
            ?.value
            .trim() ||
        "Not provided";


    const farmSize =
        document
            .getElementById("farmSize")
            ?.value ||
        "0";


    const cropAge =
        document
            .getElementById("cropAge")
            ?.value ||
        "0";


    const snapshotFarmer =
        document.getElementById(
            "snapshotFarmer"
        );


    const snapshotCrop =
        document.getElementById(
            "snapshotCrop"
        );


    const snapshotSize =
        document.getElementById(
            "snapshotSize"
        );


    const snapshotAge =
        document.getElementById(
            "snapshotAge"
        );


    const snapshotLocation =
        document.getElementById(
            "snapshotLocation"
        );


    if (snapshotFarmer) {

        snapshotFarmer.textContent =
            farmerName;
    }


    if (snapshotCrop) {

        snapshotCrop.textContent =
            cropType;
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
            state
                ? `${location}, ${state}`
                : location;
    }
}


/* =========================================================
   INITIALIZE APPLICATION
========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    function() {

        /* -----------------------------------------------
           FARM SNAPSHOT
        ----------------------------------------------- */

        updateFarmSnapshot();


        /* -----------------------------------------------
           FARM FIELDS
        ----------------------------------------------- */

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
            function(id) {

                const field =
                    document.getElementById(id);


                if (field) {

                    field.addEventListener(
                        "input",
                        updateFarmSnapshot
                    );
                }
            }
        );


        /* -----------------------------------------------
           CLEAR CONVERSATION BUTTON
        ----------------------------------------------- */

        const clearButton =
            document.getElementById(
                "clearConversation"
            );


        if (clearButton) {

            clearButton.addEventListener(
                "click",
                clearConversation
            );
        }


        /* -----------------------------------------------
           INITIAL MESSAGE
        ----------------------------------------------- */

        displayConversation();


        console.log(
            "AgriBridge AI frontend initialized successfully."
        );
    }
);