import os.path
from customtkinter import*
from tkinter import filedialog
from PIL import Image
import json
import base64
import io

foto1=Image.open('../images/завантаження.jpg')
foto_base=CTkImage
file_name = None
x_print_mes=10

class Window(CTk):
    def __init__(self):
        super().__init__()
        self.geometry('800x700')
        self.maxsize(width=800,height=700)
        self.title('Logitalk')
        self.show_menu = False
        self._set_appearance_mode('light')
        self.image_path=None
        self.sent_image=None
        self.labels=[]
        self.bg_labels=[]
        self.messages=[]

        self.board_w=730
        self.board_h=635
        self.board = CTkScrollableFrame(self, width=self.board_w, height=self.board_h,fg_color='#F0F8FF')
        self.board.place(x=45, y=0)
        self.bind("<Configure>", self.resize_board)
        self.after(10,self.resize_board)

        self.frame = CTkFrame(self, fg_color='lightblue')
        self.frame.configure(width=0)
        self.frame_width = 0
        self.frame.place(x=0, y=0)

        base_foto = CTkImage(light_image=foto1, size=(60, 60))

        self.set_foto=CTkButton(self.frame,hover_color='white',height=60,width=60,text='',fg_color='transparent',image=base_foto,command=self.load_foto)
        self.set_foto.place(x=60,y=40)

        self.label = CTkLabel(self.frame, text="Введіть ім'я", text_color='black', font=('Times New Roman', 15))
        self.label.place(x=60, y=120)

        self.entery = CTkEntry(self.frame, width=150, height=30,fg_color='#F0F8FF',text_color='black')
        self.entery.place(x=25, y=150)

        self.save_name=CTkButton(self.frame,width=150, height=30,text='Зберегти',command=self.save_all)
        self.save_name.place(x=25,y=200)

        self.option_menu = CTkOptionMenu(self.frame, fg_color='blue', dropdown_hover_color='blue', button_color='blue',
                                         values=['Світла тема', "Темна тема"], command=self.change_mode)
        self.option_menu.place(x=25, y=self.save_name.winfo_y()+100)

        self.open_btn = CTkButton(self, width=30, height=30, text='⚙️', command=self.for_open_btn)
        self.open_btn.place(x=10, y=10)

        self.print_mes = CTkEntry(self, height=30,width=605,placeholder_text='Введіть повідомлення...',fg_color='#F0F8FF',bg_color='white',text_color='black')
        self.print_mes.place(x=40, rely=1.0, anchor="sw", y=-10)

        self.bind("<Configure>", self.resize_entry)
        self.after(10,self.resize_entry)

        self.send = CTkButton(self, text="Надіслати", width=120, height=30,command=self.send_mes,bg_color='transparent')
        self.send.place(relx=1.0, rely=1.0, anchor="se", y=-10)

        self.image_button = CTkButton(self, text="📷", width=30,height=30, command=self.open_image)
        self.image_button.place(x=680, rely=1.0, anchor="se", y=-10)

        self.load_data()
        self.load_messages_from_json()
    def resize_entry(self, event=None):
        left_margin_default = 45
        if self.show_menu:
            left_margin = 205
        else:
            left_margin = left_margin_default

        self.print_mes.place(x=left_margin, rely=1.0, anchor="sw", y=-10)

    def resize_board(self,event=None):
        left_margin_default = 45
        left_margin = 205 if self.show_menu else left_margin_default
        self.board.place(x=left_margin, y=5)

    def open_menu(self):
        if self.frame_width <= 200:
            self.frame_width += 5
            self.frame.configure(width=self.frame_width, height=self.winfo_height())
        if self.show_menu:
            self.after(10, self.open_menu)

    def close_menu(self):
        if self.frame_width >= 0:
            self.frame_width -= 5
            self.frame.configure(width=self.frame_width, height=self.winfo_height())
        if not self.show_menu:
            self.after(10, self.close_menu)

    def for_open_btn(self):
        if not self.show_menu:
            self.show_menu = True
            self.open_menu()
        else:
            self.show_menu = False
            self.close_menu()

    def send_mes(self, custom_message=None, img=None):
        name = self.entery.get()
        message = custom_message if custom_message else self.print_mes.get()
        if not message.strip() and not img:
            return  # не надсилаємо порожнє

        if self.option_menu.get() == 'Світла тема':
            fg_color = 'lightgrey'
            text_color = 'black'
        else:
            fg_color = '#333333'
            text_color = 'white'

        bg = CTkFrame(self.board, corner_radius=10, fg_color=fg_color)
        bg.pack(fill="x", padx=10, pady=5, anchor="w")
        if hasattr(self, "image_path") and self.image_path:
            avatar_img = CTkImage(light_image=Image.open(self.image_path), size=(30, 30))
            avatar = CTkLabel(bg, image=avatar_img, text="")
            avatar.image = avatar_img
            avatar.pack(side="left", padx=5)

        if message.strip():
            new_label = CTkLabel(bg, text=f"{name}: {message}", anchor="w", justify="left", text_color=text_color)
            new_label.pack(fill="x", padx=10, pady=5)
            self.labels.append(new_label)
            self.save_message_to_json({'type':'text','text':message})
        if img:
            image_label = CTkLabel(bg, image=img, text="")
            image_label.image = img
            image_label.pack(padx=10, pady=5)
        self.bg_labels.append(bg)

        if not custom_message:
            self.print_mes.delete(0, 'end')
    def change_mode(self, choice):
        if choice == 'Світла тема':
            self.frame.configure(fg_color='lightblue')
            self.label.configure(text_color='black')
            self.option_menu.configure(fg_color='blue', button_color='blue')
            self._set_appearance_mode('light')
            self.board.configure(fg_color='#F0F8FF')
            self.print_mes.configure(fg_color='#F0F8FF', bg_color='#F0F8FF', text_color='black')
            self.entery.configure(fg_color='#F0F8FF', text_color='black')
            for bg in self.bg_labels:
                bg.configure(fg_color='lightgrey')
            for label in self.labels:
                label.configure(text_color='black')

        if choice == 'Темна тема':
            self.frame.configure(fg_color='dodgerblue')
            self.label.configure(text_color='white')
            self.option_menu.configure(fg_color='darkblue', button_color='darkblue')
            self._set_appearance_mode('dark')
            self.board.configure(fg_color='#191970')
            self.print_mes.configure(fg_color='#191970', bg_color='black', text_color='white')
            self.entery.configure(fg_color='#191970', text_color='white')
            for bg in self.bg_labels:
                bg.configure(fg_color='#333333')
            for label in self.labels:
                label.configure(text_color='white')

    def load_foto(self):
        file_path = filedialog.askopenfilename(filetypes=[("Зображення", "*.png *.jpg *.jpeg")])
        if file_path:
            self.image_path=file_path
            image = Image.open(file_path)
            image = image.resize((60, 60))
            new_image = CTkImage(light_image=image, size=(60, 60))
            self.set_foto.configure(image=new_image)
            self.set_foto.image = new_image

    def save_all(self):
        username=self.entery.get()
        if self.image_path:
            data={'username':username,'image':self.image_path}
            with open('user_data.json','w',encoding='utf-8') as f:
                json.dump(data,f,ensure_ascii=False,indent=4)
    def load_data(self):
        try:
            with open('user_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.entery.insert(0, data.get('username', ''))
                image_path = data.get('image')
                if image_path:
                    self.image_path = image_path
                    image = Image.open(image_path).resize((60, 60))
                    img = CTkImage(light_image=image, size=(60, 60))
                    self.set_foto.configure(image=img, text='')
                    self.set_foto.image = img
        except Exception as e:
            print('Error loading user data:', e)

    def save_message_to_json(self, entry):
        try:
            with open('messages.json', 'r', encoding='utf-8') as f:
                messages = json.load(f)
        except FileNotFoundError:
            messages = []
        messages.append(entry)
        with open('messages.json', 'w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False, indent=4)

    def load_messages_from_json(self):
        try:
            with open('messages.json', 'r', encoding='utf-8') as f:
                messages = json.load(f)
                for msg in messages:
                    if msg['type'] == 'text':
                        self.display_message(message=f"{msg['text']}")
                    elif msg['type'] == 'image':
                        pil_img = Image.open(msg['image'])
                        ctk = CTkImage(light_image=pil_img, size=(300, 300))
                        self.display_message( img=ctk)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Помилка при завантаженні повідомлень: {e}")

    def open_image(self):
        file_path=filedialog.askopenfilename(filetypes=[("Зображення", "*.png *.jpg *.jpeg")])
        if not file_path:
            return
        try:
            with open(file_path,'rb') as f:
                raw=f.read()
                pil_img = Image.open(io.BytesIO(raw))
                ctk_img = CTkImage(light_image=pil_img, size=(300, 300))
                self.send_mes(custom_message=None, img=ctk_img)
        except Exception as e:
            self.send_mes(f'Не вдалося надіслати зображення{e}')

        self.save_message_to_json({'type': 'image', 'image': file_path})

    def display_message(self, message=None, img=None):
        name = self.entery.get()
        if self.option_menu.get() == 'Світла тема':
            fg_color = 'lightgrey'
            text_color = 'black'
        else:
            fg_color = '#333333'
            text_color = 'white'

        bg = CTkFrame(self.board, corner_radius=10, fg_color=fg_color)
        bg.pack(fill="x", padx=10, pady=5, anchor="w")

        if self.image_path:
            avatar_img = CTkImage(light_image=Image.open(self.image_path), size=(30, 30))
            avatar = CTkLabel(bg, image=avatar_img, text="")
            avatar.image = avatar_img
            avatar.pack(side="left", padx=5)

        if message:
            label = CTkLabel(bg, text=f"{name}: {message}", anchor="w", justify="left", text_color=text_color)
            label.pack(fill="x", padx=10, pady=5)
            self.labels.append(label)

        if img:
            label_img = CTkLabel(bg, image=img, text="")
            label_img.image = img
            label_img.pack(padx=10, pady=5)
            self.labels.append(label_img)

        self.bg_labels.append(bg)
win = Window()
win.mainloop()


