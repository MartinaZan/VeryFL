import torch.nn as nn
class Martina_simpleMLP(nn.Module):
    def __init__(self, class_num):
        super(Martina_simpleMLP, self).__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(3, 5),
            nn.ReLU(),
            nn.Linear(5, class_num)
        )
        
    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

def get_simple_mlp(class_num): 
    return Martina_simpleMLP(class_num)
