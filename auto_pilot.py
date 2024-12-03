
import numpy as np
import random
import torch
import torch.nn as nn
import torch.nn.functional as F


models = ["random", "random_NN", "trained_NN"]
selected_model = models[0]

#-------------------------------
# Define the Neural Network
class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(3 * 3, 16)  # Hidden layer with 16 neurons
        self.fc2 = nn.Linear(16, 4)     # Output layer with 4 neurons (classes)

    def forward(self, x):
        x = x.view(-1, 3 * 3)  # Flatten the 3x3 input to a 9-dimensional vector
        x = F.relu(self.fc1(x))  # Apply ReLU activation on the hidden layer
        x = self.fc2(x)          # Output layer
        return F.softmax(x, dim=1)  # Apply softmax activation
    
model_save_path = "C:/Users/leopo/Documents/GitHub/wumpus_world/models/simple_nn_model.pth"


if selected_model == "random_NN":
    # Create the model
    model_test = SimpleNN()
elif selected_model == "trained_NN":
    # Create the model
    model_test = SimpleNN()
    # Load the saved state dictionary
    model_test.load_state_dict(torch.load(model_save_path))

def get_direction_from_auto_pilot(world, mask, agent, breeze, feet):
    possible_directions = ["up","down", "left", "right"]

    if selected_model == "random":
        direction = random.choice(possible_directions)  # Randomly choose a direction
    elif selected_model == "random_NN" or selected_model == "trained_NN":
        my_world = 4*agent + 1*breeze + 2*feet
        masked_world = np.where(mask == 1, -1, my_world)
        row, col = np.argwhere(agent == 1)[0]
        padded_masked_world = np.pad(masked_world, pad_width=1, mode='constant', constant_values=-2)
        submatrix = padded_masked_world[row:row+3, col:col+3]
        normalized_sub_matrix = (submatrix + 2) / 9 # now all values are between 0 and 1.

        # Convert to PyTorch tensor
        input_tensor = torch.tensor(normalized_sub_matrix, dtype=torch.float32)

        # Add a batch dimension (shape: [1, 3, 3])
        input_tensor = input_tensor.unsqueeze(0)
        # Set the model to evaluation mode
        model_test.eval()
        # Perform inference
        with torch.no_grad():  # Disable gradient computation for inference
            output = model_test(input_tensor)
        # Get the predicted class (index of the maximum probability)
        predicted_class = torch.argmax(output, dim=1).item()
        direction = possible_directions[predicted_class]
    else:
        direction = random.choice(possible_directions)  # Randomly choose a direction
    return direction