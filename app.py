import csv
import datetime
import tkinter as tk

class TimerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Task Timer")
        self.root.geometry("300x250")
        self.root.configure(bg="grey")

        self.timer_label = tk.Label(self.root, text="00:00:00", font=("Arial", 50))
        self.timer_label.pack(pady=10)

        self.duration_label = tk.Label(self.root, text="Total duration today: 0h 0m 0s", font=("Arial", 10))
        self.duration_label.pack(pady=5)

        self.timer_button = tk.Button(self.root, text="Start", font=("Arial", 20), command=self.toggle_timer)
        self.timer_button.pack(pady=10)

        self.is_timer_running = False
        self.start_time = None
        self.end_time = None

        self.total_duration = self.get_total_duration_today()
        self.update_duration_label()

    def toggle_timer(self):
        if not self.is_timer_running:
            self.start_time = datetime.datetime.now()
            self.is_timer_running = True
            self.timer_button.configure(text="Stop", bg="green")
            self.root.configure(bg="green")
            self.update_timer()
        else:
            self.end_time = datetime.datetime.now()
            self.is_timer_running = False
            self.timer_button.configure(text="Start", bg="grey")
            self.root.configure(bg="grey")
            self.save_data()
            self.total_duration = self.get_total_duration_today()
            self.update_duration_label()

    def update_timer(self):
        if self.is_timer_running:
            elapsed_time = datetime.datetime.now() - self.start_time
            timer_str = str(elapsed_time).split(".")[0]
            self.timer_label.configure(text=timer_str)
            self.root.after(1000, self.update_timer)

    def save_data(self):
        date_str = datetime.datetime.now().strftime("%Y-%m-%d")
        start_time_str = self.start_time.strftime("%H:%M:%S")
        end_time_str = self.end_time.strftime("%H:%M:%S")
        duration_str = str(self.end_time - self.start_time).split(".")[0]
        with open("timer-data.csv", mode="a", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([date_str, start_time_str, end_time_str, duration_str])


    def get_total_duration_today(self):
        today_str = datetime.datetime.now().strftime("%Y-%m-%d")
        total_duration = datetime.timedelta()
        try:
            with open("timer-data.csv", mode="r") as csv_file:
                reader = csv.reader(csv_file)
                next(reader)  # skip header row
                for row in reader:
                    if row[0] == today_str:
                        start_time = datetime.datetime.strptime(row[1], "%H:%M:%S")
                        end_time = datetime.datetime.strptime(row[2], "%H:%M:%S")
                        duration = end_time - start_time
                        total_duration += duration
                        print(total_duration)

        except FileNotFoundError:
            with open("timer-data.csv", mode="w", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["date", "start_time", "end_time", "duration"])
        # If no entries were found for today, return 0 duration
        if total_duration == datetime.timedelta():
            return datetime.timedelta(seconds=0)
        else:
            return total_duration


    def update_duration_label(self):
        duration_str = str(self.total_duration).split(".")[0]
        duration_hms = datetime.datetime.strptime(duration_str, "%H:%M:%S")
        duration_h = duration_hms.hour
        duration_m = duration_hms.minute
        duration_s = duration_hms.second
        self.duration_label.configure


if __name__ == "__main__":
    app = TimerApp()
    app.root.mainloop()
