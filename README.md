# Virtual environment
pip install virtualenv
cd C:\GitHub\
git clone https://github.com/i-evgenii/data2graph.git
cd data2graph
python -m venv env
env\Scripts\activate
pip install -r requirements.txt

# Activate
cd C:\GitHub\data2graph
env\Scripts\activate

# Deactivate
cd C:\GitHub\data2graph
env\Scripts\deactivate

# Start
python data2graph.py

# IDLE in venv
python -m idlelib.idle