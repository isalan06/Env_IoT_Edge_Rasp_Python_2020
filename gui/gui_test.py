from guizero import App, Text, TextBox, PushButton, Slider, Picture, Window, Combo

def say_my_name():
    welcome_message.value = my_name.value

def change_text_size(slider_value):
    welcome_message.size = slider_value

def close_app():
    app.destroy()

def close_app2():
    app2.destroy()

def show_window():
    window.show()

def hide_window():
    window.hide()

print("Start")

app = App(title="Hello world")

window = Window(app, title="2nd Window")
window.hide()


welcome_message = Text(app, text="Welcome to my app", size=40, font="Times New Roman", color="lightblue")
my_name = TextBox(app, text="Type here", width=100)
update_text = PushButton(app, command=say_my_name, text="Display my name")
show_text = PushButton(app, command=show_window, text="Popup Window")
close_text = PushButton(app, command=close_app, text="Close")
text_size = Slider(app, command=change_text_size, start = 10, end=80)
my_cat = Picture(app, image="/home/pi/Pictures/testshow.jpg", width=200, height = 100)

hide_test = PushButton(window, command="hide_window", text="Close")

app.display()

app2 = App(title="My second GUI app", width=300, height = 200, layout="grid")
app2.set_full_screen('Esc')

close_text2 = PushButton(app2, command=close_app2, text="Close", grid=[0,0])
film_description = Text(app2, text="Which film?", grid=[0,1], align="left")
film_choice = Combo(app2, options=["Start Wars", "Frozen", "Lion King"], grid=[1,1], align="left")


#app2.full_screen = True
app2.display()

print("Finish")

