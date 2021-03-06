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
        self.window.Maximize()
        self.canvas_elem = self.window['plots']

    def get_layout(self):
        # Define the window layout
        plot_w = int(self.size[0])
        plot_h = int(self.size[1])
        btn_w = int(self.size[0] / 200)
        btn_h = int(self.size[0] / 1000)
        layout_btn = [
            [sg.Button("Start", size=(btn_w, btn_h))],
            [sg.Button("Stop", size=(btn_w, btn_h))],
            [sg.Button("Exit", size=(btn_w, btn_h))],
        ]
        layout_canvas = [
            [sg.Canvas(size=(plot_w, plot_h), key='plots')],
        ]
        layout = [
            # [sg.Text("Matrix Wave - Transmitter demo", size=(60, 1), justification="center")],
            [sg.Col(layout_btn),
             sg.Col(layout_canvas),
             ]
        ]
        return layout

    def set_state(self, event):
        if event == "Start":
            self.is_work = True
        elif event == "Stop":
            self.is_work = False


class Axes:
    def __init__(self, canvas_elem):
        self.canvas = canvas_elem.TKCanvas
        self.fig = Figure(figsize=(15, 10))
        self.ax11 = Plot(self.fig,
                         location=221,
                         xlabel='Frequency, kHz',
                         ylabel='PSD, V2/Hz',
                         title='Power spectral density',
                         )
        self.ax12 = Plot(self.fig,
                         location=222,
                         xlabel='I samples',
                         ylabel='Q samples',
                         title='Constellation')
        self.ax21 = Plot(self.fig,
                         location=223,
                         xlabel='Samples',
                         ylabel='Signal',
                         title='Signal with shaping pulses')
        self.ax22 = Plot(self.fig,
                         location=224,
                         xlabel='Samples',
                         ylabel='Signal',
                         title='Signal without shaping pulses')
        # fig, ((self.ax11, self.ax12), (self.ax21, self.ax22)) = plt.subplots(nrows=2, ncols=2)
        self.fig_canvas = _draw_figure(self.canvas, self.fig)

    def draw(self, ax, x, y, style='b.', is_clear=False):
        ax.draw(x, y, style, is_clear)
        self.fig_canvas.draw()


class Plot:
    def __init__(self, fig, location=111, xlabel='X', ylabel='Y', title='Title'):
        self.ax = fig.add_subplot(location)
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.title = title
        self.set_labels()

    def draw(self, x, y, style='b.', is_clear=False):
        if not is_clear:
            self.ax.cla()
            self.set_labels()
        self.ax.plot(x, y, style)

    def set_labels(self):
        self.ax.set_xlabel(self.xlabel, fontsize=8)
        self.ax.set_ylabel(self.ylabel, fontsize=8)
        self.ax.set_title(self.title, y=0.98, fontsize=10)
        self.ax.grid()
