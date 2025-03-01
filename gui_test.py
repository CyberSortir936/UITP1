import customtkinter as tk
from Classes import *

base_frequency = 432
is_active = False
offset = 0


def slider_get_value(value):    #Функція для отримання інформації з повзунка
    global base_frequency
    base_frequency = value
    label_freq.configure(text=str(int(base_frequency)) + 'Hz')


def switch_event():
    global is_active
    if switch_var.get() == "on":
        is_active = True
    else:
        is_active = False
    print(f"Switch is {'on' if is_active else 'off'}")

#Ініціалізація вікна
window = tk.CTk()
window._set_appearance_mode('light')

window.title("Tuner")
window.geometry("512x512")
window.resizable(False, False) #Неможна змінювати розміри вікна

recorder = Recorder()
audio_devices = recorder.get_device_names()


tuner = Tuner()

def combobox_callback(choice):
    recorder.set_device_index(int(choice[0]))


def update_loop(): #Функція оновлення викликається кожні 110мс допоки перемикач знаходиться у стані Ввімкнено
    global offset
    if is_active:
        main_frequency = recorder.calculate_main_freq(recorder.record())
        print(main_frequency)

        tuner.set_note_freq(main_frequency)
        tuner.init_frequencies(base_frequency=base_frequency)
        tuner.calculate_tolerance()
        tuner.find_note_index(tuner.find_octave())
        offset = tuner.find_offset()

        if tuner.get_sharp() == 1:
            label_sharp.configure(text_color=SHARP_ACTIVATED)
        else:
            label_sharp.configure(text_color=SHARP_DEACTIVATED)

        label_note.configure(text=tuner.get_note())

        label_cents.configure(text=str(offset)  + 'c')
        print(offset)
        left_values.set_offset(offset)
        right_values.set_offset(offset)

        left_values.set_fullness()
        left_values.fullness_check()
        left_values.set_values_left()

        right_values.set_fullness()
        right_values.fullness_check()
        right_values.set_values_right()

        for j in range(5):
            left_bars[j].configure(progress_color=left_values.get_color())
            left_bars[j].set(left_values.get_value_at_index(j))

            right_bars[j].configure(progress_color=right_values.get_color())
            right_bars[j].set(right_values.get_value_at_index(j))

        tuner.clear_frequencies()
    window.after(110, update_loop)

#Малювання інтерфейсу
left_values = BarValues(color=YELLOW)
right_values = BarValues(color=RED)

left_bars = []
right_bars = []

combobox = tk.CTkComboBox(window, values=audio_devices,
                                     command=combobox_callback)
combobox.set(audio_devices[recorder.get_device_index()])
combobox.place(x=20, y=20)

for i in range(5):
    left_bars.append(tk.CTkProgressBar(window, orientation="vertical", width=BAR_WIDTH, height=BAR_HEIGHT + BAR_HEIGHT_DIFFERENCE * i, progress_color=left_values.get_color()))
    left_bars[i].set(left_values.get_value_at_index(i))
    left_bars[i].place(x=BAR_LEFT_START + BAR_MARGIN * i, y=BAR_Y_START_POSITION - BAR_HEIGHT_DIFFERENCE * i)

    right_bars.append(tk.CTkProgressBar(window, orientation="vertical", width=BAR_WIDTH, height=BAR_HEIGHT + BAR_HEIGHT_DIFFERENCE * i, progress_color=right_values.get_color()))
    right_bars[i].set(right_values.get_value_at_index(i))
    right_bars[i].place(x=BAR_RIGHT_START - BAR_MARGIN * i, y=BAR_Y_START_POSITION - BAR_HEIGHT_DIFFERENCE * i)


label_freq = tk.CTkLabel(window, text=str(base_frequency) + 'Hz', fg_color="transparent", font=("Cascadia Mono", 20))
label_freq.place(x=BAR_LEFT_START + BAR_MARGIN, y=352)
label_cents = tk.CTkLabel(window, text=str(offset) + 'c', fg_color="transparent", font=("Cascadia Mono", 20))
label_cents.place(x=BAR_RIGHT_START - BAR_MARGIN - BAR_WIDTH * 2, y=352)
slider = tk.CTkSlider(window, from_=415, to=466, command=slider_get_value, height=BAR_WIDTH/2, width=BAR_RIGHT_START - BAR_LEFT_START + BAR_WIDTH, number_of_steps=51)
slider.place(x=BAR_LEFT_START, y=380)

switch_var = tk.StringVar(value="off")
switch = tk.CTkSwitch(window, command=switch_event,
                                 variable=switch_var, onvalue="on", offvalue="off", text='')
switch.place(x=246, y=400)

label_note = tk.CTkLabel(window, text="0", font=("Cascadia Mono", 128), fg_color="transparent")
label_note.place(x=228, y=180)
label_sharp = tk.CTkLabel(window, text='#', font=("Cascadia Mono", 64), text_color=SHARP_DEACTIVATED)
label_sharp.place(x=300, y=150)

#Виклик функції оновлення
update_loop()

window.mainloop()
