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
import soundfile as sf
import io
from tqdm import tqdm

class LSTM(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, num_classes, sequence_length, dropout):
        super(LSTM, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.num_classes = num_classes
        self.sequence_length = sequence_length
        self.dropout = dropout
        
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True, dropout=dropout)
        self.fc = nn.Linear(hidden_size*sequence_length, num_classes)
        
    def forward(self, x):
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
        
        out, (_,_) = self.lstm(x, (h0, c0))
        # out = self.fc(out[:, -1, :])
        out = out.reshape(out.shape[0], -1)
        out = self.fc(out)
        return out
    
device = torch.device("cpu")

def prepare_spectrogram(wave):
    # Transform wave -> spectrogram
    transform = MelSpectrogram(sample_rate=48000, n_mels=40, n_fft=512, hop_length=256)
    spectrogram = transform(wave)
    print(spectrogram.shape)
    spectrogram = spectrogram.squeeze()
    print(spectrogram.shape)

    # Normalize
    mean = spectrogram.mean()
    std = spectrogram.std()
    spectrogram = (spectrogram - mean) / std

    #Padding
    spectrogram = F.pad(spectrogram, (0, 2021-spectrogram.shape[1]))
    spectrogram = spectrogram.transpose(0, 1)
    return spectrogram

def predict(spectrogram):
    lstm = torch.load('new-lstm-15epch-15clas-88acc.pth')
    lstm.to(device)    
    lstm.eval()
    return lstm(spectrogram)

def predict_from_wave(wave):
    wave_tensor = torch.tensor(wave)
    if wave_tensor.ndim > 1:
        wave_tensor = wave_tensor.mean(axis=1)
    spectrogram = prepare_spectrogram(wave_tensor)
    return predict(spectrogram)