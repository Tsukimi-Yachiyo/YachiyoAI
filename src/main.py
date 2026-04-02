import uvicorn
import api


class Service:

    def __init__(self):

        pass


def main():
    app = Service()
    uvicorn.run(api.create_app(app),
                host="0.0.0.0",
                port=5200)

if __name__ == "__main__":
    main()
