import streamlit as st
from PIL import Image

# Page config
st.set_page_config(page_title="WellnessBuddy", layout="wide", initial_sidebar_state="collapsed")


def topbar():
    st.markdown(
        """
        <style>
            /* Fixed topbar styling */
            .fixed-top {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                background-color: #d6abab;    /* dark gray */
                padding: 1rem 2rem;
                color: white;
                font-weight: bold;
                font-size: 1.5rem;
                z-index: 1000;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            }
            /* Links inside the topbar */
            .fixed-top a {
                color: #61dafb;
                text-decoration: none;
                margin-left: 20px;
                font-weight: normal;
                font-size: 1rem;
            }
            .fixed-top a:hover {
                text-decoration: underline;
            }
        </style>
        <div class="fixed-top">
            🦾 WellnessBuddy
            <a href="#" onclick="window.location.reload()">Home</a>
            <a href="#profile">Profile</a>
            <a href="#settings">Settings</a>
        </div>
        <!-- Spacer to push the rest of the content below the topbar -->
        <div style="height: 80px;"></div>
        """,
        unsafe_allow_html=True,
    )


# Avatar images (use your actual image paths)
avatar_paths = {
    "Max Bauer": "data\Calisthenics.jpg",      # Calisthenics
    "Liam Carter": "data\Gym.jpg",  # Strength
    "Sofia Müller": "data\Yoga.jpg" # Yoga
}

# App branding banner
def app_header():
    st.markdown("""
        <div style='background-color:#0E1117;padding:1.5rem;border-radius:10px;margin-bottom:20px;'>
            <h1 style='color:white;text-align:center;'>🏋️‍♀️ WellnessBuddy</h1>
            <p style='color:#d1d1d1;text-align:center;font-size:18px;'>Your AI-powered personalized fitness journey 💪</p>
        </div>
    """, unsafe_allow_html=True)

# Main routing logic
def main():
    # Insert the fixed topbar
    topbar()

    if 'page' not in st.session_state:
        st.session_state.page = 'welcome'
    if 'selected_coach' not in st.session_state:
        st.session_state.selected_coach = None
    elif st.session_state.page == 'exercise_demo':
        show_exercise_demo()

    app_header()
    
    if st.session_state.page == 'welcome':
        show_welcome()
    elif st.session_state.page == 'biomarkers':
        show_biomarkers()
    elif st.session_state.page == 'preferences':
        show_preferences()
    elif st.session_state.page == 'leaderboard':
        show_leaderboard()

def show_welcome():
    st.markdown("### 🌟 Welcome to WellnessBuddy")
    st.write("Ready to level up your health with expert-guided workouts, personalized plans, and social motivation?")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Get Started"):
        st.session_state.page = 'biomarkers'

def show_biomarkers():
    st.markdown("### 🔬 Enter Your Biomarkers")
    st.markdown("#### Help us tailor your fitness journey")

    with st.container():
        cols = st.columns(2)
        with cols[0]:
            age = st.slider("🎂 Age", 10, 80, 25)
            height = st.number_input("📏 Height (cm)", 100, 220, 170)
        with cols[1]:
            weight = st.number_input("⚖️ Weight (kg)", 30, 200, 70)
            resting_hr = st.selectbox("❤️ Resting Heart Rate (bpm)", list(range(40, 101)))

    fitness_level = st.selectbox("📊 Fitness Level", ["Beginner", "Intermediate", "Advanced"])

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("➡️ Next"):
        st.session_state.update({
            'age': age,
            'weight': weight,
            'height': height,
            'resting_hr': resting_hr,
            'fitness_level': fitness_level,
            'page': 'preferences'
        })

def show_leaderboard():
    st.markdown("### 🏆 Leaderboard")
    st.markdown("#### Compete with friends and stay on top!")

    leaderboard_data = [
        {"name": "Alice 🔥", "score": 920},
        {"name": "Bob ⚡", "score": 875},
        {"name": "Charlie 🌪️", "score": 860},
        {"name": "You ⭐", "score": 790},
    ]

    with st.container():
        for rank, user in enumerate(leaderboard_data, 1):
            st.markdown(f"""
            <div style='padding:10px;margin-bottom:10px;background-color:#f5f5f5;border-radius:8px'>
                <strong>{rank}. {user['name']}</strong> — <span style='color:green;'>{user['score']} pts</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Start Over"):
        st.session_state.page = 'welcome'
        st.session_state.selected_coach = None

def show_preferences():
    st.markdown("### 🧘 Choose Your Coach & Workout Style")
    st.markdown("#### Swipe through expert trainers to personalize your journey")

    trainer_names = list(avatar_paths.keys())

    if "trainer_index" not in st.session_state:
        st.session_state.trainer_index = 0

    total = len(trainer_names)
    idx = st.session_state.trainer_index
    selected_name = trainer_names[idx]

    col1, col2, col3 = st.columns([1, 3, 1])

    with col1:
        if st.button("⬅️", key="left"):
            st.session_state.trainer_index = (idx - 1) % total

    with col2:
        st.markdown(f"#### {selected_name}")
        try:
            img = Image.open(avatar_paths[selected_name])
            st.image(img, use_column_width=True)
        except:
            st.warning("Image not found")

        if st.button(f"✅ Select {selected_name}"):
            st.session_state.selected_coach = selected_name

        if st.session_state.selected_coach == selected_name:
            st.success("🎉 You selected this coach!")

    with col3:
        if st.button("➡️", key="right"):
            st.session_state.trainer_index = (idx + 1) % total



    if st.button("➡️ Proceed to Demo"):
        if st.session_state.selected_coach is None:
            st.error("Please select a coach to continue.")
        else:
            st.session_state.page = 'exercise_demo'


def show_exercise_demo():
    st.markdown("## 🎥 Exercise Demo")
    st.markdown("Watch and follow along with your personalized training demo.")

    coach = st.session_state.get("selected_coach")
    st.write("Selected coach:", coach)

    coach_to_video = {
        "Sofia Müller": "data\yoga.mp4",
        "Max Bauer": "data\pushup.mp4",
        "Liam Carter": "data\lateral_raises.mp4"
    }

  

    if coach:
        video_path = coach_to_video.get(coach)
        st.write("Video path:", video_path)

        if video_path:
            st.video(video_path)
        else:
            st.error("No video found for this coach.")
    else:
        st.warning("Please select a coach first.")
        st.markdown("<br>", unsafe_allow_html=True)

    if st.button("➡️ Proceed to Leaderboard"):
        if st.session_state.selected_coach is None:
            st.error("Please select a coach to continue.")
        else:
            st.session_state.page = 'leaderboard'


# Run app
if __name__ == "__main__":
    main()
