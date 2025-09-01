import getpass
import os


os.environ["GITHUB_TOKEN"]=getpass.getpass("Enter your GitHub token: ")
os.environ["ACTIVELOOP_TOKEN"]=getpass.getpass("Enter your ActiveLoop token: ")
os.environ["OPENAI_API_KEY"]=getpass.getpass("Enter your OpenAI API key: ")
DATASET_PATH="hub://YOUR_ORG/repository_vector_store"