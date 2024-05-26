import subprocess
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

map = {
     0:'un',
     1:'deux',
     2:'trois',
     3:'quatre'
}

def load_lstm(path):
    num_layers = 4
    hidden_size = 50

    # Input_size = n filter
    input_size = 40

    # Séquence length = padding = 2021  ou 2296
    sequence_length = 2021
    num_classes = 4
    dropout = 0.2
    lstm = LSTM(input_size, hidden_size, num_layers, num_classes, sequence_length, dropout)
    lstm.load_state_dict(torch.load(path))
    return lstm

def prepare_spectrogram(wave):
    # Transform wave -> spectrogram
    # wave = torch.tensor(wave)
    transform = MelSpectrogram(sample_rate=48000, n_mels=40, n_fft=512, hop_length=256)
    spectrogram = transform(wave)
    print(spectrogram.shape)
    spectrogram = spectrogram.squeeze()
    print(spectrogram.shape)

    # Normalize
    s_max = spectrogram.max()
    s_min = spectrogram.min()
    spectrogram = (spectrogram - spectrogram.mean()) / spectrogram.std()
    # spectrogram = (spectrogram - s_min) / (s_max - s_min)

    #Padding
    spectrogram = F.pad(spectrogram, (0, 2021-spectrogram.shape[1]))
    spectrogram = spectrogram.transpose(0, 1)
    return spectrogram

# Exemple de fonction pour convertir WebM en WAV en mémoire
def convert_webm_to_wav_memory(input_io, output_io):
    # Utilisez une bibliothèque ou une méthode appropriée pour convertir l'audio
    # Cela pourrait être une utilisation d'une commande ffmpeg exécutée en mémoire, par exemple:
    command = ['ffmpeg', '-i', 'pipe:0', '-acodec', 'pcm_s16le', '-ar', '48000', '-ac', '1', '-f', 'wav', 'pipe:1']
    process = subprocess.run(command, input=input_io.read(), stdout=subprocess.PIPE,  stderr=subprocess.DEVNULL)
    output_io.write(process.stdout)
    output_io.seek(0) 
    return output_io


