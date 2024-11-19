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
if 'is_mobile' not in st.session_state:
    st.session_state.is_mobile = False
if 'goals' not in st.session_state:
        st.session_state.goals = []
if 'journal_entries' not in st.session_state:
        st.session_state.journal_entries = []
if 'custom_tags' not in st.session_state:
        st.session_state.custom_tags = []
if 'meditation_active' not in st.session_state:
        st.session_state.meditation_active = False






class MentalHealthApp:
    def __init__(self):
        pass

    def save_data(self):
        """Save data to JSON file"""
        data = {
            'mood_data': st.session_state.mood_data,
            'activities': st.session_state.activities,
            'sleep_data': st.session_state.sleep_data,
            'goals': st.session_state.goals,
            'journal_entries': st.session_state.journal_entries,
            'custom_tags': st.session_state.custom_tags,
            'meditation_active': st.session_state.meditation_active

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
                st.session_state.goals = data.get('goals', [])
                st.session_state.journal_entries = data.get('journal_entries', [])
                st.session_state.custom_tags = data.get('custom_tags', [])
                st.session_state.meditation_active = data.get('meditation_active', False)
                st.session_state.is_mobile = data.get('is_mobile', False)
                
        except FileNotFoundError:
            pass
    def set_page_layout(self):
        """Set page layout"""
         # Detect device type based on viewport width
    is_mobile = st.session_state.get('is_mobile', False)
    st.set_page_config(
            page_title="Mental Health Tracker",
            page_icon="🧠",
            layout="wide",
            initial_sidebar_state="expanded"
        )
          # Add a toggle in sidebar
    with st.sidebar:
        is_mobile = st.toggle("Mobile Mode", value= is_mobile)
        st.session_state.is_mobile = is_mobile
    def main_page(self):
        """Main page layout"""
        st.title("**🧠 :rainbow[Mental Health Tracker]**")
        
        # Sidebar navigation
        if st.session_state.is_mobile:

    # Mobile navigation using selectbox at top
            page = st.selectbox("**:rainbow[Navigate]**", 
        ["Dashboard", "Track Mood", "Track Activities", "Track Sleep", 
             "Journal", "Meditation", "Goals", "Analytics & Insights", 
             "Export Data"])
        else:

    # Desktop navigation using sidebar
            page = st.sidebar.radio("**:rainbow[Navigate]**", 
         ["Dashboard", "Track Mood", "Track Activities", "Track Sleep", 
             "Journal", "Meditation", "Goals", "Analytics & Insights", 
             "Export Data"])
        if page == "Dashboard":
            self.show_dashboard()
        elif page == "Track Mood":
            self.track_mood()
        elif page == "Track Activities":
            self.track_activities()
        elif page == "Track Sleep":
            self.track_sleep()
        elif page == "Journal":
            self.add_journal_entry()
        elif page == "Meditation":
            self.meditation_timer()
        elif page == "Goals":
            self.add_wellness_goals()
        elif page == "Analysis & Insights":
            self.show_analysis()
        elif page == "Export Data":
            self.export_data()

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
                "hours": float(sleep_hours),
                "quality": sleep_quality
            }
            st.session_state.sleep_data.append(sleep_entry)
            self.save_data()
            st.success("Sleep data logged successfully!")
        #display recent sleep data 
        if st.session_state.sleep_data:
            st.subheader("Recent Sleep Data")
            sleep_df = pd.DataFrame(st.session_state.sleep_data)
            sleep_df['date'] = pd.to_datetime(sleep_df['date'])
            sleep_df = sleep_df.sort_values('date', ascending=False)
            st.dataframe(sleep_df)
    def plot_mood_trend(self):
        """Plot mood trend visualization"""
        if st.session_state.mood_data:
            df = pd.DataFrame(st.session_state.mood_data)
            df['date'] = pd.to_datetime(df['date'])
            
            height = 300 if st.session_state.is_mobile else 400
            fig = px.line(df, x='date', y='mood_value', 
                         title='Mood Trend Over Time',
                         labels={'mood_value': 'Mood Level', 'date': 'Date'},
                         height=height)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No mood data available yet. Start tracking your mood to see trends!")
    
    def plot_sleep_pattern(self):
        """Plot sleep pattern visualization"""
        if st.session_state.sleep_data:
            df = pd.DataFrame(st.session_state.sleep_data)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values('date')

            height = 300 if st.session_state.is_mobile else 400
            fig = px.bar(df, x='date', y='hours',
                        title='Sleep Pattern',
                        labels={'hours': 'Hours of Sleep', 'date': 'Date'},
                        height=height)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No sleep data available yet. Start tracking your sleep to see patterns!")
    
    def show_dashboard(self):
        """Display dashboard with overview of all metrics"""
        st.subheader("Your Wellness Dashboard")
        #create metrics 
        col1 , col2  ,col3 = st.columns(3)
        # Summary metrics
        with col1:
            # Mood metric
            if st.session_state.mood_data:
                mood_df = pd.DataFrame(st.session_state.mood_data)
                mood_df['date'] = pd.to_datetime(mood_df['date'])
                recent_mood = mood_df[mood_df['date'] > (datetime.now() - pd.Timedelta(days=7))]
                if not recent_mood.empty:
                    avg_mood = recent_mood['mood_value'].mean()
                    st.metric("Average Mood (Last 7 days)", f"{avg_mood:.1f}")
                else:
                    st.metric("Average Mood", "No recent data")
            else:
                st.metric("Average Mood", "No data")
    
        with col2:
        # Sleep metric
            if st.session_state.sleep_data:
                sleep_df = pd.DataFrame(st.session_state.sleep_data)
                sleep_df['date'] = pd.to_datetime(sleep_df['date'])
                recent_sleep = sleep_df[sleep_df['date'] > (datetime.now() - pd.Timedelta(days=7))]
                if not recent_sleep.empty:
                    avg_sleep = recent_sleep['hours'].mean()
                    st.metric("Average Sleep (Last 7 days)", f"{avg_sleep:.1f} hrs")
                else:
                    st.metric("Average Sleep", "No recent data")
            else:
                st.metric("Average Sleep", "No data")
    
        with col3:
            # Activity metric
            if st.session_state.activities:
                activities_df = pd.DataFrame(st.session_state.activities)
                activities_df['date'] = pd.to_datetime(activities_df['date'])
                recent_activities = activities_df[activities_df['date'] > (datetime.now() - pd.Timedelta(days=7))]
                activity_count = len(recent_activities)
                st.metric("Activities (Last 7 days)", activity_count)
            else:
                st.metric("Activities", "No data")
        # Show visualizations
    if st.session_state.mood_data:
        st.subheader("Mood Trend")
        mood_df = pd.DataFrame(st.session_state.mood_data)
        mood_df['date'] = pd.to_datetime(mood_df['date'])
        fig_mood = px.line(mood_df, x='date', y='mood_value',
                          title='Mood Trend',
                          labels={'mood_value': 'Mood Level', 'date': 'Date'})
        st.plotly_chart(fig_mood, use_container_width=True, key="dashboard_mood")

    if st.session_state.sleep_data:
        st.subheader("Sleep Pattern")
        sleep_df = pd.DataFrame(st.session_state.sleep_data)
        sleep_df['date'] = pd.to_datetime(sleep_df['date'])
        fig_sleep = px.bar(sleep_df, x='date', y='hours',
                          title='Sleep Pattern',
                          labels={'hours': 'Hours of Sleep', 'date': 'Date'})
        st.plotly_chart(fig_sleep, use_container_width=True, key="dashboard_sleep")

    # Show recent activities
    if st.session_state.activities:
        st.subheader("Recent Activities")
        activities_df = pd.DataFrame(st.session_state.activities)
        activities_df['date'] = pd.to_datetime(activities_df['date'])
        recent_activities = activities_df.sort_values('date', ascending=False).head(5)
        st.dataframe(recent_activities[['date', 'activity', 'duration']])
    # Show recent journal entries
    if st.session_state.journal_entries:
        st.subheader("Recent Journal Entries")
        journal_df = pd.DataFrame(st.session_state.journal_entries)
        journal_df['date'] = pd.to_datetime(journal_df['date'])
        recent_entries = journal_df.sort_values('date', ascending=False).head(5)
        st.dataframe(recent_entries[['date', 'title', 'content']])
    # show recent goals
    if st.session_state.goals:
        st.subheader("Recent Goals")
        goals_df = pd.DataFrame(st.session_state.wellness_goals)
        goals_df['date'] = pd.to_datetime(goals_df['date'])
        recent_goals = goals_df.sort_values('date', ascending=False).head(5)
        st.dataframe(recent_goals[['date', 'goal', 'status']])

        
        
        

    def show_analysis(self):
        """Show comprehensive analysis page"""
        st.subheader("Analysis & Insights")
        
        tab1, tab2, tab3 = st.tabs(["Mood Analysis", "Sleep Analysis", "Activity Impact"])
        
        with tab1:
            
            if st.session_state.mood_data:
                st.subheader("Mood Trend Analysis")
                mood_df = pd.DataFrame(st.session_state.mood_data)
                mood_df['date'] = pd.to_datetime(mood_df['date'])
                mood_df = mood_df.sort_values('date')
            
                fig1 = px.line(mood_df, x='date', y='mood_value',
                         title='Mood Trend Over Time',
                         labels={'mood_value': 'Mood Level', 'date': 'Date'})
                st.plotly_chart(fig1, use_container_width=True, key="mood_trend_analysis")
            
                # Show mood statistics
                st.subheader("Mood Statistics (Last 30 days)")
                recent_mood = mood_df[mood_df['date'] > (datetime.now() - pd.Timedelta(days=30))]
                if not recent_mood.empty:
                    col1, col2, col3 = st.columns(3)
                    col2.metric("Highest Mood", f"{recent_mood['mood_value'].max():.0f}")
                    col3.metric("Lowest Mood", f"{recent_mood['mood_value'].min():.0f}")
            else:
                st.info("Start tracking your mood to see analysis here!")
    
        with tab2:
            if st.session_state.sleep_data:
                st.subheader("Sleep Patterns")
                sleep_df = pd.DataFrame(st.session_state.sleep_data)
                sleep_df['date'] = pd.to_datetime(sleep_df['date'])
                sleep_df = sleep_df.sort_values('date')
                
                # Create sleep trend visualization
                fig2 = px.bar(sleep_df, x='date', y='hours',
                        title='Sleep Duration Over Time',
                        labels={'hours': 'Hours of Sleep', 'date': 'Date'})
                st.plotly_chart(fig2, use_container_width=True, key="sleep_trend_analysis")
                
                # Show sleep statistics
                st.subheader("Sleep Statistics (Last 30 days)")
                recent_sleep = sleep_df[sleep_df['date'] > (datetime.now() - pd.Timedelta(days=30))]
                if not recent_sleep.empty:
                    col1, col2, col3 = st.columns(3)
                    col3.metric("Least Sleep", f"{recent_sleep['hours'].min():.1f} hrs")
            else:
                st.info("Start tracking your sleep to see analysis here!")
    
        with tab3:
            if st.session_state.activities and st.session_state.mood_data:
                st.subheader("Activity Impact Analysis")
                
                # Create activity analysis
                activities_df = pd.DataFrame(st.session_state.activities)
                activities_df['date'] = pd.to_datetime(activities_df['date'])
                
                # Activity frequency chart
                activity_counts = activities_df['activity'].value_counts()
                fig3 = px.pie(values=activity_counts.values,
                        names=activity_counts.index,
                        title='Activity Distribution')
                st.plotly_chart(fig3, use_container_width=True, key="activity_distribution")
                
                # Activity duration analysis
                avg_duration = activities_df.groupby('activity')['duration'].mean().reset_index()
                fig4 = px.bar(avg_duration, x='activity', y='duration',
                        title='Average Duration by Activity',
                        labels={'duration': 'Minutes', 'activity': 'Activity'})
                st.plotly_chart(fig4, use_container_width=True, key="activity_duration")
            else:
                st.info("Start tracking both activities and mood to see their relationship!")
    def generate_insights(self):
        """Generate personalized insights based on user data"""
        insights = []
        
        if st.session_state.mood_data:
            df_mood = pd.DataFrame(st.session_state.mood_data)
            df_mood['date'] = pd.to_datetime(df_mood['date'])
            
            # Analyze mood trends
            avg_mood = df_mood['mood_value'].mean()
            if avg_mood < 3:
                insights.append("Your mood has been lower than average. Consider scheduling activities that bring you joy or speaking with a mental health professional.")
            elif avg_mood >= 4:
                insights.append("Great job! Your mood has been consistently positive.")
    
        if st.session_state.sleep_data:
            df_sleep = pd.DataFrame(st.session_state.sleep_data)
            avg_sleep = df_sleep['hours'].mean()
            
            if avg_sleep < 7:
                insights.append("You're getting less than the recommended 7-9 hours of sleep. Try to maintain a consistent sleep schedule.")
            elif avg_sleep > 9:
                insights.append("You're getting more than average sleep. If you feel tired despite this, consider checking your sleep quality.")
    
        if st.session_state.activities:
            df_activities = pd.DataFrame(st.session_state.activities)
            activity_counts = df_activities['activity'].value_counts()
            
            if len(activity_counts) < 3:
                insights.append("Consider diversifying your activities to maintain better mental health.")
            
            if 'Exercise' in activity_counts and activity_counts['Exercise'] > 3:
                insights.append("Great job maintaining regular exercise! This is excellent for mental health.")
    
        if not insights:
            insights.append("Start logging more data to receive personalized insights!")
            
        return insights
    
    #mood correlation analysis
    def analyze_mood_correlations(self):
        """Analyze correlations between activities and mood"""
        if st.session_state.mood_data and st.session_state.activities:
            mood_df = pd.DataFrame(st.session_state.mood_data)
            activities_df = pd.DataFrame(st.session_state.activities)
            
            # Convert dates and merge data
            mood_df['date'] = pd.to_datetime(mood_df['date']).dt.date
            activities_df['date'] = pd.to_datetime(activities_df['date']).dt.date
            
            # Group activities by date
            daily_activities = activities_df.groupby('date')['activity'].agg(list).reset_index()
            
            # Merge with mood data
            combined_df = pd.merge(mood_df, daily_activities, on='date', how='inner')
            return combined_df
    #goal setting and progress tracking
    def add_wellness_goals(self):
        """Add wellness goals tracking"""
        st.subheader("Set Wellness Goals")
        
        goal_types = ["Mood", "Sleep", "Exercise", "Meditation"]
        goal_type = st.selectbox("Goal Type", goal_types)
        
        goal_target = st.number_input("Target Value", min_value=0)
        goal_deadline = st.date_input("Target Date")
        
        if st.button("Set Goal"):
            goal = {
                "type": goal_type,
                "target": goal_target,
                "deadline": goal_deadline.strftime("%Y-%m-%d"),
                "created_date": datetime.now().strftime("%Y-%m-%d")
            }
            if 'goals' not in st.session_state:
                st.session_state.goals = []
            st.session_state.goals.append(goal)
            self.save_data()
    #Journaling Feature
    def add_journal_entry(self):
        """Add journaling capability"""
        st.subheader("Daily Journal")
        
        journal_date = st.date_input("Date")
        journal_title = st.text_input("Entry Title")
        journal_content = st.text_area("Write your thoughts...", height=200)
        
        if st.button("Save Journal Entry"):
            entry = {
                "date": journal_date.strftime("%Y-%m-%d"),
                "title": journal_title,
                "content": journal_content
            }
            if 'journal_entries' not in st.session_state:
                st.session_state.journal_entries = []
            st.session_state.journal_entries.append(entry)
            self.save_data()
    #advance analytics and reporting
    def generate_weekly_report(self):
        """Generate detailed weekly wellness report"""
        st.subheader("Weekly Wellness Report")
        
        if st.session_state.mood_data:
            df = pd.DataFrame(st.session_state.mood_data)
            df['date'] = pd.to_datetime(df['date'])
            
            # Weekly averages
            weekly_stats = df.set_index('date').resample('W').agg({
                'mood_value': 'mean'
            }).reset_index()
            
            # Create visualization
            fig = px.line(weekly_stats, x='date', y='mood_value',
                         title='Weekly Mood Trends',
                         labels={'mood_value': 'Average Mood', 'date': 'Week'})
            st.plotly_chart(fig)
    #meditation Timer
    def meditation_timer(self):
        """Add meditation timer feature"""
        st.subheader("Meditation Timer")
        time = st.slider("Session Duration (minutes)", 1, 60, 15)
        
        duration = st.slider("Duration (minutes)", 1, 60, 5)
        if 'meditation_active' not in st.session_state:
            st.session_state.meditation_active = False
        
        if st.button("Start Meditation"):
            st.session_state.meditation_active = True
            
        if st.session_state.meditation_active:
            progress_bar = st.progress(0)
            for i in range(duration * 60):
                time.sleep(1)
                progress_bar.progress((i + 1) / (duration * 60))
    #CUstomizable tags and categories
    def manage_custom_tags(self):
        """Manage custom tags for activities and moods"""
        st.subheader("Manage Custom Tags")
        
        if 'custom_tags' not in st.session_state:
            st.session_state.custom_tags = []
        
        new_tag = st.text_input("Add New Tag")
        if st.button("Add Tag") and new_tag:
            st.session_state.custom_tags.append(new_tag)
            self.save_data()
    
    # def add_custom_tags(self):
    #     """Add custom tags for categorization"""
    #     st.subheader("Add Custom Tags")

    #     tag_name = st.text_input("Tag Name")
    #     tag_description = st.text_area("Tag Description")

    #     if st.button("Add Tag"):
    #         tag = {
    #             "name": tag_name,
    #             "description": tag_description
    #         }
    #         if 'custom_tags' not in st.session_state:
    #             st.session_state.custom_tags = []
    #         st.session_state.custom_tags.append(tag)
    #         self.save_data()
    #explore data feature
    def export_data(self):
        """Export user data in various formats"""
        st.subheader("Export Your Data")
    # add a format selection for the export button
        export_format = st.selectbox("Select Export Format", ["CSV", "JSON", "EXCEL"])
        
        
        if st.button("Export Data"):
            data = {
                'mood_data': pd.DataFrame(st.session_state.mood_data),
                'activities': pd.DataFrame(st.session_state.activities),
                'sleep_data': pd.DataFrame(st.session_state.sleep_data)
            }
            VALID_FORMATS = {"CSV", "JSON", "EXCEL"}
            
            for name, df in data.items():
                # Convert to uppercase for case-insensitive comparison
                format_upper = export_format.upper()
                
                if format_upper not in VALID_FORMATS:
                    raise ValueError(f"Invalid export format: {export_format}. Must be one of {VALID_FORMATS}")
                    
                if format_upper == "CSV":
                    df.to_csv(f"{name}.csv", index=False)
                elif format_upper == "JSON":
                    df.to_json(f"{name}.json", orient="records")
                elif format_upper == "EXCEL":
                    df.to_excel(f"{name}.xlsx", index=False)
            
           
    
    
    

def main():
    app = MentalHealthApp()
    app.load_data()
    app.main_page()

if __name__ == "__main__":
    main()
