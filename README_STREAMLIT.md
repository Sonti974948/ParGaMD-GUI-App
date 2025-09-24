# ParGaMD Streamlit GUI

A modern cloud-based web interface for configuring ParGaMD (Parallelizable Gaussian Accelerated Molecular Dynamics) simulations using Streamlit.

## 🚀 Features

### ✨ **Enhanced User Experience**
- **Multi-step Wizard**: Intuitive 6-step configuration process
- **Live Code Editor**: Edit configuration files directly in the browser with syntax highlighting
- **Real-time Preview**: See changes instantly as you edit
- **Drag & Drop File Upload**: Easy PDB and PRMTOP file handling
- **Advanced Dropdowns**: Smart parameter selection with dependencies

### 🔧 **Core Functionality**
- **Dynamic Configuration Generation**: Automatically generates all required ParGaMD files
- **GPU Parallelization Control**: Toggle multi-GPU support with a single click
- **Progress Coordinate Setup**: Configure RMSD and Radius of Gyration boundaries
- **Infinite Bounds Support**: Optional `-inf` and `inf` boundaries to prevent errors
- **ZIP Export**: Download complete configuration bundles

### 📁 **Generated Files**
- `west.cfg` - WESTPA configuration with dynamic bin boundaries
- `env.sh` - Environment setup script
- `westpa_scripts/runseg.sh` - Segment execution script
- `cMD/run_cmd.sh` - Conventional MD execution script
- `run_we.sh` - Weighted Ensemble execution script

## 🛠️ Installation & Usage

### Local Development
```bash
# Clone the repository
git clone <repository-url>
cd pargamd-streamlit

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run streamlit_app.py
```

### Cloud Deployment (Streamlit Community Cloud)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with one click!

## 📋 Usage Guide

### Step 1: System Setup
- Enter your SLURM account information
- Provide email for notifications

### Step 2: Molecular System
- Enter protein name (e.g., "chignolin")
- Upload PDB and PRMTOP files using drag & drop

### Step 3: WE Parameters
- Configure walkers per bin (default: 4)
- Set maximum iterations (default: 1000)
- Define MD steps and print frequency
- Set up progress coordinates (RMSD and Rg)

### Step 4: GPU Options
- Toggle multi-GPU parallelization
- Single-GPU mode comments out parallelization code

### Step 5: Review & Edit ⭐ **NEW FEATURE**
- **Live Editor**: Edit any configuration file directly
- **Syntax Highlighting**: YAML for .cfg files, Bash for .sh files
- **Apply Changes**: Save edits instantly
- **Reset to Original**: Restore original generated content

### Step 6: Download
- Download complete ZIP bundle
- View all generated files
- Start new configuration

## 🆕 **New Features vs Flask Version**

### ✅ **Added Features**
- **Live Code Editor**: Edit configuration files directly in the browser
- **Advanced Dropdowns**: Smart parameter selection
- **Better File Handling**: Drag & drop with validation
- **Real-time Updates**: Instant feedback and preview
- **Cloud Ready**: Easy deployment to Streamlit Community Cloud

### ❌ **Removed Features**
- SSH connectivity (not needed for cloud deployment)
- Remote job submission (focus on configuration generation)
- WebSocket real-time updates (replaced with Streamlit's native updates)

## 🔧 **Technical Details**

### **Architecture**
- **Frontend**: Streamlit native components
- **Backend**: Python with Jinja2 templating
- **Configuration**: Extracted from Flask version
- **File Handling**: Streamlit file uploader
- **Editor**: Streamlit's built-in code editor

### **Key Components**
- `streamlit_app.py` - Main application (400+ lines)
- `config_generator.py` - Configuration generation logic
- Session state management for multi-step forms
- Live code editor with syntax highlighting

## 🌐 **Deployment Options**

### Streamlit Community Cloud (Recommended)
- **Free tier available**
- **One-click deployment**
- **Automatic updates from GitHub**
- **Custom domain support**

### Other Cloud Platforms
- **Heroku**: Container deployment
- **AWS/GCP/Azure**: Container services
- **Railway/Render**: Easy deployment

## 📊 **Comparison with Flask Version**

| Feature | Flask Version | Streamlit Version |
|---------|---------------|-------------------|
| **Setup Complexity** | High | Low |
| **Deployment** | Manual | One-click |
| **Live Editing** | No | ✅ Yes |
| **File Handling** | Complex | Simple |
| **Maintenance** | High | Low |
| **Cloud Ready** | No | ✅ Yes |
| **Real-time Updates** | WebSocket | Native |

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally with `streamlit run streamlit_app.py`
5. Submit a pull request

## 📝 **License**

This project is licensed under the MIT License.

## 🙏 **Acknowledgments**

- **ParGaMD**: Parallelizable Gaussian Accelerated Molecular Dynamics framework
- **WESTPA**: Weighted Ensemble Simulation Toolkit
- **AMBER**: Assisted Model Building with Energy Refinement
- **Streamlit**: Modern web app framework for Python

---

**Note**: This Streamlit version focuses on configuration generation and is optimized for cloud deployment. For local HPC cluster integration, consider the original Flask version.


