import os
import sys

current_dir = os.path.dirname(__file__)

parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(parent_dir)
from routes.indexing import submit_urls

if __name__ == "__main__":
    submit_urls()
