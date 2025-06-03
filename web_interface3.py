import streamlit as st
from PIL import Image

# Page config
st.set_page_config(page_title="WellnessBuddy", layout="wide", initial_sidebar_state="collapsed")


def topbar():
    st.markdown(
        """
        <style>
            /* Hide Streamlit's default header */
            .stApp > header {
                background-color: transparent;
            }
            
            /* Fixed topbar styling */
            .fixed-top {
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                background-color: #a65314 !important;
                padding: 1rem 2rem;
                color: white !important;
                font-weight: bold;
                font-size: 1.5rem;
                z-index: 9999 !important;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
                margin: 0;
                border: none;
                height: 80px;
                display: flex;
                align-items: center;
            }
            
            /* Ensure main content starts below topbar */
            .main .block-container {
                padding-top: 100px !important;
            }
            
            /* Reduce top padding specifically for exercise demo page */
            .exercise-demo-page .main .block-container {
                padding-top: 90px !important;
            }
            
            /* Optimize exercise demo page layout */
            .exercise-demo-container {
                padding-top: 100px !important;
                height: calc(100vh - 100px);
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }


            /* Video container styling */
            .video-container {
                flex: 1;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                max-height: calc(100vh - 200px);
                padding: 10px;
            }
            
            /* Responsive video wrapper */
            .video-wrapper {
                width: 100%;
                max-width: 800px;
                height: auto;
                max-height: 60vh;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 4px 8px srgba(0,0,0,0.1);
            }
            
            /* Video element responsive sizing */
            .video-wrapper video {
                width: 100% !important;
                height: auto !important;
                max-height: 60vh !important;
                object-fit: contain;
            }
            
            /* Button container at bottom */
            .demo-button-container {
                padding: 20px;
                text-align: center;
                flex-shrink: 0;
            }
            
            /* Style the navigation buttons container */
            .nav-container {
                position: fixed;
                top: 15px;
                right: 2rem;
                z-index: 10000;
                display: flex;
                gap: 10px;
            }
        </style>
        <div class="fixed-top">
            🦾 WellnessBuddy
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Create navigation buttons positioned in the topbar area
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    
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
        if st.button("💪 Program", key="nav_program", use_container_width=True):
            # If no coach is selected, default to Max Bauer
            if st.session_state.selected_coach is None:
                st.session_state.selected_coach = "Coach Bauer"
            st.session_state.page = 'exercise_demo'
            st.rerun()
    
    with nav_col4:
        if st.button("⚙️ Settings", key="nav_settings", use_container_width=True):
            st.info("Settings page coming soon!")
    
    st.markdown('</div>', unsafe_allow_html=True)


# Avatar images (use your actual image paths)
avatar_paths = {
    "Coach Bauer": "data\Calisthenics.jpg",      # Calisthenics
    "Coach Carter": "data\Gym.jpg",  # Strength
    "Coach Fang": "data\Yoga.jpg" # Yoga
}

# Coach descriptions
coach_descriptions = {
    "Coach Bauer": "🏃‍♂️ Calisthenics Expert - Master bodyweight movements and build functional strength",
    "Coach Carter": "💪 Strength Training - Build muscle and power with proven weightlifting techniques", 
    "Coach Fang": "🧘‍♀️ Yoga & Flexibility - Improve balance, flexibility, and mindfulness"
}

# App branding banner (removed - no longer used)
def app_header():
    pass

# Compact header for exercise demo page (removed - no longer used)
def compact_header():
    pass

# Main routing logic
def main():
    # Insert the fixed topbar
    topbar()

    if 'page' not in st.session_state:
        st.session_state.page = 'welcome'
    if 'selected_coach' not in st.session_state:
        st.session_state.selected_coach = None

    # No headers needed - removed conditional header calls
    
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
    st.markdown("""
    <style>
    .leaderboard-container {
        background: linear-gradient(135deg, #1f1c2c, #FFAB0F);
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        color: white;
    }
    .leaderboard-title {
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
        color: #FFD700;
    }
    .player-entry {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 10px 20px;
        margin-bottom: 12px;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .player-rank {
        font-size: 20px;
        font-weight: bold;
        width: 40px;
    }
    .player-name {
        flex: 1;
        font-size: 18px;
        margin-left: 10px;
    }
    .player-stars {
        color: gold;
        font-size: 18px;
        margin-right: 15px;
    }
    .player-score {
        font-weight: bold;
        font-size: 18px;
    }
    </style>

    <div class="leaderboard-container">
        <div class="leaderboard-title">🏆 Leaderboard</div>
    """, unsafe_allow_html=True)

    leaderboard_data = [
        {"name": "Alice 🔥", "score": 2980, "stars": 5, "medal": "🥇"},
        {"name": "Bob ⚡", "score": 2721, "stars": 4.5, "medal": "🥈"},
        {"name": "Charlie 🌪️", "score": 2579, "stars": 4, "medal": "🥉"},
        {"name": "You ⭐", "score": 1874, "stars": 3.5, "medal": "4️⃣"},
        {"name": "David 💥", "score": 1756, "stars": 3, "medal": "5️⃣"},
    ]

    for idx, player in enumerate(leaderboard_data):
        stars = '★' * int(player['stars']) + ('½' if player['stars'] % 1 != 0 else '')
        st.markdown(f"""
        <div class="player-entry">
            <div class="player-rank">{player['medal']}</div>
            <div class="player-name">{player['name']}</div>
            <div class="player-stars">{stars}</div>
            <div class="player-score">{player['score']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""</div><br>""", unsafe_allow_html=True)
    if st.button("🔄 Start Over"):
        st.session_state.page = 'welcome'
        st.session_state.selected_coach = None

def show_preferences():
    st.markdown("### 🧘 Choose Your AI Coach & Workout Style To Personalize Your Journey")

    # Display all three coaches in columns
    col1, col2, col3 = st.columns(3)
    
    trainer_names = list(avatar_paths.keys())
    
    with col1:
        coach_name = trainer_names[0]  # Max Bauer
        st.markdown(f"#### {coach_name}")
        
        try:
            img = Image.open(avatar_paths[coach_name])
            st.image(img, use_container_width=True)
        except:
            st.warning("Image not found")
        
        st.markdown(f"*{coach_descriptions[coach_name]}*")
        
        if st.button(f"✅ Select {coach_name}", key="select_max"):
            st.session_state.selected_coach = coach_name
        
        if st.session_state.selected_coach == coach_name:
            st.success("🎉 Selected!")

    with col2:
        coach_name = trainer_names[1]  # Liam Carter
        st.markdown(f"#### {coach_name}")
        
        try:
            img = Image.open(avatar_paths[coach_name])
            st.image(img, use_container_width=True)
        except:
            st.warning("Image not found")
        
        st.markdown(f"*{coach_descriptions[coach_name]}*")
        
        if st.button(f"✅ Select {coach_name}", key="select_liam"):
            st.session_state.selected_coach = coach_name
        
        if st.session_state.selected_coach == coach_name:
            st.success("🎉 Selected!")

    with col3:
        coach_name = trainer_names[2]  # Sofia Müller
        st.markdown(f"#### {coach_name}")
        
        try:
            img = Image.open(avatar_paths[coach_name])
            st.image(img, use_container_width=True)
        except:
            st.warning("Image not found")
        
        st.markdown(f"*{coach_descriptions[coach_name]}*")
        
        if st.button(f"✅ Select {coach_name}", key="select_sofia"):
            st.session_state.selected_coach = coach_name
        
        if st.session_state.selected_coach == coach_name:
            st.success("🎉 Selected!")

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("➡️ Proceed to Demo"):
        if st.session_state.selected_coach is None:
            st.error("Please select a coach to continue.")
        else:
            st.session_state.page = 'exercise_demo'


def show_exercise_demo():
    # Add custom CSS for responsive video layout
    st.markdown("""
    <style>
    /* Responsive video sizing without layout constraints */
    .stVideo > div {
        max-height: 60vh !important;
    }
    
    .stVideo video {
        max-height: 60vh !important;
        width: 100% !important;
        object-fit: contain !important;
        border-radius: 10px !important;
    }
    
    /* Media queries for different screen sizes */
    @media (max-width: 768px) {
        .stVideo video {
            max-height: 50vh !important;
        }
    }
    
    @media (max-width: 480px) {
        .stVideo video {
            max-height: 40vh !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("## 🎥 Exercise Demo", unsafe_allow_html=True)

    coach = st.session_state.get("selected_coach")
    
    coach_to_video = {
        "Coach Fang": "data\yoga.mp4",
        "Coach Bauer": "data\pushup.mp4",
        "Coach Carter": "data\lateral_raises.mp4"
    }

    if coach:
        video_path = coach_to_video.get(coach)
        
        if video_path:
            # Create columns for centering
            col1, col2, col3 = st.columns([1, 3, 1])
            with col2:
                st.video(video_path, autoplay=True)
        else:
            st.error("No video found for this coach.")
    else:
        st.warning("Please select a coach first.")

    # Button in a container at the bottom
    st.markdown("<div style='text-align: center; padding-top: 20px;'>", unsafe_allow_html=True)
    if st.button("➡️ Proceed to Leaderboard", key="proceed_leaderboard"):
        if st.session_state.selected_coach is None:
            st.error("Please select a coach to continue.")
        else:
            st.session_state.page = 'leaderboard'
    st.markdown("</div>", unsafe_allow_html=True)


# Run app
if __name__ == "__main__":
    main()