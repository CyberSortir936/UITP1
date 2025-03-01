from math import isclose
import pyaudio
import numpy as np

#Кольори
GREEN = '#b4eeb4'
YELLOW = '#fff68f'
RED = '#ff6666'
SHARP_DEACTIVATED = '#1f1f1f'
SHARP_ACTIVATED = '#ffffff'

#Розміри для інтерфейсу
BAR_WIDTH = 16
BAR_HEIGHT = 128
BAR_HEIGHT_DIFFERENCE = 32
BAR_MARGIN = 24
BAR_LEFT_START = 64
BAR_RIGHT_START = 448
BAR_Y_START_POSITION = 224

#Константи для запису звуку
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1  # MONO
RATE = 44100 #Семпл-рейт
RECORD_SECONDS = 0.1


class BarValues:
    def __init__(self, color):
        self.values = [0, 0, 0, 0, 0]
        self.offset = 0
        self.is_full = False
        self.color = color
        self.original_color = color

    def set_offset(self, offset):
        self.offset = offset

    def set_values_left(self): #Можна було б зробити або два різних класи, або одну елегантну функцію
        if self.offset < 0:     #Перше занадто затратно, а для другого я недостатньо розумний, тому маємо таку суміш
            match abs(self.offset):
                case v if 2 < v <= 10:
                    for i in range(4):
                        self.values[i] = 1
                    self.values[4] = (10 - v) * 0.125
                case v if 11 <= v <= 20:
                    for i in range(3):
                        self.values[i] = 1
                    self.values[3] = (10 - (v - 10)) * 0.1
                case v if 21 <= v <= 30:
                    for i in range(2):
                        self.values[i] = 1
                    self.values[2] = (10 - (v - 10 * 2)) * 0.1
                case v if 31 <= v <= 40:
                    self.values[0] = 1
                    self.values[1] = (10 - (v - 10 * 3)) * 0.1
                case v if 41 <= v <= 50:
                    self.values[0] = (10 - (v - 10 * 4)) * 0.1
                case _:
                    for i in range(5):
                        self.values[i] = 1
        else:
            for i in range(5):
                self.values[i] = 1

    def set_values_right(self):
        if self.offset >= 0:
            match abs(self.offset):
                case v if 2 < v <= 10:
                    self.values[4] = v * 0.125
                case v if 11 <= v <= 20:
                    self.values[4] = 1
                    self.values[3] = (v - 10 * 1) * 0.1
                case v if 21 <= v <= 30:
                    for i in range(4, 2, -1):
                        self.values[i] = 1
                    self.values[2] = (v - 10 * 2) * 0.1
                case v if 31 <= v <= 40:
                    for i in range(4, 1, -1):
                        self.values[i] = 1
                    self.values[1] = (v - 10 * 3) * 0.1
                case v if 41 <= v <= 50:
                    for i in range(4, 0, -1):
                        self.values[i] = 1
                    self.values[0] = (v - 10 * 4) * 0.1
                case _:
                    for i in range(5):
                        self.values[i] = 1
        else:
            for i in range(5):
                self.values[i] = 0

    def set_fullness(self):
        if abs(self.offset) <= 2:
            self.is_full = True
            print('full')
        else:
            self.is_full = False

    def fullness_check(self):
        if self.is_full:
            for i in range(len(self.values)):
                self.values[i] = 1
            self.color = GREEN
        else:
            for i in range(len(self.values)):
                self.values[i] = 0
            self.color = self.original_color

    def get_value_at_index(self, index):
        return self.values[index]

    def get_color(self):
        return self.color


