from guizero import App, Text

app = App(title="Hello world")

welcome_message = Text(app, text="Welcome to my app", size=40, font="Times New Roman", color="lightblue")
my_name = TextBox(app, width=100)

app.display()