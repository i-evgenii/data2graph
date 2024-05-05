# Virtual environment
pip install virtualenv
cd C:\GitHub\
mkdir Graph-prog
cd Graph-prog
python -m venv env
env\Scripts\activate
pip install -r requirements.txt

# Activate
cd C:\GitHub\Graph-prog
env\Scripts\activate

# Deactivate
cd C:\GitHub\Graph-prog
env\Scripts\deactivate

# Start
python data2graph.py

# IDLE in venv
python -m idlelib.idle