#ПРИДУМАЙ ЯК ВРАХУВАТИ КРАЙНІ МЕЖІ, ДО ЛЯ І ПІСЛЯ СОЛЬ
class Tuner:
    def __init__(self):
        self.notes = ['G', 'A', 'A', 'B', 'C', 'C', 'D', 'D', 'E', 'F', 'F', 'G', 'G', 'A']
        self.sharps = [1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0]
        self.note_index = 0
        self.note_freq = 0
        self.frequencies = []
        self.tolerance = 0
        self.is_up = False

    def set_note_freq(self, note_freq):
        self.note_freq = note_freq

    def init_frequencies(self, base_frequency):
        for i in range(12):
            self.frequencies.append(base_frequency * (2 ** (i/12)))

    def find_octave(self):
        temp_note = self.note_freq
        multiply_count = 1
        if isclose(self.note_freq, self.frequencies[0], rel_tol=self.tolerance):
            multiply_count = 1
        elif self.note_freq < self.frequencies[0]:
            while temp_note < self.frequencies[0]:
                temp_note *= 2
                multiply_count /= 2
        elif self.note_freq > self.frequencies[11]:
            while temp_note > self.frequencies[11]:
                temp_note /= 2
                multiply_count *= 2
        print(multiply_count)
        return multiply_count

    def calculate_tolerance(self):
        average_distance = self.frequencies[6] - self.frequencies[5]
        step = average_distance / 100
        self.tolerance = step / 150

    def find_note_index(self, multiply_count):
        for i in range(len(self.frequencies)):
            self.frequencies[i] *= multiply_count

        first_note = self.frequencies[0] / 2 * (2 ** (11 / 12))
        self.frequencies.insert(0, first_note)
        self.frequencies.append(self.frequencies[1] * 2)

        if self.note_freq > self.frequencies[-2]:
            for i in range(len(self.frequencies)):
                self.frequencies[i] *= 2

        boundaries = ()

        for i in range(1, len(self.frequencies) - 1, 1):
            print(self.frequencies[i])
            if self.note_freq < self.frequencies[i]:
                boundaries = (i - 1, i)
                break

        if self.note_freq >= (self.frequencies[boundaries[0]] + self.frequencies[boundaries[1]]) / 2:
            self.note_index = boundaries[1]
        else:
            self.note_index = boundaries[0]
        print(boundaries)
        print(self.note_index)

        if self.note_freq > self.frequencies[self.note_index]:
            self.is_up = False
        else:
            self.is_up = True

    def get_note(self):
        return self.notes[self.note_index]

    def get_sharp(self):
        return self.sharps[self.note_index]

    def find_offset(self):
        print(self.frequencies)

        offset = 0
        if isclose(self.frequencies[self.note_index], self.note_freq, rel_tol=self.tolerance):
            offset = 0
            return offset
        elif not self.is_up:
            for i in range(50):
                print(str(offset))
                if isclose(self.note_freq + offset, self.frequencies[self.note_index], rel_tol=self.tolerance):
                    return -offset
                elif self.note_freq + offset < self.frequencies[self.note_index]:
                    return -offset
                offset -= 1
        elif self.is_up:
            for i in range(50):
                print('+' + str(offset))
                print(self.note_freq + offset)
                if isclose(self.note_freq + offset, self.frequencies[self.note_index], rel_tol=self.tolerance):
                    return -offset
                elif self.note_freq + offset > self.frequencies[self.note_index]:
                    return -offset
                offset += 1
        else:
            return -offset

    def clear_frequencies(self):
        self.frequencies = []
#ТЕПЕР ДУМАЙ ЯК ЦЕ НОРМАЛЬНО ПОЄДНАТИ З ПОПЕРЕДНІМ КЛАСОМ


class Recorder:
    def __init__(self):
        self.device_names = []
        self.device_index = 0
        self.frames = []

    def get_device_names(self):
        p = pyaudio.PyAudio()   # Але для зручності сприйняття і оскільки ми пишемо всеодно в моно, тут обираються лише перші девайси, до того як почнуть повторюватись
        device_count = p.get_device_count()
        for i in range(device_count): # Взагалі ці девайси будуть дублюватися по 2 а інколи і по 4, залежно від того в якому режимі ми записуємо
            device_info = p.get_device_info_by_index(i) # Але для зручності сприйняття і оскільки ми пишемо всеодно в моно, тут обираються лише перші девайси, до того як почнуть повторюватись
            if device_info.get('maxInputChannels') > 0 and device_info.get('hostApi') == 0 and device_info.get( # Деякі системні або сторонні інтерфейси є віртуальними і не можуть писати звук, тому нам треба ті, у яких більше ніж 0 входів
                    'index') != 0: # Також ми прибираємо деавайс з індексом 0, бо це дефолтний віртуальний інтерфейс вінди, його користувач системи не бачить
                self.device_names.append(str(device_info.get('index')) + ' - ' + str(device_info.get('name'))) # Всіма цими обмеженянми ми лишаємо лише ті інтерфейси, які користувач бачить в налаштуваннях вінди
        p.terminate()
        return self.device_names

    def set_device_index(self, device_index):
        self.device_index = device_index
        print("Device index: ", device_index)

    def get_device_index(self):
        return self.device_index

    def record(self):
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK,
                        input_device_index=self.device_index)

        for _ in range(int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            self.frames.append(np.frombuffer(data, dtype=np.int16)) # пишемо чанки в масив frames

        stream.stop_stream()
        stream.close()
        p.terminate()

        numpydata = np.hstack(self.frames)
        return numpydata

    def calculate_main_freq(self, numpydata):
        fft_result = np.fft.fft(numpydata) # Швидке перетворення Фур'є
        fft_magnitude = np.abs(fft_result)  # Список з потужностями частот
        frequencies = np.fft.fftfreq(len(fft_magnitude), 1 / RATE)  # Список самих частот

        lower_threshold = 20  # Мінімальна частота, середня людина чує від 20 до 20000 Гц
        upper_threshold = 20000  # Максимальна частота

        valid_freq_mask = (frequencies >= lower_threshold) & (frequencies <= upper_threshold)

        valid_frequencies = frequencies[valid_freq_mask] # Застосовуємо обмеження
        valid_fft_magnitude = fft_magnitude[valid_freq_mask]

        main_frequency_index = np.argmax(valid_fft_magnitude)
        main_frequency = valid_frequencies[main_frequency_index]

        return main_frequency
