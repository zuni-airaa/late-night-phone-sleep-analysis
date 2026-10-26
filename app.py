import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, ttest_ind
from pathlib import Path
import base64


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Does Late-Night Phone Use Affect Sleep?",
    page_icon="🌙",
    layout="wide"
)


# =========================================================
# FIND IMAGES
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"

# Full-screen wallpaper
background_image = ASSETS_DIR / "moon-background.jpg"

# Cute animated foreground GIF
gif_image = ASSETS_DIR / "background.gif"

# Analysis transition image
transition_image = ASSETS_DIR / "transition.jpg"

# Result image
result_image = ASSETS_DIR / "result.jpg"


# =========================================================
# FULL-PAGE MOON BACKGROUND
# =========================================================

if background_image.exists():

    with open(background_image, "rb") as f:
        bg_data = base64.b64encode(f.read()).decode("utf-8")

    st.markdown(
        f"""
        <style>

        /* =========================================
           MOON IMAGE = ENTIRE PAGE BACKGROUND
           ========================================= */

        html,
        body,
        [data-testid="stAppViewContainer"],
        [data-testid="stApp"] {{
            background: transparent !important;
        }}


        .stApp {{
            background-image:
                url("data:image/jpeg;base64,{bg_data}") !important;

            background-size: cover !important;
            background-position: center center !important;
            background-repeat: no-repeat !important;
            background-attachment: fixed !important;
        }}


        [data-testid="stHeader"] {{
            background: transparent !important;
        }}


        [data-testid="stToolbar"] {{
            background: transparent !important;
        }}


        footer {{
            visibility: hidden;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

else:

    st.error(
        "moon-background.jpg not found. Put it inside the assets folder."
    )


# =========================================================
# AESTHETIC CSS
# =========================================================

st.markdown(
    """
    <style>

    /* MAIN PAGE WIDTH */

    .block-container {
        max-width: 1100px !important;
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
    }


    /* =====================================================
       TITLE BOXES
       ===================================================== */

    .main-title-box {
        background: rgba(255, 255, 255, 0.62);
        border-radius: 18px;
        padding: 18px 28px;
        margin: 5px auto 14px auto;
        max-width: 850px;

        box-shadow:
            0 8px 25px rgba(50, 20, 50, 0.12);

        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);

        text-align: center;
    }


    .subtitle-box {
        background: rgba(255, 255, 255, 0.55);
        border-radius: 18px;
        padding: 15px 28px;
        margin: 0 auto 30px auto;
        max-width: 850px;

        box-shadow:
            0 8px 25px rgba(50, 20, 50, 0.10);

        backdrop-filter: blur(5px);
        -webkit-backdrop-filter: blur(5px);

        text-align: center;
    }


    .main-title {
        color: #000000 !important;
        font-size: 30px;
        font-weight: 900;
        margin: 0;
        padding: 0;
    }


    .subtitle {
        color: #000000 !important;
        font-size: 17px;
        font-weight: 700;
        margin: 0;
        padding: 0;
    }


    /* =====================================================
       SECTION TITLES
       ===================================================== */

    .section-title {
        color: #000000 !important;
        font-size: 25px;
        font-weight: 900;

        margin-top: 25px;
        margin-bottom: 10px;

        text-shadow:
            0px 2px 6px rgba(255,255,255,0.95);
    }


    .helper-text {
        color: #000000 !important;
        font-size: 16px;
        font-weight: 800;

        margin-bottom: 12px;

        text-shadow:
            0px 2px 5px rgba(255,255,255,0.95);
    }


    /* =====================================================
       DATA EDITOR
       ===================================================== */

    [data-testid="stDataEditor"] {
        background: rgba(255,255,255,0.94) !important;

        border-radius: 16px !important;

        box-shadow:
            0px 7px 22px rgba(40,20,40,0.16) !important;
    }


    /* =====================================================
       FILE UPLOADER
       ===================================================== */

    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.88) !important;

        border-radius: 15px !important;

        padding: 8px !important;

        box-shadow:
            0px 6px 18px rgba(40,20,40,0.12) !important;
    }


    [data-testid="stFileUploader"] label,
    [data-testid="stFileUploader"] p {
        color: #000000 !important;
        font-weight: 700 !important;
    }


    /* =====================================================
       BUTTON
       ===================================================== */

    div.stButton > button,
    div[data-testid="stFormSubmitButton"] > button {

        background: #955a91 !important;

        color: white !important;

        border: none !important;

        border-radius: 14px !important;

        min-height: 50px !important;

        padding-left: 24px !important;
        padding-right: 24px !important;

        font-size: 16px !important;

        font-weight: 900 !important;

        box-shadow:
            0px 6px 18px rgba(70,30,70,0.25) !important;
    }


    div.stButton > button:hover,
    div[data-testid="stFormSubmitButton"] > button:hover {

        background: #774675 !important;
        color: white !important;
    }


    /* =====================================================
       METRICS
       ===================================================== */

    [data-testid="stMetric"] {

        background: rgba(255,255,255,0.88) !important;

        border-radius: 16px !important;

        padding: 15px !important;

        box-shadow:
            0px 6px 18px rgba(40,20,40,0.12) !important;
    }


    [data-testid="stMetricLabel"] {
        color: #222222 !important;
        font-weight: 800 !important;
    }


    [data-testid="stMetricValue"] {
        color: #000000 !important;
        font-weight: 900 !important;
    }


    /* =====================================================
       ALERTS
       ===================================================== */

    [data-testid="stAlert"] {
        border-radius: 14px !important;
        font-weight: 700 !important;
    }


    .stMarkdown p,
    .stCaption {
        color: #000000 !important;
        font-weight: 650;
    }


    /* Remove unwanted Streamlit container boxes */

    [data-testid="stVerticalBlockBorderWrapper"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }


    /* =====================================================
       RESULT CARD
       ===================================================== */

    .result-card {
        background: rgba(255,255,255,0.93);

        border-radius: 22px;

        padding: 18px;

        max-width: 430px;

        margin: 25px auto 20px auto;

        box-shadow:
            0px 10px 30px rgba(40,20,40,0.20);

        text-align: center;
    }


    .result-card-title {
        color: #000000;

        font-size: 20px;

        font-weight: 900;

        margin-bottom: 12px;
    }


    /* =====================================================
       FULL SCREEN ANALYSIS ANIMATION
       ===================================================== */

    .analysis-overlay {
        position: fixed;
        inset: 0;
        width: 100vw;
        height: 100vh;

        background: rgba(245, 225, 239, 0.97);

        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;

        z-index: 999999;

        animation: overlayFadeIn 0.7s ease forwards;
    }


    .analysis-image {
        width: min(75vw, 650px);
        max-height: 65vh;

        object-fit: contain;

        border-radius: 30px;

        box-shadow:
            0 20px 60px rgba(70, 30, 70, 0.25);

        animation:
            cuteZoom 2.8s ease-in-out forwards;
    }


    .analysis-text {
        margin-top: 25px;

        color: #5c3859;

        font-size: 25px;
        font-weight: 800;

        text-align: center;

        animation:
            textFloat 1.2s ease-in-out infinite alternate;
    }


    .analysis-subtext {
        margin-top: 8px;

        color: #76566f;

        font-size: 15px;
        font-weight: 600;
    }


    @keyframes overlayFadeIn {

        from {
            opacity: 0;
        }

        to {
            opacity: 1;
        }
    }


    @keyframes cuteZoom {

        0% {
            opacity: 0;
            transform: scale(0.82);
        }

        25% {
            opacity: 1;
            transform: scale(1);
        }

        75% {
            opacity: 1;
            transform: scale(1.04);
        }

        100% {
            opacity: 1;
            transform: scale(1.08);
        }
    }


    @keyframes textFloat {

        from {
            transform: translateY(0px);
        }

        to {
            transform: translateY(-5px);
        }
    }


    /* floating decorative elements */

    .sparkle {
        position: absolute;

        color: #b77cad;

        font-size: 25px;

        animation:
            sparkleFloat 2s ease-in-out infinite alternate;
    }


    .sparkle.one {
        top: 18%;
        left: 18%;
    }


    .sparkle.two {
        top: 25%;
        right: 20%;

        animation-delay: 0.5s;
    }


    .sparkle.three {
        bottom: 20%;
        left: 25%;

        animation-delay: 1s;
    }


    .sparkle.four {
        bottom: 25%;
        right: 24%;

        animation-delay: 1.5s;
    }


    @keyframes sparkleFloat {

        from {
            transform: translateY(0px) rotate(0deg);
            opacity: 0.5;
        }

        to {
            transform: translateY(-12px) rotate(15deg);
            opacity: 1;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# CUTE GIF FOREGROUND
# =========================================================

if gif_image.exists():

    with open(gif_image, "rb") as f:
        gif_data = base64.b64encode(f.read()).decode("utf-8")

    st.markdown(
        f"""
        <style>

        /* =========================================
           GIF LAYER
           ========================================= */

        .cute-gif {{
            position: fixed;

            left: 50%;
            top: 50%;

            transform: translate(-50%, -50%);

            width: 500px;
            max-width: 45vw;

            height: auto;
            max-height: 55vh;

            object-fit: contain;

            z-index: 0;

            pointer-events: none;

            opacity: 1;

            border-radius: 25px;

            filter:
                drop-shadow(
                    0px 15px 35px
                    rgba(40, 20, 40, 0.30)
                );
        }}


        /* =========================================
           KEEP STREAMLIT CONTENT ABOVE GIF
           ========================================= */

        [data-testid="stAppViewContainer"] {{
            position: relative;
            z-index: 1;
            background: transparent !important;
        }}

        [data-testid="stMain"] {{
            position: relative;
            z-index: 2;
            background: transparent !important;
        }}

        .block-container {{
            position: relative;
            z-index: 3;
        }}

        </style>


        <img
            class="cute-gif"
            src="data:image/gif;base64,{gif_data}"
        />
        """,
        unsafe_allow_html=True
    )


# =========================================================
# TITLE
# =========================================================

st.html(
    """
    <div class="main-title-box">
        <div class="main-title">
            🌙 Does Late-Night Phone Use Affect Sleep?
        </div>
    </div>
    """
)


st.html(
    """
    <div class="subtitle-box">
        <div class="subtitle">
            Explore whether using your phone late at night is associated
            with sleep duration and sleep quality.
        </div>
    </div>
    """
)


# =========================================================
# SESSION STATE
# =========================================================

if "sleep_table" not in st.session_state:

    st.session_state.sleep_table = pd.DataFrame(
        {
            "Phone Usage After 9 PM (hours)": [None] * 5,
            "Sleep Duration (hours)": [None] * 5,
            "Sleep Quality (1-10)": [None] * 5
        }
    )


if "analysis_requested" not in st.session_state:

    st.session_state.analysis_requested = False


# =========================================================
# ENTER DATA
# =========================================================

st.markdown(
    '<div class="section-title">📝 Enter Your Data</div>',
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="helper-text">
        Enter the information below. You can add as many participants as you need.
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# CSV UPLOAD
# =========================================================

uploaded_file = st.file_uploader(
    "📂 Or upload a CSV dataset",
    type=["csv"]
)


# =========================================================
# MANUAL DATA TABLE
# =========================================================

if uploaded_file is None:

    with st.form(
        "sleep_data_form",
        clear_on_submit=False
    ):

        edited_data = st.data_editor(
            st.session_state.sleep_table,
            num_rows="dynamic",
            width="stretch",
            height=280,
            hide_index=True,
            key="sleep_editor",

            column_config={

                "Phone Usage After 9 PM (hours)":
                    st.column_config.NumberColumn(
                        "Phone Usage After 9 PM (hours)",
                        min_value=0,
                        max_value=24,
                        step=0.5
                    ),

                "Sleep Duration (hours)":
                    st.column_config.NumberColumn(
                        "Sleep Duration (hours)",
                        min_value=0,
                        max_value=24,
                        step=0.5
                    ),

                "Sleep Quality (1-10)":
                    st.column_config.NumberColumn(
                        "Sleep Quality (1-10)",
                        min_value=1,
                        max_value=10,
                        step=1
                    )
            }
        )

        submitted = st.form_submit_button(
            "🌙 ANALYZE MY DATA"
        )

else:

    submitted = st.button(
        "🌙 ANALYZE MY DATA"
    )


# =========================================================
# CUTE ANALYSIS ANIMATION
# =========================================================

def show_analysis_animation():

    if not transition_image.exists():

        return

    with open(transition_image, "rb") as f:

        transition_data = base64.b64encode(
            f.read()
        ).decode("utf-8")


    placeholder = st.empty()


    placeholder.html(
        f"""
        <div class="analysis-overlay">

            <div class="sparkle one">✦</div>

            <div class="sparkle two">✧</div>

            <div class="sparkle three">♡</div>

            <div class="sparkle four">✦</div>


            <img
                class="analysis-image"
                src="data:image/jpeg;base64,{transition_data}"
            >


            <div class="analysis-text">
                🌙 Analyzing your sleep data...
            </div>


            <div class="analysis-subtext">
                Looking for patterns between phone use and sleep ✨
            </div>

        </div>
        """
    )


    import time

    time.sleep(3)


    placeholder.empty()


# =========================================================
# HANDLE ANALYZE BUTTON
# =========================================================

if uploaded_file is None and submitted:

    # Save entered values

    st.session_state.sleep_table = edited_data.copy()


    # Tell Streamlit to show analysis

    st.session_state.analysis_requested = True


    # Show animation

    show_analysis_animation()


elif uploaded_file is not None and submitted:

    st.session_state.analysis_requested = True

    show_analysis_animation()


# =========================================================
# ANALYSIS
# =========================================================

if st.session_state.analysis_requested:


    # =====================================================
    # GET DATA
    # =====================================================

    if uploaded_file is not None:

        data = pd.read_csv(
            uploaded_file
        )

    else:

        data = st.session_state.sleep_table.copy()


    # =====================================================
    # REQUIRED COLUMNS
    # =====================================================

    required_columns = [

        "Phone Usage After 9 PM (hours)",

        "Sleep Duration (hours)",

        "Sleep Quality (1-10)"
    ]


    missing = [

        column

        for column in required_columns

        if column not in data.columns
    ]


    if missing:

        st.error(
            "Missing columns: " + ", ".join(missing)
        )

        st.stop()


    # =====================================================
    # CONVERT TO NUMBERS
    # =====================================================

    for column in required_columns:

        data[column] = pd.to_numeric(
            data[column],
            errors="coerce"
        )


    # =====================================================
    # REMOVE INCOMPLETE ROWS
    # =====================================================

    analysis_data = data.dropna(
        subset=required_columns
    ).copy()


    # =====================================================
    # MINIMUM DATA
    # =====================================================

    if len(analysis_data) < 3:

        st.warning(
            "Please enter at least 3 complete participants before running the analysis."
        )

        st.stop()


    # =====================================================
    # VARIABLES
    # =====================================================

    phone = analysis_data[
        "Phone Usage After 9 PM (hours)"
    ]


    sleep = analysis_data[
        "Sleep Duration (hours)"
    ]


    quality = analysis_data[
        "Sleep Quality (1-10)"
    ]


    # =====================================================
    # RESULT IMAGE
    # =====================================================

    if result_image.exists():

        with open(
            result_image,
            "rb"
        ) as f:

            result_data = base64.b64encode(
                f.read()
            ).decode("utf-8")


        st.html(
            f"""
            <div class="result-card">

                <div class="result-card-title">
                    🌙 Analysis Complete
                </div>

                <img
                    src="data:image/jpeg;base64,{result_data}"
                    style="
                        width:300px;
                        border-radius:16px;
                        display:block;
                        margin:auto;
                    "
                >

            </div>
            """
        )


    else:

        st.html(
            """
            <div class="result-card">

                <div class="result-card-title">
                    🌙 Analysis Complete
                </div>

            </div>
            """
        )


    # =====================================================
    # DATA OVERVIEW
    # =====================================================

    st.markdown(
        '<div class="section-title">📊 Data Overview</div>',
        unsafe_allow_html=True
    )


    overview1, overview2, overview3 = st.columns(3)


    with overview1:

        st.metric(
            "Participants",
            len(analysis_data)
        )


    with overview2:

        st.metric(
            "Average Sleep",
            f"{sleep.mean():.1f} hrs"
        )


    with overview3:

        st.metric(
            "Average Sleep Quality",
            f"{quality.mean():.1f}/10"
        )


    # =====================================================
    # CORRELATION
    # =====================================================

    correlation, p_value = pearsonr(
        phone,
        sleep
    )


    # =====================================================
    # GRAPH 1
    # =====================================================

    st.markdown(
        """
        <div class="section-title">
            📈 Late-Night Phone Use vs Sleep Duration
        </div>
        """,
        unsafe_allow_html=True
    )


    fig, ax = plt.subplots(
        figsize=(7, 4)
    )


    sns.regplot(
        x=phone,
        y=sleep,

        scatter_kws={
            "s": 55
        },

        line_kws={
            "linewidth": 2
        },

        ax=ax
    )


    ax.set_xlabel(
        "Phone Usage After 9 PM (hours)"
    )


    ax.set_ylabel(
        "Sleep Duration (hours)"
    )


    ax.set_title(
        "Late-Night Phone Use vs Sleep Duration"
    )


    ax.grid(
        alpha=0.15
    )


    fig.tight_layout()


    st.pyplot(
        fig,
        use_container_width=False
    )


    plt.close(fig)


    # =====================================================
    # STATISTICAL RESULT
    # =====================================================

    st.markdown(
        '<div class="section-title">🧪 Statistical Result</div>',
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Correlation (r)",
            f"{correlation:.3f}"
        )


    with col2:

        st.metric(
            "P-value",
            f"{p_value:.4f}"
        )


    if correlation < 0:

        st.write(
            "📉 Higher late-night phone usage is associated with lower sleep duration."
        )


    elif correlation > 0:

        st.write(
            "📈 Higher late-night phone usage is associated with higher sleep duration."
        )


    else:

        st.write(
            "There is no linear relationship between the two variables in this dataset."
        )


    if p_value < 0.05:

        st.success(
            "The relationship is statistically significant."
        )


    else:

        st.info(
            "The relationship is not statistically significant."
        )


    # =====================================================
    # LOW VS HIGH PHONE USAGE
    # =====================================================

    st.markdown(
        '<div class="section-title">👥 Low vs High Phone Usage</div>',
        unsafe_allow_html=True
    )


    threshold = 2


    low = analysis_data[
        phone < threshold
    ]


    high = analysis_data[
        phone >= threshold
    ]


    group_names = []

    group_values = []


    if len(low) > 0:

        group_names.append(
            "Low Usage"
        )

        group_values.append(
            low[
                "Sleep Duration (hours)"
            ].mean()
        )


    if len(high) > 0:

        group_names.append(
            "High Usage"
        )

        group_values.append(
            high[
                "Sleep Duration (hours)"
            ].mean()
        )


    if len(group_names) > 0:

        fig2, ax2 = plt.subplots(
            figsize=(6, 3.5)
        )


        ax2.bar(
            group_names,
            group_values
        )


        ax2.set_ylabel(
            "Average Sleep (hours)"
        )


        ax2.set_title(
            "Average Sleep by Phone Usage"
        )


        ax2.grid(
            axis="y",
            alpha=0.15
        )


        fig2.tight_layout()


        st.pyplot(
            fig2,
            use_container_width=False
        )


        plt.close(fig2)


    # =====================================================
    # T-TEST
    # =====================================================

    if len(low) >= 2 and len(high) >= 2:

        t_stat, t_p = ttest_ind(

            low[
                "Sleep Duration (hours)"
            ],

            high[
                "Sleep Duration (hours)"
            ],

            equal_var=False
        )


        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "T-statistic",
                f"{t_stat:.3f}"
            )


        with col2:

            st.metric(
                "T-test p-value",
                f"{t_p:.4f}"
            )


    else:

        st.caption(
            "Add at least two participants in each group to perform the t-test."
        )


    # =====================================================
    # PHONE USE VS SLEEP QUALITY
    # =====================================================

    quality_corr, quality_p = pearsonr(
        phone,
        quality
    )


    st.markdown(
        """
        <div class="section-title">
            😴 Phone Use vs Sleep Quality
        </div>
        """,
        unsafe_allow_html=True
    )


    fig3, ax3 = plt.subplots(
        figsize=(7, 4)
    )


    sns.regplot(
        x=phone,
        y=quality,

        scatter_kws={
            "s": 55
        },

        line_kws={
            "linewidth": 2
        },

        ax=ax3
    )


    ax3.set_xlabel(
        "Phone Usage After 9 PM (hours)"
    )


    ax3.set_ylabel(
        "Sleep Quality (1-10)"
    )


    ax3.set_title(
        "Phone Use vs Sleep Quality"
    )


    ax3.grid(
        alpha=0.15
    )


    fig3.tight_layout()


    st.pyplot(
        fig3,
        use_container_width=False
    )


    plt.close(fig3)


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "Quality Correlation",
            f"{quality_corr:.3f}"
        )


    with col2:

        st.metric(
            "Quality P-value",
            f"{quality_p:.4f}"
        )


    # =====================================================
    # CONCLUSION
    # =====================================================

    st.markdown(
        '<div class="section-title">💡 Conclusion</div>',
        unsafe_allow_html=True
    )


    if p_value < 0.05 and correlation < 0:

        st.success(
            "The data shows a statistically significant negative relationship "
            "between late-night phone usage and sleep duration."
        )


    elif p_value < 0.05:

        st.info(
            "The data shows a statistically significant relationship "
            "between late-night phone usage and sleep duration."
        )


    else:

        st.warning(
            "The data does not provide enough evidence of a statistically "
            "significant relationship between late-night phone usage and sleep duration."
        )


    st.caption(
        "Correlation does not prove causation. These results describe "
        "the relationship observed in this dataset."
    )