import numpy as np
import torch
from torchvision import datasets, transforms
from torch.utils.data import Dataset
#from config.dataset import dataset_file_path

class MyDataset(Dataset):
    def __init__(self, train=True, transform=None):
        """
        Inizializza il dataset, caricando dati e target da un file txt.
        :param train: bool, True per i dati di addestramento, False per i dati di test.
        :param transform: eventuali trasformazioni da applicare ai dati.
        """

        # Name of the file
        file_name = 'EURUSD.txt'
        
        #file_path = dataset_file_path + '/' + file_name
        file_path = file_name

        # Creation of matricial dataset
        order = 3

        data_tot = torch.Tensor(np.loadtxt("EURUSD.txt"))
        matrix = np.zeros((len(data_tot)-order,order+1))
        length_test = int(len(data_tot)*.2)

        for i in range(order,(len(data_tot))):
            matrix[i-order,:] = (data_tot[(i-order):(i+1)])

        Y = torch.from_numpy(matrix[:,order]).float()
        #Y = Y.unsqueeze(1).float()
        X = torch.from_numpy(matrix[:len(Y),:order]).unsqueeze(1).float()

        if train:
            self.data = X[:-length_test]
            self.targets = Y[:-length_test]
        else:
            self.data = X[-length_test:]
            self.targets = Y[-length_test:]
        
        self.transform = transform

    def __len__(self):
        return len(self.targets)

    def __getitem__(self, idx):
        sample = self.data[idx]
        target = self.targets[idx]
        
        if self.transform:
            sample = self.transform(sample)
        
        return sample, target

def get_mydataset(train=True):
    """
    Restituisce un'istanza del dataset `MyDataset`.
    :param train: bool, True per i dati di addestramento, False per i dati di test.
    """
    transform = None # Nessuna trasformazione per il momento
    return MyDataset(train=train, transform=transform)
