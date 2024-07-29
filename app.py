import streamlit as st
import numpy as np
import random
import math

# Game setup
width, height = 800, 600
player_x, player_y = width // 2, height // 2
player_length = 10
food_positions = [(random.randint(0, width), random.randint(0, height)) for _ in range(50)]

# Streamlit setup
st.set_page_config(page_title="Slither.io-like Game", layout="wide")
st.title("Slither.io-like Game")

# Game state
if 'player_segments' not in st.session_state:
    st.session_state.player_segments = [(player_x, player_y)]
if 'score' not in st.session_state:
    st.session_state.score = 0

# Game loop
def update_game():
    # Move player
    mouse_x, mouse_y = st.session_state.mouse_pos
    head_x, head_y = st.session_state.player_segments[0]
    dx, dy = mouse_x - head_x, mouse_y - head_y
    angle = math.atan2(dy, dx)
    new_x = head_x + math.cos(angle) * 5
    new_y = head_y + math.sin(angle) * 5
    st.session_state.player_segments.insert(0, (new_x, new_y))
    if len(st.session_state.player_segments) > st.session_state.score + 10:
        st.session_state.player_segments.pop()

    # Check for food collision
    for food in food_positions[:]:
        if math.hypot(new_x - food[0], new_y - food[1]) < 15:
            food_positions.remove(food)
            food_positions.append((random.randint(0, width), random.randint(0, height)))
            st.session_state.score += 1

# Render game
canvas = st.empty()

# Mouse position update
mouse_pos = st.empty()

def main():
    while True:
        # Get mouse position
        st.session_state.mouse_pos = st.session_state.get('mouse_pos', (width // 2, height // 2))
        
        # Update game state
        update_game()
        
        # Draw game
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)
        ax.set_xlim(0, width)
        ax.set_ylim(0, height)
        ax.axis('off')
        
        # Draw food
        for food in food_positions:
            ax.add_patch(plt.Circle(food, 5, color='green'))
        
        # Draw player
        for segment in st.session_state.player_segments:
            ax.add_patch(plt.Circle(segment, 10, color='red'))
        
        canvas.pyplot(fig)
        plt.close(fig)
        
        # Display score
        st.sidebar.write(f"Score: {st.session_state.score}")
        
        # Update mouse position
        mouse_pos.write("Move your mouse over this area to control the snake")
        
        # Delay to control game speed
        time.sleep(0.05)

if __name__ == "__main__":
    main()