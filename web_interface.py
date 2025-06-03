import streamlit as st
from PIL import Image

# Page config - Keep it wide
st.set_page_config(page_title="WellnessBuddy", layout="wide", initial_sidebar_state="collapsed")

# --- INITIALIZE SESSION STATE AT THE TOP ---
# This is crucial to prevent AttributeError on initial load and subsequent reruns
if 'page' not in st.session_state:
    st.session_state.page = 'welcome'
if 'selected_coach' not in st.session_state:
    st.session_state.selected_coach = None
if 'selected_program_step' not in st.session_state:
    # Set default to 3 (Lateral Raises) for the initial load
    st.session_state.selected_program_step = 3
# --- END SESSION STATE INITIALIZATION ---


def topbar():
    st.markdown(
        """
        <style>
            /* Global Styles & Theming */
            :root {
                --primary-color: #7a431a; /* Your current topbar color */
                --secondary-color: #ba6322; /* Your desired button pink */
                --text-color: #E0E0E0; /* Light gray for text */
                --background-color: #1A1A1A; /* Dark background */
                --card-background: #2B2B2B; /* Slightly lighter dark for cards/containers */
                --border-color: rgba(255, 255, 255, 0.1);
                --shadow-color: rgba(0, 0, 0, 0.3);
                --font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            }

            body {
                font-family: var(--font-family);
                color: var(--text-color);
                background-color: var(--background-color);
            }

            /* --- CRITICAL: ZERO OUT ALL POTENTIAL TOP SPACING --- */

            /* Target the main Streamlit app container itself */
            .stApp {
                padding-top: 0px !important;
                margin-top: 0px !important;
            }

            /* Hide Streamlit's default header */
            .stApp > header {
                background-color: transparent;
                height: 0px !important; /* Force hide the header */
                margin-top: 0px !important;
                padding-top: 0px !important;
            }

            /* Target the primary content block */
            .main {
                padding-top: 0px !important;
                margin-top: 0px !important;
            }

            /* Target the specific block container that holds your content */
            .block-container {
                padding-top: 0px !important;
                margin-top: 0px !important;
            }

            /* Target the div that usually wraps ALL user-defined content within the main area */
            /* This is a very common culprit for the top gap */
            [data-testid="stVerticalBlock"] {
                padding-top: 0px !important;
                margin-top: 0px !important;
            }

            /* Target the first immediate child of the main block container */
            /* This is also a very common culprit, effectively pulling up the first visible element */
            .main .block-container > div:first-child {
                padding-top: 0px !important;
                margin-top: -80px !important; /* Adjust this value (-70px, -90px etc.) if the alignment isn't perfect */
            }

            /* If the issue persists, try making the negative margin even larger */
            .main .block-container > div:first-child > div {
                padding-top: 0px !important;
                margin-top: 0px !important;
            }

            /* --- END CRITICAL SPACING FIXES --- */


            /* Fixed topbar styling */
            .fixed-top-container {
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                background-color: var(--primary-color) !important;
                padding: 1rem 2rem;
                color: white !important;
                font-weight: bold;
                font-size: 1.5rem;
                z-index: 9999 !important;
                box-shadow: 0 2px 4px var(--shadow-color);
                margin: 0;
                border: none;
                height: 80px; /* Fixed height for the top bar */
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            .fixed-top-brand {
                font-size: 1.8rem;
                letter-spacing: 1px;
                color: white;
                display: flex;
                align-items: center;
                gap: 10px;
            }

            /* Ensure main content starts BELOW the fixed topbar */
            section.main {
                padding-top: 80px !important; /* Push main content down by topbar height */
            }

            /* Global padding for the main content area */
            .main .block-container {
                padding-left: 2rem !important;
                padding-right: 2rem !important;
                padding-bottom: 2rem !important; /* Ensure some bottom padding too */
            }


            /* Exercise Demo Page Specific Adjustments */
            .exercise-demo-page .main .block-container {
                min-height: calc(100vh - 80px);
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }

            /* Video container styling (centralized) */
            .video-container {
                flex-grow: 1;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                padding: 10px;
                max-height: calc(100vh - 250px);
                overflow: hidden;
            }

            [data-testid="stVideo"] {
                width: 100%;
                display: flex;
                justify-content: center;
                align-items: center;
                margin: 0 auto;
                max-width: 700px;
            }

            [data-testid="stVideo"] video {
                width: 100% !important;
                height: auto !important;
                max-height: calc(100vh - 280px) !important; /* Adjust if header or button height changes */
                object-fit: contain !important;
                border-radius: 15px;
                box-shadow: 0 8px 25px var(--shadow-color);
                border: 1px solid var(--border-color);
            }

            /* Button container at bottom (for exercise demo) */
            .demo-button-container {
                padding-top: 20px;
                padding-bottom: 20px;
                text-align: center;
                flex-shrink: 0;
                margin-top: auto;
            }

            /* Styling for ALL Streamlit buttons by default */
            .stButton > button {
                background-color: var(--secondary-color) !important;
                color: white !important;
                border: none !important;
                padding: 0.7rem 1.5rem !important;
                border-radius: 0.7rem !important;
                font-weight: bold !important;
                font-size: 1rem !important;
                cursor: pointer;
                transition: background-color 0.3s ease, transform 0.2s ease, box-shadow 0.2s ease !important;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }

            .stButton > button:hover {
                background-color: #7a431a !important;
                transform: translateY(-2px);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
            }

            .stButton > button:active {
                transform: translateY(0);
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            }

            /* Specific styling for the top navigation buttons */
            .nav-buttons-container [data-testid="stColumn"] > .stButton > button {
                background-color: var(--secondary-color) !important;
                color: white !important;
            }
            .nav-buttons-container [data-testid="stColumn"] > .stButton > button:hover {
                background-color: #FF1493 !important;
            }

            /* For the "Program" button when active */
            .stButton[data-testid="stButton-nav_program"] > button[aria-selected="true"],
            .stButton[data-testid="stButton-nav_program"] > button.st-emotion-cache-nahz7x {
                background-color: #FF1493 !important;
                border: 2px solid white !important;
            }


            /* Styling for text inputs, sliders, selectboxes (dark theme look) */
            .stTextInput > div > div > input,
            .stSlider .stSlider > div > div > div > div,
            .stSelectbox > div > div {
                background-color: var(--card-background);
                border: 1px solid var(--border-color);
                color: var(--text-color);
                border-radius: 0.5rem;
            }

            /* Headers */
            h1, h2, h3, h4, h5, h6 {
                color: white;
                font-weight: 600;
                margin-bottom: 0.5em;
            }

            /* Info, Warning, Error boxes */
            .stAlert {
                border-radius: 0.7rem;
            }
            .stAlert.info {
                background-color: rgba(66, 133, 244, 0.2);
                color: #8ab4f4;
                border-left: 5px solid #8ab4f4;
            }
            .stAlert.warning {
                background-color: rgba(251, 188, 5, 0.2);
                color: #fddb66;
                border-left: 5px solid #fddb66;
            }
            .stAlert.error {
                background-color: rgba(234, 67, 53, 0.2);
                color: #f28b82;
                border-left: 5px solid #f28b82;
            }
            .stAlert p {
                color: var(--text-color);
            }

            /* Container styling (for sections like leaderboard or preferences) */
            .stContainer {
                background-color: var(--card-background);
                padding: 1.5rem;
                border-radius: 10px;
                box-shadow: 0 4px 12px var(--shadow-color);
                margin-bottom: 1.5rem;
                border: 1px solid rgba(255, 255, 255, 0.08);
            }
            /* Styling for columns to add padding/gap */
            .st-emotion-cache-nahz7x,
            .st-emotion-cache-1c7y2vl,
            .st-emotion-cache-uf99v8,
            .st-emotion-cache-1r6dm7m,
            .st-emotion-cache-j7qwjs
            {
                gap: 1.5rem;
            }

            /* Ensure background of the avatar images and text look good in dark mode */
            .stImage > img {
                border-radius: 10px;
                box-shadow: 0 4px 10px var(--shadow-color);
            }
            .stMarkdown > div > p {
                color: var(--text-color);
            }

            /* Custom styles for welcome message */
            .welcome-message {
                text-align: center;
                padding: 50px 20px;
                background: linear-gradient(45deg, #1A1A1A, #2B2B2B);
                border-radius: 15px;
                margin-top: 0px !important;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            }
            .welcome-message h3 {
                font-size: 2.5rem;
                color: #FFD700;
                margin-bottom: 0.5em;
                text-shadow: 2px 2px 5px rgba(0,0,0,0.4);
            }
            .welcome-message p {
                font-size: 1.2rem;
                max-width: 700px;
                margin: 0 auto;
                line-height: 1.6;
            }
            .welcome-message .stButton button {
                margin-top: 30px;
                padding: 1rem 3rem !important;
                font-size: 1.2rem !important;
            }

            /* Specific styles for preference page coach cards */
            .coach-card-title {
                text-align: center;
                color: white;
                font-size: 1.8rem;
                margin-bottom: 10px;
            }
            .coach-description {
                font-size: 0.95rem;
                color: var(--text-color);
                min-height: 70px;
            }
            .coach-selection-container {
                background-color: var(--card-background);
                border-radius: 15px;
                padding: 20px;
                box-shadow: 0 5px 15px var(--shadow-color);
                border: 1px solid rgba(255, 255, 255, 0.08);
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
                height: 100%;
            }
            .coach-selection-container img {
                max-width: 100%;
                height: 200px;
                object-fit: cover;
                border-radius: 10px;
                margin-bottom: 15px;
                box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            }
            /* Default button styling within coach cards */
            .coach-selection-container .stButton > button {
                margin-top: auto;
                background-color: var(--secondary-color) !important; /* Default for unselected */
                border: none !important;
            }
            .coach-selection-container .stButton > button:hover {
                background-color: #FF1493 !important;
            }
            /* Styling for the *selected* coach button (when type="primary") */
            .coach-selection-container .stButton[data-baseweb="button"] > button[data-testid*="primaryButton"] {
                background-color: #4CAF50 !important; /* Distinct green for selected coaches */
                border: 2px solid white !important; /* White border to indicate selection */
                box-shadow: 0 0 15px rgba(255, 255, 255, 0.5) !important; /* Glow effect */
                transform: scale(1.02); /* Slightly larger */
            }

            .stAlert.success {
                background-color: rgba(92, 184, 92, 0.2);
                color: #dff0d8;
                border-left: 5px solid #dff0d8;
                margin-top: 15px;
                border-radius: 0.7rem;
            }
            .stSuccess {
                background-color: var(--card-background) !important;
                border-color: #5cb85c !important;
                color: #5cb85c !important;
                border-radius: 0.5rem;
                padding: 10px;
            }
            .stSuccess > div {
                color: #5cb85c !important;
            }
            .stSuccess p {
                color: var(--text-color) !important;
            }

            /* Biomarkers page specific */
            .biomarker-input-container {
                background-color: var(--card-background);
                padding: 2rem;
                border-radius: 15px;
                box-shadow: 0 5px 20px var(--shadow-color);
                border: 1px solid var(--border-color);
                max-width: 800px;
                margin: 30px auto;
            }
            .biomarker-input-container label {
                color: var(--text-color);
                font-weight: 500;
                margin-bottom: 5px;
            }

            /* Program Page Specific Styles */
            .program-list-container {
                background-color: var(--card-background);
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 5px 15px var(--shadow-color);
                border: 1px solid rgba(255, 255, 255, 0.08);
                margin-right: 20px;
                height: 100%; /* Take full height of the column */
            }
            .program-step-button {
                background-color: rgba(255, 255, 255, 0.05) !important;
                color: var(--text-color) !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
                margin-bottom: 10px;
                text-align: left;
                width: 100%;
            }
            .program-step-button:hover {
                background-color: rgba(255, 255, 255, 0.1) !important;
            }
            .program-step-button-active {
                background-color: var(--secondary-color) !important;
                color: white !important;
                border: 1px solid #FF1493 !important;
                font-weight: bold;
            }
            .program-step-button-active:hover {
                background-color: #FF1493 !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Use st.columns to create a flexible layout for the fixed top bar
    brand_col, nav_buttons_col = st.columns([0.2, 0.8])

    with brand_col:
        st.markdown('<div class="fixed-top-brand">🦾 GymGAZE</div>', unsafe_allow_html=True)

    with nav_buttons_col:
        st.markdown('<div class="nav-buttons-container">', unsafe_allow_html=True)
        nav_col1, nav_col2, nav_col3, nav_col4 = st.columns(4)

        with nav_col1:
            if st.button("🏃 Coaches", key="nav_coaches", use_container_width=True):
                st.session_state.page = 'preferences'
                st.rerun()

        with nav_col2:
            if st.button("🏆 Leaderboard", key="nav_leaderboard", use_container_width=True):
                st.session_state.page = 'leaderboard'
                st.rerun()

        with nav_col3:
            is_program_active = (st.session_state.page == 'exercise_demo')
            if st.button("💪 Program", key="nav_program", use_container_width=True, type="primary" if is_program_active else "secondary"):
                if st.session_state.selected_coach is None:
                    st.session_state.selected_coach = "Coach Bauer" # Default coach if none selected
                # When navigating to program, ensure Lateral Raises is the default shown if no specific step was selected
                if st.session_state.page != 'exercise_demo': # Only reset if coming from another page
                    st.session_state.selected_program_step = 3 # Default to Lateral Raises
                st.session_state.page = 'exercise_demo'
                st.rerun()

        with nav_col4:
            if st.button("⚙️ Settings", key="nav_settings", use_container_width=True):
                st.info("Settings page coming soon!")

        st.markdown('</div>', unsafe_allow_html=True)


# Avatar images (make sure these paths are correct relative to your script)
avatar_paths = {
    "Coach Bauer": "data/Calisthenics.jpg",        # Calisthenics
    "Coach Carter": "data/Gym.jpg",  # Strength
    "Coach Fang": "data/Yoga.jpg" # Yoga
}

# Coach descriptions
coach_descriptions = {
    "Coach Bauer": "Adaptive Wellness – Gentle, physiotherapy-informed programs designed for seniors and individuals with special needs.",
    "Coach Carter": "Strength Training - Build muscle and power with proven weightlifting techniques and structured progression.",
    "Coach Fang": "Yoga & Flexibility - Improve balance, flexibility, and mindfulness with ancient practices and modern adaptations."
}

# Main routing logic
def main():
    topbar()

    if st.session_state.page == 'welcome':
        show_welcome()
    elif st.session_state.page == 'biomarkers':
        show_biomarkers()
    elif st.session_state.page == 'preferences':
        show_preferences()
    elif st.session_state.page == 'leaderboard':
        show_leaderboard()
    elif st.session_state.page == 'exercise_demo':
        show_exercise_demo()

def show_welcome():
    st.markdown(
        """
        <div class="welcome-message">
            <h3>🌟 Welcome to GymGAZE</h3>
            <p>Ready to level up your health with our AI coaches, personalized plans?</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button("🚀 Get Started", key="get_started_welcome"):
        st.session_state.page = 'biomarkers'
    st.markdown("</div>", unsafe_allow_html=True)


def show_biomarkers():
    st.markdown("### 🔬 Enter Your Biomarkers")
    st.markdown("#### Help us tailor your fitness journey", unsafe_allow_html=True)

    st.markdown("<div class='biomarker-input-container'>", unsafe_allow_html=True)
    cols = st.columns(2)
    with cols[0]:
        age = st.slider("🎂 Age", 10, 80, 25, help="Your age helps us recommend appropriate exercises.")
    with cols[1]:
        height = st.number_input("📏 Height (cm)", 100, 220, 170, help="Your height for BMI calculations.")

    cols2 = st.columns(2)
    with cols2[0]:
        weight = st.number_input("⚖️ Weight (kg)", 30, 200, 70, help="Your weight for BMI calculations.")
    with cols2[1]:
        resting_hr = st.selectbox("❤️ Resting Heart Rate (bpm)", list(range(40, 101)), help="A lower resting heart rate often indicates better cardiovascular fitness.")

    fitness_level = st.selectbox("📊 Fitness Level", ["Beginner", "Intermediate", "Advanced"], help="Your current fitness level helps us adjust workout intensity.")
    st.markdown("</div>", unsafe_allow_html=True)


    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button("➡️ Next", key="biomarkers_next"):
        st.session_state.update({
            'age': age,
            'weight': weight,
            'height': height,
            'resting_hr': resting_hr,
            'fitness_level': fitness_level,
            'page': 'preferences'
        })
    st.markdown("</div>", unsafe_allow_html=True)

def show_leaderboard():
    st.markdown("""
    <style>
    /* Leaderboard Specific Styles */
    .leaderboard-container {
        background: var(--card-background);
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 8px 25px var(--shadow-color);
        color: var(--text-color);
        border: 1px solid var(--border-color);
        margin-top: 20px;
    }
    .leaderboard-title {
        font-size: 38px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 30px;
        color: #FFD700;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.5);
    }
    .player-entry {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 15px 25px;
        margin-bottom: 15px;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .player-entry:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.4);
    }
    .player-rank {
        font-size: 24px;
        font-weight: bold;
        width: 50px;
        text-align: center;
        color: white;
    }
    .player-name {
        flex: 1;
        font-size: 20px;
        margin-left: 15px;
        font-weight: 500;
        color: white;
    }
    .player-stars {
        color: gold;
        font-size: 20px;
        margin-right: 20px;
        letter-spacing: 2px;
    }
    .player-score-container {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        font-weight: bold;
    }
    .player-score {
        font-size: 17px;
        line-height: 1.4;
        color: #FFD700;
    }
    .player-score-label {
        font-size: 12px;
        color: var(--text-color);
        margin-bottom: 2px;
    }
    </style>

    <div class="leaderboard-container">
        <div class="leaderboard-title">🏆 Leaderboard</div>
    """, unsafe_allow_html=True)

    leaderboard_data = [
        {"name": "Alice 🔥", "weekly_score": 750, "monthly_score": 2980, "stars": 5, "medal": "🥇"},
        {"name": "Bob ⚡", "weekly_score": 680, "monthly_score": 2721, "stars": 4.5, "medal": "🥈"},
        {"name": "Charlie 🌪️", "weekly_score": 620, "monthly_score": 2579, "stars": 4, "medal": "🥉"},
        {"name": "You ⭐", "weekly_score": 450, "monthly_score": 1874, "stars": 3.5, "medal": "4️⃣"},
        {"name": "David 💥", "weekly_score": 400, "monthly_score": 1756, "stars": 3, "medal": "5️⃣"},
        {"name": "Eve 🚀", "weekly_score": 380, "monthly_score": 1600, "stars": 2.5, "medal": "6️⃣"},
    ]

    for idx, player in enumerate(leaderboard_data):
        stars = '★' * int(player['stars']) + ('½' if player['stars'] % 1 != 0 else '')
        if player['name'] == "You ⭐":
            entry_style = "background-color: rgba(255, 215, 0, 0.15); border: 1px solid #FFD700;"
            player['medal'] = "🌟"
        else:
            entry_style = ""

        st.markdown(f"""
        <div class="player-entry" style="{entry_style}">
            <div class="player-rank">{player['medal']}</div>
            <div class="player-name">{player['name']}</div>
            <div class="player-stars">{stars}</div>
            <div class="player-score-container">
                <span class="player-score-label">Weekly</span>
                <div class="player-score">{player['weekly_score']}</div>
                <span class="player-score-label">Monthly</span>
                <div class="player-score">{player['monthly_score']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""</div><br>""", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button("🔄 Start Over", key="leaderboard_start_over"):
        st.session_state.page = 'welcome'
        st.session_state.selected_coach = None
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


def show_preferences():
    st.markdown("### 🧘 Choose Your AI Coach & Personalize Your Journey")

    cols = st.columns(3)

    trainer_names = list(avatar_paths.keys())

    for i, coach_name in enumerate(trainer_names):
        with cols[i]:
            st.markdown(f"""
                <div class="coach-selection-container">
                    <h4 class="coach-card-title">{coach_name}</h4>
                """, unsafe_allow_html=True)

            try:
                img = Image.open(avatar_paths[coach_name])
                st.image(img, caption=coach_name, use_container_width=True)
            except Exception as e:
                st.warning(f"Image for {coach_name} not found: {e}")

            st.markdown(f"<p class='coach-description'>*{coach_descriptions[coach_name]}*</p>", unsafe_allow_html=True)

            # Determine button type based on selection for visual feedback
            # Using type="primary" for selected, "secondary" for unselected
            button_type = "primary" if st.session_state.selected_coach == coach_name else "secondary"

            if st.button(
                f"✅ Select {coach_name}",
                key=f"select_{coach_name.replace(' ', '_').lower()}",
                use_container_width=True,
                type=button_type # Apply the type here
            ):
                st.session_state.selected_coach = coach_name
                st.rerun() # Rerun to update button styling immediately

            # Display "Selected!" message only below the selected coach
            if st.session_state.selected_coach == coach_name:
                st.success("🎉 Selected!")

            st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    if st.button("➡️ Proceed to Demo", key="proceed_to_demo_preferences"):
        if st.session_state.selected_coach is None:
            st.error("Please select a coach to continue.")
        else:
            st.session_state.page = 'exercise_demo'
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


def show_exercise_demo():
    st.markdown("<div class='exercise-demo-page'>", unsafe_allow_html=True)

    st.markdown("<h2 style='text-align: center; color: white; margin-bottom: 20px;'>🎥 Exercise Demo</h2>", unsafe_allow_html=True)

    coach = st.session_state.get("selected_coach")

    # Define program steps and their corresponding videos
    # Make sure you have these video files in your 'data' folder
    program_steps = {
        1: {"name": "1: Warm-up", "video": None},
        2: {"name": "2: Stretching", "video": "data/yoga.mp4"},
        3: {"name": "3: Lateral Raises", "video": "data/lateral_raises.mp4"},
        4: {"name": "4: Push-ups", "video": "data/pushup.mp4"},
        5: {"name": "5: Physiotherapy", "video": None}, # 
    }

    # Create two columns: one for the program list and one for the video
    program_col, video_col = st.columns([0.3, 0.7]) # Adjust ratios as needed

    with program_col:
        st.markdown("<div class='program-list-container'>", unsafe_allow_html=True)
        st.markdown("<h4>Daily Program:</h4>", unsafe_allow_html=True)
        for step_num, step_info in program_steps.items():
            is_active = (st.session_state.selected_program_step == step_num)
            
            # Use Streamlit's built-in button type for "primary" if active, "secondary" otherwise
            # This makes the active button stand out without custom CSS workarounds
            button_type = "primary" if is_active else "secondary"

            if st.button(
                step_info["name"],
                key=f"program_step_{step_num}",
                use_container_width=True,
                type=button_type, # Apply the type here
                help=f"Click to play {step_info['name']}"
            ):
                st.session_state.selected_program_step = step_num
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    with video_col:
        current_video_path = program_steps.get(st.session_state.selected_program_step, {}).get("video")

        if current_video_path:
            st.markdown("<div class='video-container'>", unsafe_allow_html=True)
            st.video(current_video_path, autoplay=True, loop=True, muted=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("No video found for the selected program step. Please check the 'data' folder.")
            # Optionally set a default video if one is missing
            # st.video("data/default_placeholder.mp4")
            
    st.markdown("<div class='demo-button-container'>", unsafe_allow_html=True)
    if st.button("➡️ Proceed to Leaderboard", key="proceed_leaderboard_demo"):
        st.session_state.page = 'leaderboard'
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# Run app
if __name__ == "__main__":
    main()