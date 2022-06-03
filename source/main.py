# TODO: move constants to arguments with argparse
# TODO: think about transmitting data from file

import serial
import PySimpleGUI as sg
import uart
import processing
from gui import GUI, Axes


def main():
    # sudo chmod 666 /dev/ttyUSB0
    baud_rate = 115200
    block_length_in_bits = 2 ** 12
    welch_nperseg = 512
    is_single_byte = False
    block_length_in_bytes = int(block_length_in_bits / 8)
    filter_coefficients = [6, 3, -4, -10, -8, 2, 16, 23, 13, -13, -40, -47, -15, 57, 149, 226, 255, 226, 149, 57, -15,
                           -47, -40, -13, 13, 23, 16, 2, -8, -10, -4, 3, 6]
    sps = 4

    gui = GUI(resolution='FHD', location=(0, 100), title='Matrix Wave - Transmit Demo')
    ax_const = Axes(gui.canvas_const_elem, xlabel='I samples', ylabel='Q samples', title='Constellation')
    ax_psd = Axes(gui.canvas_spectrum_elem, xlabel='Frequency, kHz', ylabel='PSD, V2/Hz',
                  title='Power spectral density')

    while True:
        with serial.Serial('/dev/ttyUSB0', baud_rate, timeout=1) as ser:
            event, values = gui.window.read(timeout=20)
            if event == "Exit" or event == sg.WIN_CLOSED:
                break

            gui.set_state(event)

            if gui.is_work:
                # Transmit random data and wait for FPGA answer
                rx_signal = uart.transmit_and_receive_data(ser, block_length_in_bytes, is_single_byte=is_single_byte)

                # Calculate power spectral density of signal
                frequency, psd = processing.psd(rx_signal, 1e6, nperseg=welch_nperseg)

                # Parse signal to IQ signal
                i_signal, q_signal = processing.parce_real_imag(rx_signal, sps)

                # Filter IQ signal to get IQ samples
                i_samples = processing.filter_signal(i_signal, filter_coefficients, sps)
                q_samples = processing.filter_signal(q_signal, filter_coefficients, sps)

                # Update plots
                ax_const.draw(x=i_samples, y=q_samples, style='ro')
                ax_psd.draw(x=frequency, y=psd, style='b')


if __name__ == '__main__':
    main()
