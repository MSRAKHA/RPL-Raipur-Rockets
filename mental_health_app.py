import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import json

# Initialize session state variables
if 'mood_data' not in st.session_state:
    st.session_state.mood_data = []
if 'activities' not in st.session_state:
    st.session_state.activities = []
if 'sleep_data' not in st.session_state:
    st.session_state.sleep_data = []

class MentalHealthApp:
    def __init__(self):
        pass

    def save_data(self):
        """Save data to JSON file"""
        data = {
            'mood_data': st.session_state.mood_data,
            'activities': st.session_state.activities,
            'sleep_data': st.session_state.sleep_data
        }
        with open('mental_health_data.json', 'w') as f:
            json.dump(data, f)

    def load_data(self):
        """Load data from JSON file"""
        try:
            with open('mental_health_data.json', 'r') as f:
                data = json.load(f)
                st.session_state.mood_data = data.get('mood_data', [])
                st.session_state.activities = data.get('activities', [])
                st.session_state.sleep_data = data.get('sleep_data', [])
        except FileNotFoundError:
            pass

    def main_page(self):
        """Main page layout"""
        st.title("**🧠 :rainbow[Mental Health Tracker]**")
        
        # Sidebar navigation
        page = st.sidebar.radio("**:rainbow[Navigate]**", 
            ["Dashboard", "Track Mood", "Track Activities", "Track Sleep", "Analysis & Insights"])
        
        if page == "Dashboard":
            self.show_dashboard()
        elif page == "Track Mood":
            self.track_mood()
        elif page == "Track Activities":
            self.track_activities()
        elif page == "Track Sleep":
            self.track_sleep()
        elif page == "Analysis & Insights":
            self.show_analysis()

    def track_mood(self):
        """Mood tracking interface"""
        st.subheader("Track Your Mood")
        
        mood_scale = {
            "Excellent": 5,
            "Good": 4,
            "Neutral": 3,
            "Low": 2,
            "Very Low": 1
        }
        
        col1, col2 = st.columns(2)
        
        with col1:
            mood = st.select_slider(
                "How are you feeling?",
                options=list(mood_scale.keys())
            )
            
        with col2:
            notes = st.text_area("Any notes about your day?")
        
        if st.button("Log Mood"):
            mood_entry = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "mood": mood,
                "mood_value": mood_scale[mood],
                "notes": notes
            }
            st.session_state.mood_data.append(mood_entry)
            self.save_data()
            st.success("Mood logged successfully!")

    def track_activities(self):
        """Activity tracking interface"""
        st.subheader("Track Your Activities")
        
        activities = ["Exercise", "Meditation", "Reading", "Socializing", "Therapy", "Other"]
        
        col1, col2 = st.columns(2)
        
        with col1:
            activity = st.selectbox("Select Activity", activities)
            if activity == "Other":
                activity = st.text_input("Specify activity")
                
        with col2:
            duration = st.number_input("Duration (minutes)", 
                                     min_value=5, 
                                     max_value=150,
                                     value=30,
                                     step=5)
        
        if st.button("Log Activity"):
            activity_entry = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "activity": activity,
                "duration": duration
            }
            st.session_state.activities.append(activity_entry)
            self.save_data()
            st.success("Activity logged successfully!")

        # Display recent activities
        if st.session_state.activities:
            st.subheader("Recent Activities")
            activities_df = pd.DataFrame(st.session_state.activities)
            activities_df['date'] = pd.to_datetime(activities_df['date'])
            activities_df = activities_df.sort_values('date', ascending=False)
            st.dataframe(activities_df)

    def track_sleep(self):
        """Sleep tracking interface"""
        st.subheader("Track Your Sleep")
        
        col1, col2 = st.columns(2)
        
        with col1:
            sleep_hours = st.number_input("Hours of sleep", 
                                        min_value=0.0, 
                                        max_value=24.0, 
                                        value=7.0, 
                                        step=0.5)
            
        with col2:
            sleep_quality = st.select_slider(
                "Sleep Quality",
                options=["Poor", "Fair", "Good", "Excellent"]
            )
            
        if st.button("Log Sleep"):
            sleep_entry = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "hours": sleep_hours,
                "quality": sleep_quality
            }
            st.session_state.sleep_data.append(sleep_entry)
            self.save_data()
            st.success("Sleep data logged successfully!")

    def plot_mood_trend(self):
        """Plot mood trend visualization"""
        if st.session_state.mood_data:
            df = pd.DataFrame(st.session_state.mood_data)
            df['date'] = pd.to_datetime(df['date'])
            
            fig = px.line(df, x='date', y='mood_value', 
                         title='Mood Trend Over Time',
                         labels={'mood_value': 'Mood Level', 'date': 'Date'})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No mood data available yet. Start tracking your mood to see trends!")

    def plot_sleep_pattern(self):
        """Plot sleep pattern visualization"""
        if st.session_state.sleep_data:
            df = pd.DataFrame(st.session_state.sleep_data)
            df['date'] = pd.to_datetime(df['date'])
            
            fig = px.bar(df, x='date', y='hours',
                        title='Sleep Pattern',
                        labels={'hours': 'Hours of Sleep', 'date': 'Date'})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No sleep data available yet. Start tracking your sleep to see patterns!")

    def show_dashboard(self):
        """Display dashboard with overview of all metrics"""
        st.subheader("Your Wellness Dashboard")
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.session_state.mood_data:
                recent_mood = pd.DataFrame(st.session_state.mood_data[-7:])
                avg_mood = recent_mood['mood_value'].mean()
                st.metric("Average Mood (Last 7 days)", f"{avg_mood:.1f}/5")
            else:
                st.metric("Average Mood", "No data")
        
        with col2:
            if st.session_state.sleep_data:
                recent_sleep = pd.DataFrame(st.session_state.sleep_data[-7:])
                avg_sleep = recent_sleep['hours'].mean()
                st.metric("Average Sleep (Last 7 days)", f"{avg_sleep:.1f} hrs")
            else:
                st.metric("Average Sleep", "No data")
        
        with col3:
            if st.session_state.activities:
                activity_count = len(st.session_state.activities)
                st.metric("Activities Logged", activity_count)
            else:
                st.metric("Activities Logged", 0)
        
        # Visualizations
        self.plot_mood_trend()
        self.plot_sleep_pattern()

    def show_analysis(self):
        """Show analysis and insights"""
        st.subheader("Analysis & Insights")
        
        if st.session_state.mood_data:
            recent_moods = pd.DataFrame(st.session_state.mood_data[-7:])
            avg_mood = recent_moods['mood_value'].mean()
            
            st.metric("Average Mood (Last 7 Days)", f"{avg_mood:.2f}/5.0")
            
            # Generate insights
            insights = self.generate_insights()
            
            st.subheader("Personalized Suggestions")
            for insight in insights:
                st.info(insight)
        else:
            st.warning("Not enough data for analysis. Please log more entries.")

    def generate_insights(self):
        """Generate personalized insights based on user data"""
        insights = []
        
        # Analyze mood trends
        if st.session_state.mood_data:
            recent_moods = pd.DataFrame(st.session_state.mood_data[-7:])
            avg_mood = recent_moods['mood_value'].mean()
            
            if avg_mood < 3:
                insights.append("Your mood has been lower than usual. Consider scheduling a consultation with a mental health professional.")
            
        # Analyze sleep patterns
        if st.session_state.sleep_data:
            recent_sleep = pd.DataFrame(st.session_state.sleep_data[-7:])
            avg_sleep = recent_sleep['hours'].mean()
            
            if avg_sleep < 7:
                insights.append("You're getting less than the recommended 7 hours of sleep. Try to establish a regular sleep schedule.")
                
        # Analyze activities
        if st.session_state.activities:
            activities_df = pd.DataFrame(st.session_state.activities)
            if len(activities_df) < 3:
                insights.append("Try to engage in more activities. Regular exercise and meditation can help improve mental well-being.")
                
        return insights

def main():
    app = MentalHealthApp()
    app.load_data()
    app.main_page()

if __name__ == "__main__":
    main()
