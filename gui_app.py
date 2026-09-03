import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
import threading
import json

class APIMeshGatewayStudio:
    def __init__(self, root):
        self.root = root
        self.root.title('API Mesh Gateway Studio')
        self.root.geometry('800x600')
        self.root.configure(bg='#2d2d2d')

        self.style = ttk.Style()
        self.style.configure('TFrame', background='#2d2d2d')
        self.style.configure('TButton', background='#444', foreground='white', font=('Arial', 10))
        self.style.configure('TLabel', background='#2d2d2d', foreground='white', font=('Arial', 10))
        self.style.configure('TEntry', background='#444', foreground='white', font=('Arial', 10))

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10, expand=True)

        self.create_left_panel(left_frame)
        self.create_right_panel(right_frame)

    def create_left_panel(self, frame):
        lbl_title = ttk.Label(frame, text='API Mesh Gateway Studio', font=('Arial', 14))
        lbl_title.pack(pady=10)

        lbl_api_url = ttk.Label(frame, text='API URL:')
        lbl_api_url.pack(pady=5)

        self.entry_api_url = ttk.Entry(frame, width=40)
        self.entry_api_url.pack(pady=5)

        lbl_rate_limit = ttk.Label(frame, text='Rate Limit (req/sec):')
        lbl_rate_limit.pack(pady=5)

        self.entry_rate_limit = ttk.Entry(frame, width=40)
        self.entry_rate_limit.pack(pady=5)

        lbl_auth_token = ttk.Label(frame, text='Auth Token:')
        lbl_auth_token.pack(pady=5)

        self.entry_auth_token = ttk.Entry(frame, width=40)
        self.entry_auth_token.pack(pady=5)

        btn_save = ttk.Button(frame, text='Save Configuration', command=self.save_configuration)
        btn_save.pack(pady=10)

        btn_monitor = ttk.Button(frame, text='Monitor Traffic', command=self.monitor_traffic)
        btn_monitor.pack(pady=10)

    def create_right_panel(self, frame):
        lbl_status = ttk.Label(frame, text='Status: Idle')
        lbl_status.pack(pady=10)

        self.lbl_status = lbl_status

        self.traffic_chart = tk.Canvas(frame, bg='#444', width=400, height=200)
        self.traffic_chart.pack(pady=10)

        self.latency_chart = tk.Canvas(frame, bg='#444', width=400, height=200)
        self.latency_chart.pack(pady=10)

    def save_configuration(self):
        api_url = self.entry_api_url.get()
        rate_limit = self.entry_rate_limit.get()
        auth_token = self.entry_auth_token.get()

        if not api_url or not rate_limit or not auth_token:
            messagebox.showerror('Error', 'Please fill in all fields')
            return

        config = {
            'api_url': api_url,
            'rate_limit': rate_limit,
            'auth_token': auth_token
        }

        with open('config.json', 'w') as f:
            json.dump(config, f)

        messagebox.showinfo('Success', 'Configuration saved successfully')

    def monitor_traffic(self):
        self.lbl_status.config(text='Status: Monitoring...')
        threading.Thread(target=self.fetch_traffic_data).start()

    def fetch_traffic_data(self):
        try:
            response = requests.get('http://localhost:8000/api/traffic')
            data = response.json()
            self.update_charts(data)
            self.lbl_status.config(text='Status: Idle')
        except Exception as e:
            self.lbl_status.config(text=f'Status: Error - {str(e)}')

    def update_charts(self, data):
        self.traffic_chart.delete('all')
        self.latency_chart.delete('all')

        traffic_data = data['traffic']
        latency_data = data['latency']

        self.draw_chart(self.traffic_chart, traffic_data, 'Traffic Flow')
        self.draw_chart(self.latency_chart, latency_data, 'Latency (ms)')

    def draw_chart(self, canvas, data, title):
        canvas.create_text(200, 10, text=title, fill='white', font=('Arial', 12))

        max_value = max(data)
        scale_factor = 180 / max_value

        for i in range(len(data)):
            x = i * 20 + 20
            y = 200 - data[i] * scale_factor
            canvas.create_rectangle(x, 200, x + 15, y, fill='lightblue')

if __name__ == '__main__':
    root = tk.Tk()
    app = APIMeshGatewayStudio(root)
    root.mainloop()