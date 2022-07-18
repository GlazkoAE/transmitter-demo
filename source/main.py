import serial
import PySimpleGUI as sg

import uart
import processing
from gui import GUI, Axes


def main():
    # sudo chmod 666 /dev/ttyUSB0
    baud_rate = 115200
    block_length_in_bits = 2 ** 14
    welch_nperseg = 100
    bytes_per_sample = 2
    is_single_byte = False
    block_length_in_bytes = int(block_length_in_bits / 8)
    filter_coefficients = [6, 3, -4, -10, -8, 2, 16, 23, 13, -13, -40, -47, -15, 57, 149, 226, 255, 226, 149, 57,
                           -15,
                           -47, -40, -13, 13, 23, 16, 2, -8, -10, -4, 3, 6]
    filter_power = sum(x ** 2 for x in filter_coefficients)
    sps = 4
    samples_to_show = 500
    symbols_to_show = 100

    gui = GUI(resolution='FHD', location=(0, 100), title='Matrix Wave - Transmit Demo')
    axes = Axes(gui.canvas_elem)

    while True:
        # /dev/ttyUSB0 for unix/linux, COMx for windows (you should check number of COM by yourself)
        with serial.Serial('/dev/ttyUSB0', baud_rate, timeout=1) as ser:
            event, values = gui.window.read(timeout=20)
            if event == "Exit" or event == sg.WIN_CLOSED:
                break

            gui.set_state(event)

            if gui.is_work:
                # Transmit random data and wait for FPGA answer
                rx_signal = uart.transmit_and_receive_data(ser,
                                                           block_length_in_bytes,
                                                           is_single_byte=is_single_byte,
                                                           bytes_per_sample=bytes_per_sample)
                
                
                # Parse signal to IQ signal
                i_signal, q_signal = processing.parce_real_imag(rx_signal)

                # Calculate power spectral density of signal
                frequency, psd = processing.psd(i_signal, q_signal, 1e6, nperseg=welch_nperseg)

                # Filter IQ signal to get IQ samples
                i_signal  = i_signal[sps:]
                q_signal  = q_signal[sps:]
                i_samples = processing.filter_signal(i_signal, filter_coefficients, sps) / filter_power
                q_samples = processing.filter_signal(q_signal, filter_coefficients, sps) / filter_power
                i_samples = i_samples[32:32 + sps*(symbols_to_show):sps]
                q_samples = q_samples[32:32 + sps*(symbols_to_show):sps]

                #print(i_samples)
                #print(q_samples)
                #break

                # Update plots
                axes.draw(ax=axes.ax11, x=frequency, y=psd, style='b')
                axes.draw(ax=axes.ax12, x=i_samples, y=q_samples, style='ro')
                axes.draw(ax=axes.ax21, x=range(samples_to_show), y=i_signal[:samples_to_show], style='b',
                          is_clear=False, )
                axes.draw(ax=axes.ax21, x=range(samples_to_show), y=q_signal[:samples_to_show], style='r',
                          is_clear=True)
                axes.draw(ax=axes.ax22, x=range(symbols_to_show), y=i_samples[:symbols_to_show], style='b',
                          is_clear=False)
                axes.draw(ax=axes.ax22, x=range(symbols_to_show), y=q_samples[:symbols_to_show], style='r',
                          is_clear=True)


if __name__ == '__main__':
    main()
