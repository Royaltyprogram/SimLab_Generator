# 🧪 SIMLAB_GENERATOR

<div align="center">

[![Main Repo](https://img.shields.io/badge/Main_Repo-SimLab-black?style=flat&logo=github)](https://github.com/Royaltyprogram/SimLab)
[![Simulation Archive](https://img.shields.io/badge/Archive-Simulations-blue?style=flat&logo=github)](https://github.com/Royaltyprogram/SimLab_simualtions)
[![Website](https://img.shields.io/badge/website-simlab.info-blue?style=flat&logo=internet-explorer)](https://simlabapp.com)
[![Twitter Follow](https://img.shields.io/badge/follow-%40SimLab__official-1DA1F2?logo=twitter&style=flat)](https://twitter.com/sim_lab)

![Python](https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40.2-FF4B4B?style=for-the-badge&logo=streamlit)
![OpenAI](https://img.shields.io/badge/OpenAI-1.56.0-412991?style=for-the-badge&logo=openai)

</div>

## 📌 Overview
SIMLAB_GENERATOR is a Python-based application that provides an innovative graphical user interface for simulation and laboratory tasks.

## 🚀 Quick Start

### Prerequisites
- Python 3.x
- pip (Python package installer)

### Installation

1️⃣ **Clone the repository**
```bash
git clone https://github.com/[your-username]/SIMLAB_GENERATOR.git
cd SIMLAB_GENERATOR
```

2️⃣ **Install dependencies**

You have several options for installing the required dependencies:

**Option 1: Using requirements.txt (Recommended)**
```bash
pip install -r requirements.txt
```

**Option 2: Manual Installation**
If you encounter any issues with requirements.txt, you can install packages individually:
```bash
# Install Streamlit
pip install streamlit

# Install OpenAI and Anthropic packages
pip install openai anthropic
```

> **Note**: If you encounter any permission errors during installation, try:
> ```bash
> pip install --user -r requirements.txt
> # or
> pip install --user streamlit openai anthropic
> ```

3️⃣ **Run the application**
```bash
streamlit run main/innovate_gui.py
```

After running the application, you can enter your OpenAI and Anthropic API keys directly in the Streamlit user interface.

## 📁 Project Structure
```
SIMLAB_GENERATOR/
├── main/
│   ├── api_calls.py          # API integration
│   ├── innovate_gui.py       # Main GUI interface
│   └── time_to_innovate.py   # Core functionality
├── .gitattributes
├── .gitignore
└── requirements.txt          # Project dependencies
```

## 🔧 Configuration
Before running the application, make sure you have all the required dependencies installed using the `requirements.txt` file. If you face any dependency conflicts, try creating a virtual environment:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## 🤝 Contributing
Contributions are always welcome! Please feel free to submit a Pull Request.

## 📫 Contact
- GitHub: https://github.com/Royaltyprogram/SimLab_simualtions
- Email: edulens43@gmail.com

---
