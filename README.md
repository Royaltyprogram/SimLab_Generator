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

SIMLAB_GENERATOR is a Python-based application that provides an innovative graphical user interface for simulation and laboratory tasks. It leverages the power of multiple AI models to generate and refine scientific simulations through an interactive process.

## 🔄 Process Flow

### 1. Main Process
```mermaid
flowchart TB
    Start([Launch Streamlit App]) --> ApiKeys[Enter API Keys]
    ApiKeys --> Prompt[Enter Simulation Prompt]
    Prompt --> Research[Initial Research Phase]
    Research --> Code[Code Generation Phase]
    Code --> Refine[Code Refinement Phase]
    Refine --> Review[Final Review Phase]
    Review --> Save[Save Results]
    Save --> End([End])

    style Start fill:#f9f9f9,stroke:#333
    style End fill:#f9f9f9,stroke:#333
    style Research fill:#FFE6E6,stroke:#FF9999
    style Code fill:#E6F3FF,stroke:#99CCFF
    style Refine fill:#FFE6E6,stroke:#FF9999
    style Review fill:#E6F3FF,stroke:#99CCFF
```

### 2. Research Phase
```mermaid
flowchart TB
    subgraph ResearchPhase [Research Phase - Qwen/Qwen2.5-72B-Instruct]
        direction TB
        Start([Start Research]) --> Analysis[Analyze Requirements]
        Analysis --> Libraries[Identify Required Libraries]
        Libraries --> Methods[Define Implementation Methods]
        Methods --> Tech[Select Technologies]
        Tech --> Plan[Create Implementation Plan]
        Plan --> End([Complete Research])
    end

    style ResearchPhase fill:#FFE6E6,stroke:#FF9999
    style Start fill:#f9f9f9,stroke:#333
    style End fill:#f9f9f9,stroke:#333
```

### 3. Code Generation and Refinement
```mermaid
flowchart TB
    subgraph InitialCode [Initial Code - Claude-3.5-sonnet]
        direction TB
        Start([Start Generation]) --> Base[Generate Base Code]
        Base --> Doc[Create Documentation]
        Doc --> Suggest[Suggest Improvements]
    end

    subgraph Refinement [Code Refinement - Qwen/Qwen2.5-Coder-32B-Instruct]
        direction TB
        Iter1[1st Iteration<br>Basic Functionality] --> Iter2[2nd Iteration<br>Performance]
        Iter2 --> Iter3[3rd Iteration<br>UX Enhancement]
    end

    InitialCode --> Refinement

    style InitialCode fill:#E6F3FF,stroke:#99CCFF
    style Refinement fill:#FFE6E6,stroke:#FF9999
    style Start fill:#f9f9f9,stroke:#333
```

### 4. Final Review Phase
```mermaid
flowchart TB
    subgraph FinalReview [Final Review - Claude-3.5-sonnet]
        Start([Start Review]) --> CodeReview[Review Code]
        CodeReview --> Check{Error Check}
        Check -->|Errors Found| Fix[Fix Errors]
        Fix --> Check
        Check -->|No Errors| Validate[Validate Code]
        Validate --> Final[Generate Final Version]
        Final --> Save[Save Results]
        Save --> End([Complete Review])
    end

    style FinalReview fill:#E6F3FF,stroke:#99CCFF
    style Start fill:#f9f9f9,stroke:#333
    style End fill:#f9f9f9,stroke:#333
    style Check fill:#f0f0f0,stroke:#333
```

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
