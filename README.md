# Project Goals App

A simple Streamlit web app to capture and visualize project goals using a hierarchical network structure.

## 🚀 Features

- Add, edit, and delete goals with status and comments
- Visualize goal networks in 2D (Pyvis) and 3D (Plotly)
- Status tracking using traffic light colors: red, yellow, green
- Export and import goal networks as JSON

## 🛠 Installation

```bash
git clone https://github.com/your-username/project-goals.git
cd project-goals
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The app will be available at `http://localhost:8501`.



## 📁 Project Structure

```
project-goals/
├── app.py                      # Entry point and routing
├── sidebar/
│   └── menu.py                 # Sidebar UI and workflow selector
├── project_assessment/
│   ├── gui.py                  # Main GUI logic
│   ├── goals_input.py          # Text input and JSON import
│   ├── editor.py               # Goal editing UI
│   ├── analysis.py             # KPI and rule-based analysis
│   ├── visual.py               # 2D/3D visualization UI
│   └── helper/
│       ├── tree_builder.py     # Convert text to goal tree
│       ├── data_model.py       # Node model and status choices
│       ├── data_store.py       # Load/save goal trees
│       ├── summarizer.py       # Rule-based summary
│       └── recommendations.py  # Generate rule-based recommendations
├── visualization/
│   ├── visualizer2d.py         # Pyvis rendering
│   └── visualizer3d.py         # Plotly rendering
└── requirements.txt            # Python dependencies
```

## 📄 License

MIT License
