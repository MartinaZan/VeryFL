# Esempio di utilizzo:
#   from log.read_logs import read_logs
#   read_logs('log/2024_11_07_5.log')

#####################################################################################################################################################################
#####################################################################################################################################################################

import re
from datetime import datetime
import matplotlib.pyplot as plt

#####################################################################################################################################################################
#####################################################################################################################################################################

# Estrazione informazioni di base dai log
def extract_information_from_file(file_path):
    start_time = None
    end_time = None
    dataset = None
    num_clients = set()  # Usato per evitare duplicati
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Pattern per identificare il dataset
    dataset_pattern = r"dataset: (\S+),"
    
    # Pattern per identificare l'orario
    time_pattern = r"(\d+-\d+-\d+ \d+:\d+:\d+,\d+)"
    
    # Scorre tutte le righe per estrarre le informazioni
    for line in lines:
        # Trova il dataset
        dataset_match = re.search(dataset_pattern, line)
        if dataset_match:
            dataset = dataset_match.group(1)
        
        # Trova gli orari (prima e ultima occorrenza)
        time_match = re.search(time_pattern, line)
        if time_match:
            current_time = datetime.strptime(time_match.group(1), "%Y-%m-%d %H:%M:%S,%f")
            
            # Imposta l'orario di inizio
            if start_time is None:
                start_time = current_time
            
            # Imposta l'orario di fine
            end_time = current_time
        
        # Trova il numero di client
        client_match = re.search(r"client id (\d+)", line)
        if client_match:
            num_clients.add(int(client_match.group(1)))
    
    return dataset, start_time, end_time, len(num_clients)

#####################################################################################################################################################################

# Funzione per estrarre loss dai log
def extract_losses_from_file(file_path,num_clients):
    # Dizionario per memorizzare la loss per client e per epoca
    client_losses = {i: [] for i in range(1, num_clients+1)}  # 10 client
    
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Pattern per identificare le righe con la loss
    loss_pattern = r"client id (\d+) with inner epoch (\d+), Loss: ([\d\.]+)"
    
    for line in lines:
        match = re.search(loss_pattern, line)
        if match:
            client_id = int(match.group(1))
            loss = float(match.group(3))
            client_losses[client_id].append(loss)
    
    return client_losses

#####################################################################################################################################################################

# Funzione per plottare la loss
def plot_losses(client_losses):
    for client_id, losses in client_losses.items():
        plt.plot(losses, label=f"Client {client_id}")
    
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.title('Loss per client nelle varie epoche')
    plt.legend()
    #plt.show()

#####################################################################################################################################################################
#####################################################################################################################################################################

def read_logs(nome_file):
    print("ciao")

    # Estrae le informazioni dal file di log
    dataset, start_time, end_time, num_clients = extract_information_from_file(nome_file)

    # Estrae le loss dal file di log
    client_losses = extract_losses_from_file(nome_file,num_clients)

    # Salva le informazioni
    with open((nome_file[:-4] + '_info.txt'), 'w') as file:
        file.write(f"Dataset: {dataset}\n")
        file.write(f"Numero di clients: {num_clients}\n")
        file.write(f"Numero di epoche: {len(client_losses[1])}\n")
        #file.write(f"Orario di inizio: {start_time}\n")
        #file.write(f"Orario di fine: {end_time}\n")
        file.write(f"Tempo impiegato: {str(end_time-start_time)}\n")

    plot_losses(client_losses)
    plt.savefig((nome_file[:-4] + '_plot.png'))
    plt.close()