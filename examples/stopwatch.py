import tkinter as tk

# The two following lines are NOT needed in a typical environment.
# These lines make sismic available in our testing environment
import sys
sys.path.append('..')

from sismic.io import import_from_yaml
from sismic.interpreter import Interpreter, run_in_background
from sismic.model import Event


# Create a tiny GUI
class StopwatchApplication(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)

        # Initialize widgets
        self.create_widgets()

        # Create a Stopwatch interpreter
        with open('stopwatch.yaml') as f:
            statechart = import_from_yaml(f)
        self.interpreter = Interpreter(statechart)

        # Bind interpreter events to the GUI
        self.interpreter.bind(self.event_handler)

        # Run the interpreter
        self.run = run_in_background(self.interpreter, delay=0.2)

    def create_widgets(self):
        self.pack()

        # Add buttons
        self.w_btn_start = tk.Button(self, text='start', command=self._start)
        self.w_btn_stop = tk.Button(self, text='stop', command=self._stop)
        self.w_btn_split = tk.Button(self, text='split', command=self._split)
        self.w_btn_unsplit = tk.Button(self, text='unsplit', command=self._unsplit)
        self.w_btn_reset = tk.Button(self, text='reset', command=self._reset)
        self.w_btn_quit = tk.Button(self, text='quit', command=self._quit)

        # Initial states
        self.w_btn_stop['state'] = tk.DISABLED
        self.w_btn_unsplit['state'] = tk.DISABLED

        # Pack
        self.w_btn_start.pack(side=tk.LEFT,)
        self.w_btn_stop.pack(side=tk.LEFT,)
        self.w_btn_split.pack(side=tk.LEFT,)
        self.w_btn_unsplit.pack(side=tk.LEFT,)
        self.w_btn_reset.pack(side=tk.LEFT,)
        self.w_btn_quit.pack(side=tk.LEFT,)

        # Timer label
        self.w_timer = tk.Label(root, font=("Helvetica", 16))
        self.w_timer.pack(side=tk.TOP, fill=tk.X)

    def event_handler(self, event):
        # Update text widget when timer value is updated
        if event.name == 'updated':
            self.w_timer['text'] = self.interpreter.context['display_time']

    def _start(self):
        self.interpreter.send(Event('start_button'))
        self.w_btn_start['state'] = tk.DISABLED
        self.w_btn_stop['state'] = tk.NORMAL

    def _stop(self):
        self.interpreter.send(Event('stop_button'))
        self.w_btn_start['state'] = tk.NORMAL
        self.w_btn_stop['state'] = tk.DISABLED

    def _reset(self):
        self.interpreter.send(Event('reset_button'))

    def _split(self):
        self.w_btn_split['state'] = tk.DISABLED
        self.w_btn_unsplit['state'] = tk.NORMAL
        self.interpreter.send(Event('split_button'))

    def _unsplit(self):
        self.w_btn_split['state'] = tk.NORMAL
        self.w_btn_unsplit['state'] = tk.DISABLED
        self.interpreter.send(Event('split_button'))

    def _quit(self):
        self.run.stop()
        self.master.destroy()


if __name__ == '__main__':
    # Create GUI
    root = tk.Tk()
    root.wm_title('StopWatch')
    app = StopwatchApplication(master=root)

    app.mainloop()