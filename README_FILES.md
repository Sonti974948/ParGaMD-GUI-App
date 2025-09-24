# ParGaMD GUI - Files Directory

This directory contains all the necessary files for the ParGaMD Streamlit cloud application.

## 📁 File Structure

### Core Application Files
- `streamlit_app.py` - Main Streamlit application
- `config_generator.py` - Configuration file generator
- `requirements.txt` - Python dependencies for cloud deployment

### Documentation
- `README.md` - Main project documentation
- `README_STREAMLIT.md` - Streamlit-specific documentation
- `DEPLOYMENT.md` - Cloud deployment instructions
- `CHANGELOG.md` - Version history
- `LICENSE` - MIT License

### HPC System Templates
- `env.sh` - Expanse (SDSC) environment template
- `env_HPC2.sh` - HPC2 (UCD) environment template
- `run_WE.sh` - Expanse run script template
- `run_WE_HPC2.sh` - HPC2 run script template
- `TACC_files/` - TACC Frontera templates

### ParGaMD Configuration
- `west.cfg` - WESTPA configuration template
- `westpa_scripts/` - WESTPA execution scripts
- `bstates/` - Basis state files
- `common_files/` - Common molecular dynamics files
- `cMD/` - Conventional MD files

### Utility Scripts
- `simtime.py` - Simulation time analysis
- `data_extract.py` - Data extraction utilities
- `PyReweighting-2D.py` - 2D reweighting script
- `quick_start.py` - Quick start utility
- `*.sh` - Shell execution scripts
- `nodefilelist.txt` - Node management file
- `tstate.file` - State file

## 🚀 Deployment

These files are ready for deployment to Streamlit Community Cloud. The application supports:

- **Expanse (SDSC)** - Default configuration
- **TACC Frontera** - TACC-specific setup
- **HPC2 (UCD)** - UCD cluster configuration

## 🔧 Features

- Multi-step configuration wizard
- HPC system selection
- Live code editor with syntax highlighting
- Multi-CV support (RMSD, Radius of Gyration, Distance, etc.)
- Custom CV support
- File upload (PDB, INPCRD, PRMTOP, RST)
- Complete bundle download
- Real-time configuration preview

## 📋 Requirements

- Python 3.7+
- Streamlit >= 1.28.0
- Jinja2 >= 3.1.2
- streamlit_code_editor >= 0.1.22

## 🌐 Live Demo

Access the live application at: [https://pargamd-gui.streamlit.app/](https://pargamd-gui.streamlit.app/)

## 📞 Support

For issues or questions, please create an issue on the GitHub repository.
