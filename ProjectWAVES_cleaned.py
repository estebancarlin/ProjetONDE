import numpy as np
import matplotlib.pyplot as plt
import os
import time
from random import uniform, random

# Constants representing skin states
INTACT_SKIN = -1
WOUNDED_SKIN = 0
HEALING_SKIN = 1
HEALED_SKIN = 2

###########################################
# INITIALIZATION FUNCTIONS
###########################################

def create_pristine_skin(n):
    """Creates an intact skin matrix."""
    return np.full((n + 2, n + 2), INTACT_SKIN, dtype=int)

def create_wound(n):
    """Creates a square wound in the center of the skin."""
    M = create_pristine_skin(n)
    n = len(M)
    for i in range(int(n/4), int((3*n)/4)):
        for j in range(int(n/4), int((3*n)/4)):
            M[i, j] = WOUNDED_SKIN

    # Add randomness for realism (layers near wound borders)
    for i in range(int(n/4), int((3*n)/4)):
        for offset, threshold in zip([0, 1, 2], [0.25, 0.5, 0.75]):
            if uniform(0, 1) >= threshold:
                M[i, int(n/4)+offset] = INTACT_SKIN
            if uniform(0, 1) >= threshold:
                M[i, int((3*n)/4)-1-offset] = INTACT_SKIN

    for j in range(int(n/4), int((3*n)/4)):
        for offset, threshold in zip([0, 1, 2], [0.25, 0.5, 0.75]):
            if uniform(0, 1) >= threshold:
                M[int(n/4)+offset, j] = INTACT_SKIN
            if uniform(0, 1) >= threshold:
                M[int((3*n)/4)-1-offset, j] = INTACT_SKIN

    return M

def seed_healing_phase(n):
    """Creates an initial healing phase in wounded skin."""
    M = create_wound(n)
    n = len(M)
    healing = []
    healed = []

    for i in range(int(n/4), int((3*n)/4)):
        for j in range(int(n/4), int((3*n)/4)):
            if M[i, j] == WOUNDED_SKIN:
                neighbors = [M[i-1,j], M[i+1,j], M[i,j-1], M[i,j+1],
                             M[i-2,j], M[i+2,j], M[i,j-2], M[i,j+2]]
                if any(nb == INTACT_SKIN for nb in neighbors):
                    if uniform(0, 1) >= 0.33:
                        M[i, j] = HEALING_SKIN
                        healing.append([i, j])
    return M, healing, healed

def get_neighbors(coord):
    x, y = coord
    return [[x-1,y-1], [x-1,y], [x-1,y+1], [x,y-1], [x,y+1], [x+1,y-1], [x+1,y], [x+1,y+1]]

###########################################
# HEALING SIMULATION
###########################################

def healing_step(M, healing, healed):
    p1, p2 = 0.33, 0.33  # Probabilities
    new_healing, new_healed, new_intact = [], [], []

    for cell in healing:
        if random() < p2:
            M[cell[0], cell[1]] = HEALED_SKIN
            new_healed.append(cell)

        for neighbor in get_neighbors(cell):
            i, j = neighbor
            if M[i, j] == WOUNDED_SKIN and random() < p1:
                M[i, j] = HEALING_SKIN
                new_healing.append([i, j])

    # Laser effect: healed skin regenerates to intact
    for cell in healed:
        if random() < p2:
            M[cell[0], cell[1]] = INTACT_SKIN
            new_intact.append(cell)

        for neighbor in get_neighbors(cell):
            i, j = neighbor
            if M[i, j] == HEALED_SKIN and random() < p1:
                M[i, j] = INTACT_SKIN
                new_intact.append([i, j])

    for cell in new_healed:
        healing.remove(cell)

    healing.extend(new_healing)
    healed.extend(new_healed)

    return M, healing, healed

def simulate(n, steps):
    M, healing, healed = seed_healing_phase(n)
    for _ in range(steps):
        M, healing, healed = healing_step(M, healing, healed)

    cmap = plt.cm.get_cmap('autumn', 4)
    plt.imshow(M, cmap=cmap)
    plt.axis('off')
    plt.show()
    return M, healing, healed

###########################################
# IMAGE EXPORTING (OPTIONAL)
###########################################

def save_simulation_images(step_interval, skin_size, total_steps):
    start_time = time.process_time()
    snapshots = total_steps // step_interval
    print(f"Step interval: {step_interval}\nSkin size: {skin_size}\nTotal steps: {total_steps}")

    M, healing, healed = seed_healing_phase(skin_size)
    output_dir = os.path.abspath("./SimulationImages")
    os.makedirs(output_dir, exist_ok=True)

    for idx in range(snapshots):
        for _ in range(step_interval):
            M, healing, healed = healing_step(M, healing, healed)

        cmap = plt.cm.get_cmap('autumn', 4)
        plt.imshow(M, cmap=cmap)
        plt.axis('off')
        step_title = f"Step {idx * step_interval + 1}"
        plt.title(step_title)
        plt.savefig(os.path.join(output_dir, f"{step_title}.png"))
        plt.close()

    duration = time.process_time() - start_time
    print(f"Images saved. Duration: {duration:.2f}s")

# Example usage
save_simulation_images(1, 80, 50)