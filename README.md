# 🧬 ParGaMD GUI - Cloud-Based Molecular Dynamics Interface

A modern, cloud-based graphical user interface for setting up and configuring ParGaMD (Parallelizable Gaussian Accelerated Molecular Dynamics) simulations with WESTPA (Weighted Ensemble Simulation Toolkit).

## ✨ Features

### 🎯 **Flexible Collective Variables**
- **8 CV Types**: RMSD, Radius of Gyration, Distance, Native Contacts, Dihedral Angles, Hydrogen Bonds, Surface Area, Secondary Structure
- **Multiple CVs**: Add 1, 2, 3, or more collective variables as needed
- **Live Preview**: See CPPTRAJ commands in real-time
- **Dynamic Configuration**: Automatically generates appropriate WESTPA configurations

### 📝 **Live Code Editor**
- **Professional Editor**: Syntax highlighting for all file types
- **38 Files**: Complete ParGaMD simulation package
- **Real-time Editing**: Modify any configuration file directly in the browser
- **Instant Preview**: See changes immediately

### 📦 **Complete Package**
- **Ready-to-Run**: Download complete simulation setup
- **All Dependencies**: Includes all necessary scripts and files
- **Documentation**: Comprehensive guides and examples
- **Analysis Tools**: Python scripts for post-simulation analysis

### 🚀 **Cloud-Native**
- **Streamlit-Based**: Modern, responsive web interface
- **No Installation**: Runs entirely in the browser
- **Cross-Platform**: Works on any device with a web browser
- **Free Hosting**: Deploy on Streamlit Community Cloud

## 🎮 Quick Start

### Option 1: Use the Deployed App
Visit the live application at: `https://[app-name].streamlit.app`

### Option 2: Run Locally
```bash
# Clone the repository
git clone https://github.com/your-username/ParGaMD-GUI.git
cd ParGaMD-GUI

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py
```

## 📋 Usage Guide

### 1. **Basic Information**
- Enter your protein name
- Upload PDB and PRMTOP files
- Provide account and email information

### 2. **Weighted Ensemble Parameters**
- Set walkers per bin, maximum iterations
- Configure MD steps and print frequency
- **Select Collective Variables**:
  - Choose CV types from dropdown
  - Set min/max values and step sizes
  - See live CPPTRAJ command previews
  - Add multiple CVs as needed

### 3. **Review & Edit**
- **Live Editor**: Edit any of the 38 generated files
- **Syntax Highlighting**: Professional code editing experience
- **Real-time Updates**: Changes applied immediately

### 4. **Download**
- **Complete Package**: ZIP file with all simulation files
- **Ready to Run**: Upload to your HPC cluster and execute

## 📁 Generated Files

The application generates a complete ParGaMD simulation package:

```
📦 ParGaMD_config/
├── 📄 Configuration Files
│   ├── west.cfg              # WESTPA configuration
│   ├── env.sh                # Environment setup
│   └── run_WE.sh             # Weighted Ensemble execution
│
├── 🧬 Molecular Structure Files
│   ├── common_files/         # PDB, PRMTOP, MD inputs
│   ├── cMD/                  # Conventional MD files
│   └── bstates/              # Basis state files
│
├── 🔧 WESTPA Scripts
│   └── westpa_scripts/       # All WESTPA utilities
│
├── 📊 Analysis Tools
│   ├── simtime.py            # Simulation time analysis
│   ├── data_extract.py       # Data extraction
│   └── PyReweighting-2D.py   # 2D reweighting
│
└── 📚 Documentation
    ├── README.md
    ├── CHANGELOG.md
    └── LICENSE
```

## 🎯 Supported Collective Variables

| CV Type | Description | CPPTRAJ Command |
|---------|-------------|-----------------|
| **RMSD** | Root Mean Square Deviation | `rms ca-rmsd @CA reference` |
| **Radius of Gyration** | Protein compactness | `radgyr ca-rg @CA` |
| **Distance** | Atom pair distances | `distance :1@CA :10@CA` |
| **Native Contacts** | Contact formation | `nativecontacts :* byresidue` |
| **Dihedral** | Backbone angles | `dihedral :1@C :1@N :2@CA :2@C` |
| **H-bonds** | Hydrogen bonding | `hbond` |
| **Surface Area** | Solvent exposure | `surf :*` |
| **Secondary Structure** | Structure content | `secstruct :*` |

## 🚀 Deployment

### Streamlit Community Cloud (Recommended)
1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with one click!

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 🛠️ Technical Details

- **Framework**: Streamlit
- **Language**: Python 3.9+
- **Dependencies**: See [requirements.txt](requirements.txt)
- **File Generation**: Jinja2 templating
- **Code Editor**: streamlit-code-editor

## 📊 Features Comparison

| Feature | Flask Version | Streamlit Version |
|---------|---------------|-------------------|
| **Installation** | Local only | Cloud + Local |
| **CV Support** | Fixed 2 CVs | Flexible 1+ CVs |
| **Code Editor** | Basic | Professional |
| **File Count** | ~15 files | 38 files |
| **Deployment** | Manual | One-click |
| **Sharing** | Difficult | Public URL |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **WESTPA**: Weighted Ensemble Simulation Toolkit
- **AMBER**: Molecular dynamics software suite
- **Streamlit**: Modern web app framework
- **CPPTRAJ**: Trajectory analysis tools

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/ParGaMD-GUI/issues)
- **Documentation**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Examples**: See the generated configuration files

---

**Ready to run ParGaMD simulations?** 🚀 [Try the live app](https://pargamd-gui.streamlit.app/) or [deploy your own](DEPLOYMENT.md)!
