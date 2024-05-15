import csv
import os
from pathlib import Path

import torch
from torch import Tensor
import torch.nn as nn
from torch import optim
import torch.nn.functional as F
from typing import Dict, List, Tuple, Union

from torch.utils.data import Dataset, DataLoader, TensorDataset
import torchvision.datasets as datasets
import torchvision.transforms as transforms

from torchaudio.transforms import MelSpectrogram
import torchaudio

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import torchaudio.transforms as T

from tqdm import tqdm


lstm = torch.load('./models/lstm98-77epch.pth')
transform = MelSpectrogram(sample_rate=48000, n_mels=40, n_fft=512, hop_length=256)


def prepare_spectrogram(wave):
    spectrogram = transform(wave)
    mean = spectrogram.mean()
    std = spectrogram.std()
    spectrogram = (spectrogram - mean) / std
    spectrogram = spectrogram.transpose(0, 1)
    F.pad(spectrogram, (0, 0, 0, 2021-spectrogram.shape[0]))
