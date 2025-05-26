import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# Greedy activity selection algorithm
def activity_selection(start, end):
    activities = sorted(zip(start, end), key=lambda x: x[1])
    selected = []
    last_end_time = 0
    for s, e in activities:
        if s >= last_end_time:
            selected.append((s, e))
            last_end_time = e
    return selected

# Plotting function
def plot_activities(start, end, selected):
    fig, ax = plt.subplots(figsize=(10, len(start) * 0.6))
    y_labels = []
    selected_set = set(selected)

    for i, (s, e) in enumerate(zip(start, end)):
        label = f"A{i+1}"
        y_labels.append(label)
        color = 'green' if (s, e) in selected_set else 'red'
        ax.broken_barh([(s, e - s)], (i - 0.4, 0.8), facecolors=color)
        ax.text(s + (e - s)/2, i, label, ha='center', va='center', color='white', weight='bold')

    ax.set_yticks(range(len(start)))
    ax.set_yticklabels(y_labels)
    ax.set_xlabel('Time')
    ax.set_title('Activity Selection Timeline')
    ax.set_xlim(0, max(end) + 2)

    ax.grid(True, axis='x', linestyle='--', alpha=0.6)
    legend_elements = [
        mpatches.Patch(color='green', label='Selected'),
        mpatches.Patch(color='red', label='Not Selected')
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    st.pyplot(fig)

# Streamlit UI
st.set_page_config(page_title="Activity Selection (Greedy)", layout="centered")
st.title("Activity Selection using Greedy Algorithm")
st.markdown("This app finds the **maximum number of non-overlapping activities** using a greedy approach and visualizes them on a timeline.")

with st.form("activity_input_form"):
    col1, col2 = st.columns(2)
    with col1:
        start_input = st.text_input("Start Times (comma-separated)", "1,3,0,5,8,5")
    with col2:
        end_input = st.text_input("End Times (comma-separated)", "2,4,6,7,9,9")
    
    submitted = st.form_submit_button("Run Algorithm & Show Graph")

if submitted:
    try:
        start_times = list(map(int, start_input.strip().split(',')))
        end_times = list(map(int, end_input.strip().split(',')))

        if len(start_times) != len(end_times):
            st.error("Start and End time lists must be the same length.")
        else:
            selected = activity_selection(start_times, end_times)
            st.success(f"Selected {len(selected)} activities:")
            st.write(selected)
            plot_activities(start_times, end_times, selected)

    except ValueError:
        st.error("Please enter only integers, separated by commas.")
