from IPython.display import display, Image

def start_agent(app):
    try:
        display(Image(app.get_graph(xray = True).draw_png()))
    except Exception as ex:
        print(ex)
