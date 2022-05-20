import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def _get_size(resolution, size):
    if resolution == 'HD':
        return 1280, 720
    elif resolution == 'FHD':
        return 1920, 1080
    elif resolution == '2k':
        return 2560, 1440
    elif resolution == 'custom':
        return size
    else:
        print('Unknown resolution value. Setting default HD (1280x720)')
        return 1280, 720


def _draw_figure(canvas, figure, side='right'):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side=side, fill="both", expand=1)
    return figure_canvas_agg


class GUI:
    def __init__(self, resolution='custom', size=(1280, 720), location=(0, 0), title='Default Title'):
        self.size = _get_size(resolution, size)
        self.is_work = False
        self.layout = self.get_layout()
        self.window = sg.Window(title, self.layout, finalize=True, size=self.size, location=location, resizable=True,
                                font="Helvetica 38")
        self.ax_const, self.ax_spectrum, self.fig_const_canvas, self.fig_spectrum_canvas = self.get_initial_plots()
        self.set_axes_labels()

    def get_layout(self):
        # Define the window layout
        plot_w = int(self.size[0] / 2)
        plot_h = int(self.size[1] / 2)
        btn_w = int(self.size[0] / 200)
        btn_h = int(self.size[0] / 1000)
        layout_btn = [
            [sg.Button("Start", size=(btn_w, btn_h))],
            [sg.Button("Stop", size=(btn_w, btn_h))],
            [sg.Button("Exit", size=(btn_w, btn_h))],
        ]
        layout_const = [
            [sg.Canvas(size=(plot_w, plot_h), key='constellation')],
            [sg.Push()],
        ]
        layout_spectrum = [
            [sg.Canvas(size=(plot_w, plot_h), key='spectrum')],
            [sg.Push()]
        ]
        layout = [
            # [sg.Text("Matrix Wave - Transmitter demo", size=(60, 1), justification="center")],
            [sg.Col(layout_btn),
             sg.Col(layout_spectrum),
             sg.Col(layout_const)]
        ]
        return layout

    def get_initial_plots(self):
        canvas_const_elem = self.window['constellation']
        canvas_const = canvas_const_elem.TKCanvas
        fig_const = Figure()
        ax_const = fig_const.add_subplot(111)
        fig_const_canvas = _draw_figure(canvas_const, fig_const)

        canvas_spectrum_elem = self.window['spectrum']
        canvas_spectrum = canvas_spectrum_elem.TKCanvas
        fig_spectrum = Figure()
        ax_spectrum = fig_spectrum.add_subplot(111)
        fig_spectrum_canvas = _draw_figure(canvas_spectrum, fig_spectrum)

        return ax_const, ax_spectrum, fig_const_canvas, fig_spectrum_canvas

    def set_axes_labels(self):
        self.ax_spectrum.set_xlabel("Frequency, kHz")
        self.ax_spectrum.set_ylabel("PSD, V2/Hz")
        self.ax_spectrum.set_title("Power spectral density")
        self.ax_spectrum.grid()

        self.ax_const.set_xlabel("Real")
        self.ax_const.set_ylabel("Imag")
        self.ax_const.set_title("Constellation")
        self.ax_const.grid()

    def draw(self, plot_name, x, y, style='b.'):
        if plot_name == 'const':
            self.ax_const.clear()
            self.ax_const.grid()
            self.ax_const.plot(x, y, style)
            self.fig_const_canvas.draw()

        elif plot_name == 'spectrum':
            self.ax_spectrum.clear()
            self.ax_spectrum.grid()
            self.ax_spectrum.plot(x, y, style)
            self.fig_spectrum_canvas.draw()

    def set_state(self, event):
        if event == "Start":
            self.is_work = True
        elif event == "Stop":
            self.is_work = False
