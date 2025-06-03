import streamlit as st
from PIL import Image

# Set page config
st.set_page_config(page_title="WellnessBuddy App", layout="wide")

# Sample avatars (replace these with your actual image paths)
avatar_paths = {
    "Max Bauer": "max_bauer.jpg",      # Calisthenics
    "Liam Carter": "liam_carter.jpg",  # Strength
    "Sofia Müller": "sofia_muller.jpg" # Yoga
}

def main():
    if 'page' not in st.session_state:
        st.session_state.page = 'welcome'
    if 'selected_coach' not in st.session_state:
        st.session_state.selected_coach = None

    if st.session_state.page == 'welcome':
        show_welcome()
    elif st.session_state.page == 'biomarkers':
        show_biomarkers()
    elif st.session_state.page == 'preferences':
        show_preferences()
    elif st.session_state.page == 'leaderboard':
        show_leaderboard()

def show_welcome():
    st.title("Welcome to WellnessBuddy")
    st.subheader("Your personalized wellness journey starts here ✨")

    if st.button("Get Started ➡️"):
        st.session_state.page = 'biomarkers'

def show_biomarkers():
    st.title("🔬 Enter Your Biomarkers")
    age = st.slider("Age", 10, 80, 25)
    weight = st.number_input("Weight (kg)", 30, 200, 70)
    height = st.number_input("Height (cm)", 100, 220, 170)
    resting_hr = st.selectbox("Resting Heart Rate (bpm)", list(range(40, 101)))
    fitness_level = st.selectbox("Fitness Level", ["Beginner", "Intermediate", "Advanced"])

    if st.button("Next ➡️"):
        # Store biomarker data if needed:
        st.session_state.age = age
        st.session_state.weight = weight
        st.session_state.height = height
        st.session_state.resting_hr = resting_hr
        st.session_state.fitness_level = fitness_level
        st.session_state.page = 'preferences'

def show_preferences():
    st.title("🧘 Choose Your Coach & Style")

    cols = st.columns(3)
    for i, (name, path) in enumerate(avatar_paths.items()):
        with cols[i]:
            try:
                img = Image.open(path)
                st.image(img, caption=name, use_column_width=True)
            except:
                st.write("[Avatar image not found]")
                st.write(name)

            if st.button(f"Select {name}"):
                st.session_state.selected_coach = name

            if st.session_state.selected_coach == name:
                st.markdown(f"✅ **{name} selected**")

    st.write("---")
    if st.button("Next ➡️ Go to Leaderboard"):
        if st.session_state.selected_coach is None:
            st.warning("Please select a coach before continuing.")
        else:
            st.session_state.page = 'leaderboard'

def show_leaderboard():
    st.title("🏆 Leaderboard")
    st.write("Here are top users based on accuracy & consistency:")

    leaderboard_data = [
        {"name": "Alice", "score": 920},
        {"name": "Bob", "score": 875},
        {"name": "Charlie", "score": 860},
        {"name": "You", "score": 790},
    ]

    for rank, user in enumerate(leaderboard_data, 1):
        st.write(f"**{rank}. {user['name']}** — {user['score']} pts")

    if st.button("🔁 Start Over"):
        st.session_state.page = 'welcome'
        st.session_state.selected_coach = None

if __name__ == "__main__":
    main()
