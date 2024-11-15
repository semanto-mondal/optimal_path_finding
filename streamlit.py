import streamlit as st
import time
from collections import deque
import plotly.graph_objects as go

#default positions for the knight movement (2.5)
KNIGHT_MOVES = [
    (2, 1), (2, -1), (-2, 1), (-2, -1),
    (1, 2), (1, -2), (-1, 2), (-1, -2)
]

def is_valid_position(x, y, board_size):
    """Check if the position is valid on the chessboard of given size."""
    return 0 <= x < board_size[0] and 0 <= y < board_size[1]

def bfs_knight_shortest_paths(start, end, board_size):
    """Find the shortest path using BFS."""
    if start == end:
        return [[start]]  # If start and end are the same, return initial path
    
    # Initialize the BFS queue and visited set
    queue = deque([(start, [start])])  # (current position, path to this position)
    visited = set()
    visited.add(start)
    
    while queue:
        position, path = queue.popleft()

        if position == end:
            return [path]
        
        for dx, dy in KNIGHT_MOVES:
            new_pos = (position[0] + dx, position[1] + dy)
            if is_valid_position(new_pos[0], new_pos[1], board_size) and new_pos not in visited:
                visited.add(new_pos)
                queue.append((new_pos, path + [new_pos]))
    
    return []  # No path found

def bidirectional_bfs(start, end, board_size):
    """Find the shortest path using Bidirectional BFS."""
    if start == end:
        return [[start]]  # If start and end are the same, return trivial path
    
    # Initialize the BFS queues and visited sets
    queue_start = deque([(start, [start])])
    queue_end = deque([(end, [end])])
    visited_start = {start}
    visited_end = {end}
    
    # Store the paths from start and end
    paths_from_start = {}
    paths_from_end = {}

    while queue_start and queue_end:
        # Forward direction BFS
        if queue_start:
            current_start, path_start = queue_start.popleft()
            for dx, dy in KNIGHT_MOVES:
                new_pos = (current_start[0] + dx, current_start[1] + dy)
                if is_valid_position(new_pos[0], new_pos[1], board_size) and new_pos not in visited_start:
                    visited_start.add(new_pos)
                    queue_start.append((new_pos, path_start + [new_pos]))
                    paths_from_start[new_pos] = path_start + [new_pos]
                    # If we meet at a node, combine the paths
                    if new_pos in visited_end:
                        return [path_start + [new_pos] + paths_from_end[new_pos][::-1][1:]]

        # Backward direction BFS
        if queue_end:
            current_end, path_end = queue_end.popleft()
            for dx, dy in KNIGHT_MOVES:
                new_pos = (current_end[0] + dx, current_end[1] + dy)
                if is_valid_position(new_pos[0], new_pos[1], board_size) and new_pos not in visited_end:
                    visited_end.add(new_pos)
                    queue_end.append((new_pos, path_end + [new_pos]))
                    paths_from_end[new_pos] = path_end + [new_pos]
                    # If we meet at a node, combine the paths
                    if new_pos in visited_start:
                        return [paths_from_start[new_pos] + [new_pos] + path_end[::-1][1:]]
    
    return []  # if there are not meeting from forward and backward path then return an empty list

# Streamlit UI
st.title("Knight's Shortest Path Finder")

# User Inputs
board_size = st.selectbox("Select the board size", [(8, 8), (5, 5), (6, 6),(16,16),(20,20),(60,60),(80,80)], index=4)
start_input = st.text_input("Enter the starting position (e.g., 0,0, 1,1, etc.)", "0,0")
end_input = st.text_input("Enter the ending position (e.g., 7,7, 4,4, etc.)", "7,7")

# Convert the input string to a tuple of integers (row, col)
def parse_position(pos):
    return tuple(map(int, pos.split(',')))

start_pos = parse_position(start_input)
end_pos = parse_position(end_input)

# Calculate paths and times on button click
if st.button("Find Paths"):
    # Record the start time for BFS
    start_time = time.time()
    bfs_paths = bfs_knight_shortest_paths(start_pos, end_pos, board_size)
    bfs_time = (time.time() - start_time)  # seconds
    
    # Record the start time for Bidirectional BFS
    start_time = time.time()
    bidi_paths = bidirectional_bfs(start_pos, end_pos, board_size)
    bidi_time = (time.time() - start_time) # seconds
    
    # Display the paths and computation times
    st.subheader("BFS Shortest Path")
    if bfs_paths:
        for path in bfs_paths:
            st.write(path)
    else:
        st.write("No path found.")

    st.subheader("Bidirectional BFS Shortest Path")
    if bidi_paths:
        for path in bidi_paths:
            st.write(path)
    else:
        st.write("No path found.")
    
    # Bar plot comparison of computation times using Plotly
    st.subheader("Computation Time Comparison (in seconds)")
    
    # Add a small constant to ensure the bars are visible even for very small times
    bfs_time = max(bfs_time, 0.0001)  # Add a small constant
    bidi_time = max(bidi_time, 0.0001)  # Add a small constant
    
    # Create a bar plot using Plotly
    fig = go.Figure(data=[
        go.Bar(
            x=["BFS", "Bidirectional BFS"],
            y=[bfs_time, bidi_time],
            marker=dict(color=["blue", "orange"])
        )
    ])
    
    # Update layout for better visualization
    fig.update_layout(
        title="Computation Time Comparison (Hover on the bar to know to unit)",
        xaxis_title="Algorithm",
        yaxis_title="Time",
        
    )
    
    
    # Display the Plotly figure
    st.plotly_chart(fig)
