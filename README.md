# ParGaMD GUI - Streamlit Cloud Application

A modern cloud-based graphical user interface for setting up and configuring ParGaMD (Parallelizable Gaussian Accelerated Molecular Dynamics) experiments. This Streamlit application streamlines the process of configuring molecular dynamics simulations by providing an intuitive interface for parameter management and configuration file generation.

## 🌐 Live Demo

**Access the live application**: [https://pargamd-gui.streamlit.app/](https://pargamd-gui.streamlit.app/)

## 🚀 Features

### Core Functionality
- **Multi-Step Configuration Wizard**: Guided setup process with 6 clear steps
- **HPC System Support**: Configure for Expanse (SDSC), TACC Frontera, or HPC2 (UCD)
- **Dynamic Configuration Generation**: Automatically generate all required configuration files with proper formatting
- **Live Code Editor**: Edit generated configuration files directly in the browser with syntax highlighting
- **Complete Bundle Export**: Download all necessary files and directories as a ZIP archive
- **Multi-CV Support**: Add multiple Collective Variables (CVs) for enhanced analysis

### HPC System Support
- **Expanse (SDSC)**: Default configuration with Expanse-specific SLURM headers and module loads
- **TACC Frontera**: TACC-specific configuration with `#SBATCH -A` and `ml` commands
- **HPC2 (UCD)**: UCD cluster configuration with `--partition=gpu-ahn` and specific module loads

### Parameter Management
- **Flexible CV Configuration**: Support for RMSD, Radius of Gyration, Distance, Native Contacts, Dihedral Angles, Hydrogen Bonds, Surface Area, Secondary Structure, and Custom CVs
- **Custom CV Support**: Define your own collective variables with custom names
- **Infinite Bounds Support**: Optional inclusion of `-inf` and `inf` as outer bin boundaries
- **GPU Parallelization Control**: Toggle multi-GPU parallelization features
- **File Upload**: Upload PDB, INPCRD, PRMTOP, and RST files with flexible placement options
- **WE Parameters**: Configure bin target counts, maximum iterations, and MD parameters

### Generated Files
The application generates the following configuration files:
- `west.cfg` - WESTPA configuration with dynamic bin boundaries
- `env.sh` - Environment setup (HPC-specific)
- `runseg.sh` - Segment execution script with CPPTRAJ commands
- `get_pcoord.sh` - Progress coordinate calculation for initial states
- `run_cmd.sh` - Conventional MD execution script
- `run_WE.sh` - Weighted Ensemble execution script (HPC-specific)

### Included Directories
The ZIP export includes complete directory structure:
- `cMD/` - Conventional MD files and scripts
- `common_files/` - Shared files and templates
- `bstates/` - Basis state files
- `westpa_scripts/` - WESTPA execution scripts
- Documentation and utility scripts

## 📋 Prerequisites

- Modern web browser (Chrome, Firefox, Safari, Edge)
- No local installation required - runs entirely in the cloud!

## 🛠️ Local Development (Optional)

If you want to run the application locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Sonti974948/ParGaMD-GUI.git
   cd ParGaMD-GUI
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Access the GUI**:
   Open your web browser and navigate to `http://localhost:8501`

## 🎯 Usage Guide

### Step 1: System Setup
- **HPC System Selection**: Choose from Expanse, TACC Frontera, or HPC2
- **SLURM Account**: Enter your allocation account name
- **Email**: Provide email for job notifications

### Step 2: Molecular System
- **Protein Name**: Enter name for file naming
- **Structure File**: Upload either PDB or INPCRD file (one required)
- **Topology File**: Upload PRMTOP file (required)
- **Optional RST File**: Upload restart file and choose placement (bstates or cMD folder)

### Step 3: Weighted Ensemble Parameters
- **Collective Variables**: Add multiple CVs with custom parameters
- **CV Types**: RMSD, Radius of Gyration, Distance, Native Contacts, Dihedral, Hydrogen Bonds, Surface Area, Secondary Structure, or Custom
- **Custom CVs**: Define your own CVs with custom names and implementation guidance
- **Basic Parameters**: Set walkers per bin, maximum iterations, MD steps, print frequency
- **Advanced Options**: Include infinite bounds for proper boundary handling

### Step 4: GPU Options
- **Multi-GPU Parallelization**: Enable or disable multi-GPU features
- Automatic code commenting for single-GPU compatibility

### Step 5: Review & Edit
- **Live Code Editor**: Edit any generated configuration file with syntax highlighting
- **File Selection**: Choose from all generated files (binary files excluded)
- **Apply Changes**: Modify files and apply changes in real-time
- **Reset Options**: Reset files to original generated state

### Step 6: Download
- **Complete Bundle**: Download all files as a ZIP archive
- **File Summary**: View text and binary files included
- **Content Preview**: Preview all text files before download

## 📁 Project Structure

```
ParGaMD-GUI/
├── streamlit_app.py          # Main Streamlit application
├── config_generator.py       # Configuration file generator
├── requirements.txt          # Python dependencies
├── env.sh                   # Expanse environment template
├── env_HPC2.sh             # HPC2 environment template
├── run_WE.sh               # Expanse run script template
├── run_WE_HPC2.sh          # HPC2 run script template
├── TACC_files/             # TACC Frontera templates
├── westpa_scripts/         # WESTPA execution scripts
├── bstates/                # Basis state files
├── common_files/           # Common molecular dynamics files
├── cMD/                    # Conventional MD files
├── README.md               # This documentation
├── README_STREAMLIT.md     # Streamlit-specific documentation
├── DEPLOYMENT.md           # Deployment instructions
└── CHANGELOG.md            # Version history
```

## 🔧 Configuration Details

### HPC-Specific Templates
- **Expanse**: Uses `#SBATCH --partition=gpu-shared` and standard module loads
- **TACC Frontera**: Uses `#SBATCH -p rtx` and `ml` commands with TACC-specific paths
- **HPC2**: Uses `#SBATCH --partition=gpu-ahn` and UCD-specific module loads

### west.cfg
- Dynamic bin boundaries based on user input
- Configurable progress coordinate dimensionality
- Automatic pcoord_len calculation based on MD parameters
- Support for infinite bounds to prevent simulation errors

### env.sh
- HPC-specific module loads and environment setup
- Dynamic NODELOC setting
- Complete environment setup for AMBER/WESTPA
- All necessary PATH and environment variable exports

### runseg.sh & get_pcoord.sh
- Dynamic CPPTRAJ command generation based on selected CVs
- Conditional reference file selection (PDB vs INPCRD)
- Proper progress coordinate extraction and formatting
- Multi-CV support with paste commands for combined outputs

### run_WE.sh
- HPC-specific SLURM job submission scripts
- ZMQ-based parallel execution setup
- Node management and communication
- HPC-specific module loads and environment setup

## 🚨 Troubleshooting

### Common Issues

1. **Code Editor Not Loading**:
   - Ensure you're using a modern browser
   - Try refreshing the page
   - Check browser console for JavaScript errors

2. **File Upload Issues**:
   - Ensure files are valid PDB/PRMTOP/INPCRD/RST format
   - Check file size limits (typically 200MB max)
   - Verify file permissions

3. **Configuration Generation Errors**:
   - Ensure all required fields are filled
   - Check that at least one CV is configured
   - Verify protein name doesn't contain special characters

4. **Download Issues**:
   - Ensure all parameters are configured
   - Try regenerating configurations
   - Check browser download settings

### Debug Information
The application includes debug expanders that show:
- Number of generated files
- File names and types
- Form data and uploaded files
- Configuration summary

## 🌐 Cloud Deployment

This application is deployed on **Streamlit Community Cloud** and automatically updates when changes are pushed to the main branch of the GitHub repository.

### Deployment Features
- **Automatic Updates**: Changes pushed to GitHub automatically deploy
- **No Server Management**: Fully managed cloud infrastructure
- **Global Access**: Accessible from anywhere with internet connection
- **Free Hosting**: No cost for public repositories

## 📚 Citation

If you use this tool in your research, please cite:

```bibtex
@article{sonti2025accelerating,
  title={Accelerating free energy exploration using parallelizable Gaussian accelerated molecular dynamics (ParGaMD)},
  author={Sonti, Siddharth and Thyagatur, Anugraha and Wan, Hung-Yu and Hamelynck, Maxen and Faller, Roland and Ahn, Surl-Hee},
  year={2025}
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **ParGaMD**: Parallelizable Gaussian Accelerated Molecular Dynamics framework
- **WESTPA**: Weighted Ensemble Simulation Toolkit
- **AMBER**: Assisted Model Building with Energy Refinement
- **Streamlit**: Modern Python web framework for data applications
- **Streamlit Community Cloud**: Free hosting platform

## 📞 Support

For issues, questions, or contributions:
- Create an issue on GitHub
- Contact the development team

## 🔄 Version History

- **v1.0.0**: Initial Flask release with basic ParGaMD configuration
- **v2.0.0**: Complete rewrite as Streamlit cloud application
- **v2.1.0**: Added multi-CV support and live code editor
- **v2.2.0**: Added HPC system selection (Expanse, TACC, HPC2)
- **v2.3.0**: Enhanced file upload options (PDB/INPCRD, RST placement)
- **v2.4.0**: Added custom CV support and improved UI

---

**Note**: This GUI is designed to work with ParGaMD simulations and requires proper setup of AMBER, WESTPA, and related dependencies on your target HPC cluster. The generated configuration files are optimized for the selected HPC system.