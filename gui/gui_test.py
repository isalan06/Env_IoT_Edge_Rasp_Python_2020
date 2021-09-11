from guizero import App, Text, TextBox, PushButton, Slider, Picture

def say_my_name():
    welcome_message.value = my_name.value

def change_text_size(slider_value):
    welcome_message.size = slider_value

def close_app():
    app.destroy()

def close_app2():
    app2.destroy()

app = App(title="Hello world")

welcome_message = Text(app, text="Welcome to my app", size=40, font="Times New Roman", color="lightblue")
my_name = TextBox(app, text="Type here", width=100)
update_text = PushButton(app, command=say_my_name, text="Display my name")
close_text = PushButton(app, command=close_app, text="Close")
text_size = Slider(app, command=change_text_size, start = 10, end=80)
my_cat = Picture(app, image="test.jpg", width=200, height = 100)

app.display()

app2 = App(title="My second GUI app", width=300, height = 200)

close_text2 = PushButton(app2, command=close_app2, text="Close")

app2.full_screen = True
app2.display()