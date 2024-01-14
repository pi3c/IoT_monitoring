import sys
from src.app import demo_test


if __name__ == "__main__":
    if "--demo" in sys.argv:
        demo_test()

    if "--run-server" in sys.argv:
        pass
