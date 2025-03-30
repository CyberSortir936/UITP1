import unittest
from Classes import Tuner, BarValues, Recorder
import numpy as np

class TestRecorder(unittest.TestCase):
    def setUp(self):
        self.recorder = Recorder()
    
    def test_calculate_main_freq(self):
        sample_data = np.sin(2 * np.pi * 440 * np.arange(44100) / 44100)  # Синусоїда 440Гц
        detected_freq = self.recorder.calculate_main_freq(sample_data)
        print(f"Detected frequency: {detected_freq} Hz")
        self.assertAlmostEqual(detected_freq, 440, delta=5)  # Допуск невеликого відхилення


class TestTuner(unittest.TestCase):
    def setUp(self):
        self.tuner = Tuner()
        self.tuner.init_frequencies(440)  # A4 = 440 Hz
        self.tuner.calculate_tolerance()
    
    def test_find_octave(self):
        self.tuner.set_note_freq(220)  # A3
        result = self.tuner.find_octave()
        print(f"Octave multiplier for 220 Hz: {result}")
        self.assertEqual(result, 0.5)
        
        self.tuner.set_note_freq(880)  # A5
        result = self.tuner.find_octave()
        print(f"Octave multiplier for 880 Hz: {result}")
        self.assertEqual(result, 2)

    def test_find_note_index(self):
        self.tuner.set_note_freq(440)  # A4
        self.tuner.find_note_index(1)
        result = self.tuner.get_note()
        print(f"Detected note for 440 Hz: {result}")
        self.assertEqual(result, 'A')
    
    def test_find_offset(self):
        self.tuner.set_note_freq(445)  # Трошки вище ніж Ля
        self.tuner.find_note_index(1)
        offset = self.tuner.find_offset()
        print(f"Offset for 445 Hz: {offset} cents")
        self.assertTrue(-50 <= offset <= 50)  # Перевірка, чи нота у межах відхилення


if __name__ == '__main__':
    unittest.main()
