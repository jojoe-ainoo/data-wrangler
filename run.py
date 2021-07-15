import os



# Run Commands

# Make sure Python3 is Installed
os.system("python3 -m pip install --upgrade pip")

# Setup virtual env
os.system("python3 -m venv ven")
print("Virtual Env Setup")

# activate env
os.system(". venv/bin/activate")

# install dependencies
os.system("pip install -r requirements.txt")

# run wrangler test
os.system("python3 wrangler/test_wrangler.py")
