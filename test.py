import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_dfd():
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Define box style
    box_props = dict(boxstyle="round,pad=0.5", fc="#ffffff", ec="#000000", lw=1.5)
    
    # Define positions
    positions = {
        "User": (0.1, 0.5),
        "Frontend": (0.35, 0.5),
        "Backend": (0.6, 0.5),
        "Model": (0.85, 0.5)
    }
    
    # Draw Boxes
    ax.text(positions["User"][0], positions["User"][1], "User", ha="center", va="center", size=12, bbox=box_props)
    ax.text(positions["Frontend"][0], positions["Frontend"][1], "Frontend UI\n(HTML/JS)", ha="center", va="center", size=12, bbox=box_props)
    ax.text(positions["Backend"][0], positions["Backend"][1], "Flask Server\n(app.py)", ha="center", va="center", size=12, bbox=box_props)
    ax.text(positions["Model"][0], positions["Model"][1], "ML Model\n(joblib/pkl)", ha="center", va="center", size=12, bbox=dict(boxstyle="round,pad=0.5", fc="#e6f3ff", ec="#000000", lw=1.5))

    # Draw Arrows (Flows)
    
    # 1. User -> Frontend
    ax.annotate("", xy=(0.28, 0.53), xytext=(0.15, 0.53), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.text(0.215, 0.55, "Inputs\nSymptoms", ha="center", va="bottom", fontsize=9)

    # 2. Frontend -> Backend
    ax.annotate("", xy=(0.53, 0.53), xytext=(0.42, 0.53), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.text(0.475, 0.55, "POST Request\n(JSON)", ha="center", va="bottom", fontsize=9)

    # 3. Backend -> Model
    ax.annotate("", xy=(0.78, 0.53), xytext=(0.67, 0.53), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.text(0.725, 0.55, "Input Vector", ha="center", va="bottom", fontsize=9)

    # 4. Model -> Backend (Return)
    ax.annotate("", xy=(0.67, 0.47), xytext=(0.78, 0.47), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.text(0.725, 0.43, "Prediction", ha="center", va="top", fontsize=9)

    # 5. Backend -> Frontend (Return)
    ax.annotate("", xy=(0.42, 0.47), xytext=(0.53, 0.47), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.text(0.475, 0.43, "JSON Response\n(Disease/Precautions)", ha="center", va="top", fontsize=9)

    # 6. Frontend -> User (Display)
    ax.annotate("", xy=(0.15, 0.47), xytext=(0.28, 0.47), arrowprops=dict(arrowstyle="->", lw=1.5))
    ax.text(0.215, 0.43, "Displays Result", ha="center", va="top", fontsize=9)

    # Clean up plot
    ax.set_xlim(0, 1)
    ax.set_ylim(0.3, 0.7)
    ax.axis('off')
    plt.title("Level-0 Data Flow Diagram (DFD) - MEDiWiSE", fontsize=14, fontweight='bold')
    
    # Save
    plt.savefig("mediwise_dfd.png", dpi=300, bbox_inches='tight')
    print("Diagram saved as mediwise_dfd.png")
    plt.show()

draw_dfd()