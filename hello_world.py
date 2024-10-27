from prefect import flow
import automl
import api

@flow(log_prints=True)
def hello_world(name: str = "world", goodbye: bool = False):
    print(f"Hello {name} from Prefect! 🤗")
    automl.main2()
    api.main4()
    if goodbye:
        print(f"Goodbye {name}!")


if __name__ == "__main__":
    hello_world.serve(name="hackathon",
                      tags=["onboarding"],
                      parameters={"goodbye": True},
                      interval=60)
