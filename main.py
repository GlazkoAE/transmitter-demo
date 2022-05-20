# TODO: add real-time spectrum plotting
# TODO: move constants to arguments with argparse
# TODO: think about transmitting data from file

import serial
import PySimpleGUI as sg
import uart
import processing
from gui import GUI


def main():
    # sudo chmod 666 /dev/ttyUSB0
    block_length_in_bits = 2 ** 12
    block_length_in_bytes = int(block_length_in_bits / 8)
    filter_coefficients = [1, 2, 3, 4, 5, 4, 3, 2, 1]
    sps = 4
    is_work = False

    gui = GUI(resolution='FHD', location=(1920, 364), title='Matrix Wave - Transmit Demo')

    while True:
        with serial.Serial('/dev/ttyUSB0', 19200, timeout=1) as ser:
            event, values = gui.window.read(timeout=20)
            if event == "Exit" or event == sg.WIN_CLOSED:
                break

            gui.set_state(event)

            if gui.is_work:
                # Transmit random data and wait for FPGA answer
                rx_signal = uart.transmit_and_receive_data(ser, block_length_in_bytes)

                # Calculate power spectral density of signal
                frequency, psd = processing.psd(rx_signal, 1e6, nperseg=256)

                # Parse signal to IQ signal
                i_signal, q_signal = processing.parce_real_imag(rx_signal, sps)

                # Filter IQ signal to get IQ samples
                i_samples = processing.filter_signal(i_signal, filter_coefficients, sps)
                q_samples = processing.filter_signal(q_signal, filter_coefficients, sps)

                # Update plots
                gui.draw(plot_name='const', x=i_samples, y=q_samples, style='ro')
                gui.draw(plot_name='spectrum', x=frequency, y=psd, style='b')
                # gui.set_axes_labels()


if __name__ == '__main__':
    main()
