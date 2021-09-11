from guizero import App, Text, TextBox, PushButton

def say_my_name():
    welcome_message.value = my_name.value

app = App(title="Hello world")

welcome_message = Text(app, text="Welcome to my app", size=40, font="Times New Roman", color="lightblue")
my_name = TextBox(app, text="Type here", width=100)
update_text = PushButton(app, command=say_my_name, text="Display my name")

app.display()