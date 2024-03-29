import torch.nn as nn
import torch.nn.functional as F

class EncoderNvidia(nn.Module):
    def __init__(self, num_classes=1):
        super().__init__()

        self.num_classes = num_classes

        # Module is expecting some encoder layers to be passed to it
        self.conv1 = nn.Conv2d(3, 24, 5, 2)
        self.conv2 = nn.Conv2d(24, 36, 5, 2)
        self.conv3 = nn.Conv2d(36, 48, 5, 2)

        if self.num_classes == 1:
            self.conv4 = nn.Conv2d(48, 64, 3)
            self.conv5 = nn.Conv2d(64, 64, 3)
            
            self.fc1 = nn.Linear(64 * 1 * 18, 100) # When images are 66 x 200
            # self.fc1 = nn.Linear(64 * 1 * 1, 100) # When images are 64 x 64
            # self.fc1 = nn.Linear(64 * 9 * 9, 100) # When images are 128 x 128
            self.fc2 = nn.Linear(100, 50)

        elif self.num_classes == 10:
            self.conv4 = nn.Conv2d(48, 64, 1)
            self.conv5 = nn.Conv2d(64, 64, 1)
            
            self.fc1 = nn.Linear(64 * 1 * 1, 100) # When images are 66 x 200
            self.fc2 = nn.Linear(100, 50)
        

    def forward(self, x):

        x = F.elu(self.conv1(x))
        x = F.elu(self.conv2(x))
        x = F.elu(self.conv3(x))
        x = F.elu(self.conv4(x))
        x = F.elu(self.conv5(x))

        if self.num_classes == 1:
            x = x.reshape(-1, 64 * 1 * 18)
        elif self.num_classes == 10:
            x = x.reshape(-1, 64 * 1 * 1)
        
        x = F.elu(self.fc1(x))
        x = F.elu(self.fc2(x))
        
        return x

class RegressorNvidia(nn.Module):
    def __init__(self, num_classes=1):
        super().__init__()
        
        self.fc3 = nn.Linear(50, 10)
        self.fc4 = nn.Linear(10, num_classes)

    def forward(self, x):
        
        x = F.elu(self.fc3(x))
        sa = self.fc4(x)

        return sa

class DecoderNvidia(nn.Module):
    def __init__(self, in_dim=50, out_dim=64*5*13, num_classes=1):
        super().__init__()

        self.relu = nn.ReLU()
        self.sigmoid = nn.Sigmoid()
        self.num_classes = num_classes

        if self.num_classes == 1:
            out_dim = 64*5*13
            self.decFC1 = nn.Linear(in_dim, out_dim)
            self.decConv2 = nn.ConvTranspose2d(64, 32, 3, stride=2, padding=1)
            self.decConv3 = nn.ConvTranspose2d(32, 16, 3, stride=2, padding=1)
            self.decConv4 = nn.ConvTranspose2d(16, 8, 3, stride=2, padding=(1,0))
            self.decConv5 = nn.ConvTranspose2d(8, 3, 3, stride=2, padding=(1,0), output_padding=1)
        
        elif self.num_classes == 10:
            out_dim = 8*4*4
            self.decFC1 = nn.Linear(in_dim, out_dim)
            self.decConv2 = nn.ConvTranspose2d(8, 4, 2, stride=2)
            self.decConv3 = nn.ConvTranspose2d(4, 3, 2, stride=2)
            self.decConv4 = nn.ConvTranspose2d(3, 3, 2, stride=2)
    
    def forward(self, x):

        if self.num_classes == 1:
            x = self.relu(self.decFC1(x))
            
            x = x.view(-1, 64, 5, 13)

            x = self.relu((self.decConv2(x)))
            x = self.relu((self.decConv3(x)))
            x = self.relu((self.decConv4(x)))     
            x = self.sigmoid((self.decConv5(x)))

        elif self.num_classes == 10:
            x = self.relu(self.decFC1(x))
            
            x = x.view(-1, 8, 4, 4)

            x = self.relu((self.decConv2(x)))
            x = self.relu((self.decConv3(x)))
            x = self.sigmoid((self.decConv4(x)))     

        return x
