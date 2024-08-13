import random
import time
import threading


class CircularBuffer:
    def __init__(self, size=5):
        self.buffer = [None] * size
        self.max_size = size
        self.write_index = 0
        self.read_index = 0
        self.lock = threading.Lock()

        # Criar evento para sincronização entre threads
        self.data_available = (
            threading.Event()
        )  # Indica que há dados disponíveis para leitura
        self.space_available = (
            threading.Event()
        )  # Indica que há espaço disponível para escrita

        # Iniciar com o buffer esperando por escrita e sem dados para leitura
        self.space_available.set()

    def get_random_and_append(self):
        while True:
            self.space_available.wait()  # Espera até que haja espaço no buffer
            rand_number = random.randint(100, 1000)
            time.sleep(1)

            with self.lock:
                self.buffer[self.write_index] = rand_number
                print("      " * self.write_index + "↓")
                self.write_index = (self.write_index + 1) % self.max_size

            # Sinaliza que há dados disponíveis para leitura
            self.data_available.set()

            # Verifica se o buffer está cheio e bloqueia a escrita se necessário
            if self.write_index == self.read_index:
                self.space_available.clear()

            print("random sendo executada")

    def read_and_append(self):
        while True:
            self.data_available.wait()  # Espera até que haja dados para leitura

            with self.lock:
                data = self.buffer[self.read_index]
                self.buffer[self.read_index] = None  # Limpa o slot após a leitura
                self.read_index = (self.read_index + 1) % self.max_size

            self.append_to_txt(str(data))
            print(f"Data read and appended: {data}")

            # Sinaliza que há espaço disponível para escrita
            self.space_available.set()

            # Verifica se todos os dados foram lidos e bloqueia a leitura se necessário
            if self.write_index == self.read_index:
                self.data_available.clear()

            print("read sendo executada")

    def append_to_txt(self, data: str):
        filename = "dados.txt"
        with open(filename, "a") as file:
            file.write(data + "\n")

    def start_threads(self):
        threading.Thread(target=self.get_random_and_append, daemon=True).start()
        threading.Thread(target=self.read_and_append, daemon=True).start()


buffer = CircularBuffer()
buffer.start_threads()

# Manter o script principal em execução
while True:
    time.sleep(1)
