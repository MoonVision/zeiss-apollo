import torch
import torch.nn as nn

class SlimWide(nn.Module):

    def __init__(self, in_channels=1, channels=64):
        super().__init__()

        self.convnet1 = nn.Sequential(
                nn.Conv2d(in_channels, channels, kernel_size=7, padding=1,
                          stride=1),
                # nn.BatchNorm2d(channels),
                nn.ReLU(True))

        self.convnet2 = nn.Sequential(
                nn.Conv2d(channels, channels, kernel_size=7, padding=1,
                          stride=1),
                # nn.BatchNorm2d(channels),
                nn.ReLU(True))

        self.convnet3 = nn.Sequential(
                nn.Conv2d(channels, channels, kernel_size=7, padding=1,
                          stride=1),
                nn.BatchNorm2d(channels),
                nn.AvgPool2d(kernel_size=2, stride=2), nn.ReLU(True))
        self.convnet4 = nn.Sequential(
                nn.Conv2d(channels, channels, kernel_size=7, padding=1,
                          stride=1),
                nn.BatchNorm2d(channels),
                nn.AvgPool2d(kernel_size=2, stride=2), nn.ReLU(True))

        self.convnet4 = nn.Conv2d(channels, 1, kernel_size=1, padding=0,
                                  stride=1)
        #self.scalar = nn.Parameter(data=torch.tensor([1.0]))
        #self.bias = nn.Parameter(data=torch.tensor([0.0]))

    def forward(self, x):
        y = self.convnet1(x)
        y = self.convnet2(y)
        y = self.convnet3(y)
        y = self.convnet4(y)

        return y #self.scalar * y - self.bias


def torchvision_default_initialize_layer(m):
    # Recent init from torch repo.
    if isinstance(m, nn.Conv2d):
        if m.bias is not None:
            m.bias.data.zero_()
        nn.init.kaiming_normal_(m.weight)
    elif isinstance(m, nn.BatchNorm2d):
        nn.init.constant_(m.weight, 1)
        nn.init.constant_(m.bias, 0)
    elif isinstance(m, nn.Linear):
        nn.init.constant_(m.bias, 0)
        nn.init.normal_(m.weight, 0.01)


def torchvision_default_initialize_weights(module):
    for m in module.modules():
        torchvision_default_initialize_layer(m)
