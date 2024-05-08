import tkinter as tk
from tkinter import messagebox
import pygame.mixer
import cv2
from PIL import Image, ImageTk


class WidgetMarketGame(tk.Tk):
    def _init_(self):
        super()._init_()
        self.title("Widget Market Middleman Game")
        self.geometry("600x400")
        self.producers = []
        self.consumers = []

        self.create_welcome_window()
    def add_background_video(self):
        # Initialize video capture using OpenCV
        self.cap = cv2.VideoCapture('C:/Users/hp/Downloads/VID-20230809-WA0001.mp4')  # Replace with the path to your background video file
        # Create a Canvas to display the video frames
        self.canvas = tk.Canvas(self, width=1100, height=300)  # Adjust the canvas size as needed
        self.canvas.pack()
        # Initialize pygame mixer
        pygame.mixer.init()
        pygame.mixer.music.load(r'C:/Users/hp/Downloads/mixkit-clinking-coins-1993.mp3')  # Replace with the path to your background music file
        pygame.mixer.music.play(-1)  # Play the background music in a loop
        # Start the video playback
        self.update_video()
    def update_video(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            self.photo = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            self.after(20, self.update_video)  # Update every 20 milliseconds


    def create_welcome_window(self):
        self.welcome_label = tk.Label(self, text="Welcome to the Auction", font=("Helvetica", 16, "bold"))
        self.welcome_label.pack(pady=20)

        self.start_button = tk.Button(self, text="Start Game", command=self.create_input_window)
        self.start_button.pack()

    def create_input_window(self):
        self.welcome_label.destroy()
        self.start_button.destroy()
        self.title("board")
        self.input_frame = tk.Frame(self)
        self.input_frame.pack(pady=20)

        self.producer_label = tk.Label(self.input_frame, text="Number of Producers:")
        self.producer_label.grid(row=0, column=0)
        self.producer_entry = tk.Entry(self.input_frame)
        self.producer_entry.grid(row=0, column=1)

        self.consumer_label = tk.Label(self.input_frame, text="Number of Consumers:")
        self.consumer_label.grid(row=1, column=0)
        self.consumer_entry = tk.Entry(self.input_frame)
        self.consumer_entry.grid(row=1, column=1)

        self.add_fields_button = tk.Button(self.input_frame, text="Add Fields", command=self.add_fields)
        self.add_fields_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.calculate_button = tk.Button(self, text="Calculate Max Profit", command=self.calculate_max_profit)
        self.calculate_button.pack(padx=5,pady=5)

    def add_fields(self):
        self.title("game")
        num_producers = int(self.producer_entry.get())
        num_consumers = int(self.consumer_entry.get())

        for widget in self.input_frame.winfo_children():
            widget.destroy()

        self.producer_label = tk.Label(self.input_frame, text="Producer Details", font=("Helvetica", 14, "bold"))
        self.producer_label.grid(row=0, column=0, columnspan=3, pady=5)

        for i in range(num_producers):
            producer_frame = tk.Frame(self.input_frame)
            producer_frame.grid(row=i+1, column=0, columnspan=3, pady=5)

            producer_name_label = tk.Label(producer_frame, text=f"Producer {i+1} Name:")
            producer_name_label.grid(row=0, column=0)
            producer_name_entry = tk.Entry(producer_frame)
            producer_name_entry.grid(row=0, column=1)

            producer_price_label = tk.Label(producer_frame, text="Price:")
            producer_price_label.grid(row=1, column=0)
            producer_price_entry = tk.Entry(producer_frame)
            producer_price_entry.grid(row=1, column=1)

            producer_start_label = tk.Label(producer_frame, text="Start Date:")
            producer_start_label.grid(row=2, column=0)
            producer_start_entry = tk.Entry(producer_frame)
            producer_start_entry.grid(row=2, column=1)

            self.producers.append((producer_name_entry, producer_price_entry, producer_start_entry))
        

        self.consumer_label = tk.Label(self.input_frame, text="Consumer Details", font=("Helvetica", 14, "bold"))
        self.consumer_label.grid(row=num_producers+2, column=0, columnspan=3, pady=5)

        for i in range(num_consumers):
            consumer_frame = tk.Frame(self.input_frame)
            consumer_frame.grid(row=num_producers+i+3, column=0, columnspan=3, pady=5)

            consumer_name_label = tk.Label(consumer_frame, text=f"Consumer {i+1} Name:")
            consumer_name_label.grid(row=0, column=0)
            consumer_name_entry = tk.Entry(consumer_frame)
            consumer_name_entry.grid(row=0, column=1)

            consumer_price_label = tk.Label(consumer_frame, text="Price:")
            consumer_price_label.grid(row=1, column=0)
            consumer_price_entry = tk.Entry(consumer_frame)
            consumer_price_entry.grid(row=1, column=1)

            consumer_end_label = tk.Label(consumer_frame, text="End Date:")
            consumer_end_label.grid(row=2, column=0)
            consumer_end_entry = tk.Entry(consumer_frame)
            consumer_end_entry.grid(row=2, column=1)

            self.consumers.append((consumer_name_entry, consumer_price_entry, consumer_end_entry))

    def calculate_max_profit(self):
        # Profit calculation logic
        max_profit = [ ]
        maxi = 0
        selected_producer = None
        selected_consumer = None

        for producer_data in self.producers:
            producer_price = int(producer_data[1].get())
            producer_start = int(producer_data[2].get())

            for consumer_data in self.consumers:
                consumer_price = int(consumer_data[1].get())
                consumer_end = int(consumer_data[2].get())
                #start_date = max(producer_start, 1)
                #end_date = min(consumer_end, producer_start + len(self.consumers) - 1)

                #potential_profit = 0
                if producer_price<=consumer_price and producer_start<=consumer_end:
                    max_profit.append(consumer_price-producer_price)
                    #break


                #if potential_profit > max_profit:
                    #max_profit = potential_profit
                selected_producer = producer_data[0].get()
                selected_consumer = consumer_data[0].get()
                if max_profit:
                    maxi = max(max_profit)
                if maxi==0:
                    selected_producer = "none"
                    selected_consumer = "none" 
        # Display the result in a message box
        result_msg = f"Maximized profit: {maxi}\nSelected Producer: {selected_producer}\nSelected Consumer: {selected_consumer}"
        messagebox.showinfo("Maximize Profits", result_msg)

if _name_ == "_main_":
    app = WidgetMarketGame()
    app.add_background_video()  # Add the background video to the game
    app.mainloop()
class close_window:
    def _init_(self, root):
        self.root = root
        self.root.title("winner")
        # Initialize video capture using OpenCV
        self.cap = cv2.VideoCapture('C:/Users/hp/Downloads/755t_AdobeExpress_AdobeExpress.mp4')
        # Create a Canvas to display the video frames
        self.canvas = tk.Canvas(self.root, width=1000, height=800)
        self.canvas.pack()
        # Initialize pygame mixer
        pygame.mixer.init()
        pygame.mixer.music.load(r'C:/Users/hp/Downloads/corn-popper-with-accents-34016.mp3')  # Replace with the path to your background music file
        pygame.mixer.music.play(-1)  # Play the background music in a loop
        # Start the video playback
        self.update_video()

    def update_video(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            self.photo = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            self.root.after(20, self.update_video)  # Update every 20 milliseconds

            
if _name_ == "_main_":
    root = tk.Tk()   
    close_window = close_window(root)
    root.mainloop()