#!/usr/bin/env python3
"""
ParGaMD Streamlit GUI
Web-based interface for configuring ParGaMD simulations
"""

import streamlit as st
import zipfile
import io
from datetime import datetime
from config_generator import ParGaMDConfigGenerator

# Try to import code editor with correct syntax
try:
    from code_editor import code_editor
    CODE_EDITOR_AVAILABLE = True
except ImportError:
    CODE_EDITOR_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="ParGaMD Configuration Generator",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .step-header {
        color: #ff7f0e;
        border-bottom: 2px solid #ff7f0e;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    .config-preview {
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 0.375rem;
        padding: 1rem;
        font-family: 'Courier New', monospace;
        font-size: 0.875rem;
        max-height: 400px;
        overflow-y: auto;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.375rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.375rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize session state variables"""
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 1
    if 'form_data' not in st.session_state:
        st.session_state.form_data = {}
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = {}
    if 'generated_configs' not in st.session_state:
        st.session_state.generated_configs = {}
    if 'config_generator' not in st.session_state:
        st.session_state.config_generator = ParGaMDConfigGenerator()

init_session_state()

def render_header():
    """Render the main header"""
    st.markdown("""
    <div class="main-header">
        <h1>🧬 ParGaMD Configuration Generator</h1>
        <p>Configure your Parallelizable Gaussian Accelerated Molecular Dynamics simulations</p>
    </div>
    """, unsafe_allow_html=True)

def render_step_indicator():
    """Render step indicator"""
    steps = [
        ("System Setup", "⚙️"),
        ("Molecular System", "🧬"),
        ("WE Parameters", "⚡"),
        ("GPU Options", "🖥️"),
        ("Review & Edit", "✏️"),
        ("Download", "📥")
    ]
    
    cols = st.columns(len(steps))
    for i, (step_name, icon) in enumerate(steps):
        with cols[i]:
            step_num = i + 1
            if step_num == st.session_state.current_step:
                st.markdown(f"**{icon} {step_name}**")
                st.progress(1.0)
            elif step_num < st.session_state.current_step:
                st.markdown(f"✅ {step_name}")
                st.progress(1.0)
            else:
                st.markdown(f"{icon} {step_name}")
                st.progress(0.0)

def render_system_setup():
    """Render system setup step"""
    st.markdown('<div class="step-header"><h2>⚙️ System Setup</h2></div>', unsafe_allow_html=True)
    
    with st.form("system_setup_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.session_state.form_data['account'] = st.text_input(
                "SLURM Account",
                value=st.session_state.form_data.get('account', ''),
                help="Your SLURM account name"
            )
            
        with col2:
            st.session_state.form_data['email'] = st.text_input(
                "Email for Notifications",
                value=st.session_state.form_data.get('email', ''),
                help="Email address for job notifications"
            )
        
        st.info("💡 SSH and remote job submission are disabled in this cloud version. You can still generate configuration files.")
        
        submitted = st.form_submit_button("Next Step →", type="primary")
        if submitted:
            if st.session_state.form_data['account'] and st.session_state.form_data['email']:
                st.session_state.current_step = 2
                st.rerun()
            else:
                st.error("Please fill in all required fields")

def render_molecular_system():
    """Render molecular system step"""
    st.markdown('<div class="step-header"><h2>🧬 Molecular System</h2></div>', unsafe_allow_html=True)
    
    with st.form("molecular_system_form"):
        st.session_state.form_data['protein_name'] = st.text_input(
            "Protein Name",
            value=st.session_state.form_data.get('protein_name', 'chignolin'),
            help="Name of your protein (used in file naming)"
        )
        
        st.subheader("File Uploads")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**PDB File**")
            pdb_file = st.file_uploader(
                "Upload PDB file",
                type=['pdb'],
                key="pdb_uploader",
                help="Protein structure file"
            )
            if pdb_file:
                st.session_state.uploaded_files['pdb_file'] = {
                    'name': pdb_file.name,
                    'content': pdb_file.read()
                }
                st.success(f"✅ {pdb_file.name} uploaded")
        
        with col2:
            st.write("**PRMTOP File**")
            prmtop_file = st.file_uploader(
                "Upload PRMTOP file",
                type=['prmtop'],
                key="prmtop_uploader",
                help="AMBER topology file"
            )
            if prmtop_file:
                st.session_state.uploaded_files['prmtop_file'] = {
                    'name': prmtop_file.name,
                    'content': prmtop_file.read()
                }
                st.success(f"✅ {prmtop_file.name} uploaded")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            back_btn = st.form_submit_button("← Back")
        with col2:
            next_btn = st.form_submit_button("Next Step →", type="primary")
        
        if back_btn:
            st.session_state.current_step = 1
            st.rerun()
        elif next_btn:
            if (st.session_state.form_data['protein_name'] and 
                'pdb_file' in st.session_state.uploaded_files and 
                'prmtop_file' in st.session_state.uploaded_files):
                st.session_state.current_step = 3
                st.rerun()
            else:
                st.error("Please fill in protein name and upload both PDB and PRMTOP files")

def render_we_parameters():
    """Render WE parameters step"""
    st.markdown('<div class="step-header"><h2>⚡ Weighted Ensemble Parameters</h2></div>', unsafe_allow_html=True)
    
    # CV Management Section (outside form)
    st.subheader("Collective Variables (CVs)")
    st.caption("💡 At least one CV is required. Add more CVs for enhanced analysis.")
    
    # Initialize CV list if not exists
    if 'cv_list' not in st.session_state.form_data:
        st.session_state.form_data['cv_list'] = [
            {'type': 'rmsd', 'min': 0.0, 'max': 8.0, 'step': 0.2, 'name': 'PC1'}
        ]
    
    # CV options
    cv_options = {
        "rmsd": "RMSD (Root Mean Square Deviation)",
        "radius_gyration": "Radius of Gyration",
        "distance": "Distance (Atom Pair Distance)", 
        "native_contacts": "Native Contacts",
        "dihedral": "Dihedral Angle",
        "hbond": "Hydrogen Bonds",
        "surface_area": "Surface Area",
        "secondary_structure": "Secondary Structure"
    }
    
    # CV help and command preview
    cv_help = {
        "rmsd": "Measures structural deviation from reference",
        "radius_gyration": "Measures protein compactness",
        "distance": "Distance between specific atom pairs",
        "native_contacts": "Number of native contacts formed",
        "dihedral": "Backbone/sidechain dihedral angles",
        "hbond": "Number or strength of hydrogen bonds",
        "surface_area": "Solvent accessible surface area",
        "secondary_structure": "Secondary structure content (helix, sheet, coil)"
    }
    
    cv_commands = {
        "rmsd": "rms ca-rmsd @CA reference out rmsd.dat mass",
        "radius_gyration": "radgyr ca-rg @CA out radius_gyration.dat mass",
        "distance": "distance PC1 :1@CA :10@CA out distance.dat",
        "native_contacts": "nativecontacts PC1 :* byresidue out native_contacts.dat",
        "dihedral": "dihedral PC1 :1@C :1@N :2@CA :2@C out dihedral.dat",
        "hbond": "hbond PC1 out hbond.dat",
        "surface_area": "surf PC1 :* out surface_area.dat",
        "secondary_structure": "secstruct PC1 :* out secondary_structure.dat"
    }
    
    # Display existing CVs
    cv_list = st.session_state.form_data['cv_list']
    for i, cv in enumerate(cv_list):
        with st.expander(f"CV {i+1}: {cv_options.get(cv['type'], cv['type'])}", expanded=True):
            col_cv1, col_cv2 = st.columns([2, 1])
            
            with col_cv1:
                # CV type selection
                cv['type'] = st.selectbox(
                    "CV Type",
                    options=list(cv_options.keys()),
                    format_func=lambda x: cv_options[x],
                    key=f"cv_type_{i}",
                    index=list(cv_options.keys()).index(cv['type']) if cv['type'] in cv_options else 0
                )
                
                # Show help and command preview
                st.caption(f"💡 {cv_help[cv['type']]}")
                st.code(cv_commands[cv['type']], language='bash')
                
                # CV parameters
                col_min, col_max = st.columns(2)
                with col_min:
                    cv['min'] = st.number_input(
                        "Min Value",
                        value=cv['min'],
                        step=0.1,
                        key=f"cv_min_{i}",
                        help="Minimum CV value"
                    )
                with col_max:
                    cv['max'] = st.number_input(
                        "Max Value", 
                        value=cv['max'],
                        step=0.1,
                        key=f"cv_max_{i}",
                        help="Maximum CV value"
                    )
                
                cv['step'] = st.number_input(
                    "Step Size",
                    value=cv['step'],
                    step=0.1,
                    key=f"cv_step_{i}",
                    help="CV step size"
                )
            
            with col_cv2:
                # Remove CV button (except for first CV)
                if i > 0:
                    if st.button("🗑️ Remove", key=f"remove_cv_{i}"):
                        cv_list.pop(i)
                        st.rerun()
                else:
                    st.caption("Required CV")
    
    # Add new CV button
    if st.button("➕ Add Another CV"):
        new_cv = {'type': 'radius_gyration', 'min': 0.0, 'max': 8.0, 'step': 0.2, 'name': f'PC{len(cv_list)+1}'}
        cv_list.append(new_cv)
        st.rerun()
    
    # Update form data
    st.session_state.form_data['cv_list'] = cv_list
    
    # Basic Parameters Form
    with st.form("we_parameters_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Basic Parameters")
            st.session_state.form_data['bin_target_counts'] = st.number_input(
                "Walkers per Bin",
                min_value=1,
                max_value=20,
                value=st.session_state.form_data.get('bin_target_counts', 4),
                help="Number of walkers per progress coordinate bin"
            )
            
            st.session_state.form_data['max_total_iterations'] = st.number_input(
                "Maximum Iterations",
                min_value=1,
                value=st.session_state.form_data.get('max_total_iterations', 1000),
                help="Total number of WE iterations"
            )
            
            st.session_state.form_data['nstlim'] = st.number_input(
                "Number of MD Steps (nstlim)",
                min_value=1000,
                value=st.session_state.form_data.get('nstlim', 50000),
                help="Number of molecular dynamics steps"
            )
            
            st.session_state.form_data['ntpr'] = st.number_input(
                "Print Frequency (ntpr)",
                min_value=100,
                value=st.session_state.form_data.get('ntpr', 500),
                help="Frequency of trajectory output"
            )
        
        with col2:
            st.subheader("Advanced Options")
            
            st.session_state.form_data['include_infinite_bounds'] = st.checkbox(
                "Include -inf and inf as outer bin boundaries",
                value=st.session_state.form_data.get('include_infinite_bounds', True),
                help="Prevents simulation errors with proper boundary handling"
            )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            back_btn = st.form_submit_button("← Back")
        with col2:
            next_btn = st.form_submit_button("Next Step →", type="primary")
        
        if back_btn:
            st.session_state.current_step = 2
            st.rerun()
        elif next_btn:
            st.session_state.current_step = 4
            st.rerun()

def render_gpu_options():
    """Render GPU options step"""
    st.markdown('<div class="step-header"><h2>🖥️ GPU Parallelization Options</h2></div>', unsafe_allow_html=True)
    
    with st.form("gpu_options_form"):
        st.session_state.form_data['enable_gpu_parallelization'] = st.checkbox(
            "Enable Multi-GPU Parallelization",
            value=st.session_state.form_data.get('enable_gpu_parallelization', False),
            help="When enabled, the simulation will use multiple GPUs for parallel processing. When disabled, the GPU parallelization code will be commented out to avoid errors on single-GPU systems."
        )
        
        if st.session_state.form_data['enable_gpu_parallelization']:
            st.info("✅ Multi-GPU parallelization will be enabled in the generated scripts")
        else:
            st.info("ℹ️ Single-GPU mode will be used (GPU parallelization code commented out)")
        
        col1, col2 = st.columns([1, 4])
        with col1:
            back_btn = st.form_submit_button("← Back")
        with col2:
            next_btn = st.form_submit_button("Next Step →", type="primary")
        
        if back_btn:
            st.session_state.current_step = 3
            st.rerun()
        elif next_btn:
            st.session_state.current_step = 5
            st.rerun()

def render_review_and_edit():
    """Render review and edit step with live editor"""
    st.markdown('<div class="step-header"><h2>✏️ Review & Edit Configuration</h2></div>', unsafe_allow_html=True)
    
    # Generate configurations if not already done
    if not st.session_state.generated_configs:
        try:
            st.session_state.generated_configs = st.session_state.config_generator.generate_configs(
                st.session_state.form_data
            )
            st.success("✅ Configuration files generated successfully!")
        except Exception as e:
            st.error(f"❌ Error generating configurations: {str(e)}")
            return
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📋 Configuration Summary")
        st.json({
            "System": {
                "Account": st.session_state.form_data.get('account', ''),
                "Email": st.session_state.form_data.get('email', ''),
                "Protein": st.session_state.form_data.get('protein_name', '')
            },
            "WE Parameters": {
                "Walkers per Bin": st.session_state.form_data.get('bin_target_counts', 4),
                "Max Iterations": st.session_state.form_data.get('max_total_iterations', 1000),
                "MD Steps": st.session_state.form_data.get('nstlim', 50000),
                "Print Frequency": st.session_state.form_data.get('ntpr', 500)
            },
            "Progress Coordinates": {
                f"CV {i+1} ({cv['type']})": f"{cv['min']} to {cv['max']} (step: {cv['step']})"
                for i, cv in enumerate(st.session_state.form_data.get('cv_list', []))
            },
            "GPU": {
                "Multi-GPU": st.session_state.form_data.get('enable_gpu_parallelization', False)
            }
        })
    
    with col2:
        st.subheader("📝 Live Editor")
        
        # File selection dropdown
        file_options = list(st.session_state.generated_configs.keys())
        selected_file = st.selectbox(
            "Select file to edit:",
            file_options,
            help="Choose a configuration file to edit"
        )
        
        if selected_file:
            # Determine language for syntax highlighting
            if selected_file.endswith('.cfg'):
                language = 'yaml'
            elif selected_file.endswith('.sh'):
                language = 'sh'  # Try 'sh' instead of 'bash'
            elif selected_file.endswith('.py'):
                language = 'python'
            else:
                language = 'text'
            
            # Live code editor
            if CODE_EDITOR_AVAILABLE:
                # Use streamlit-code-editor package with correct syntax
                st.success("✅ **Professional Code Editor Active!** Full syntax highlighting enabled.")
                
                # Debug: Show detected language
                st.caption(f"🎨 **Language detected:** {language}")
                
                # Try different language codes for .sh files if needed
                if selected_file.endswith('.sh') and language == 'sh':
                    # Try bash as fallback
                    language_fallback = 'bash'
                    st.caption(f"🔄 **Trying fallback language:** {language_fallback}")
                
                response_dict = code_editor(
                    st.session_state.generated_configs[selected_file],
                    lang=language,
                    key=f"editor_{selected_file}"
                )
                # Extract the edited content from the response dictionary
                edited_content = response_dict['text'] if 'text' in response_dict else st.session_state.generated_configs[selected_file]
            else:
                # Enhanced text_area editor
                st.info("💡 **Live Editor Ready!** Edit your configuration files directly below.")
                
                # Show file info
                st.caption(f"📄 **File:** {selected_file} | **Language:** {language}")
                
                # Syntax highlighting info
                if language == 'yaml':
                    st.caption("💡 **Tip:** This is a YAML configuration file. Use proper indentation!")
                elif language == 'bash':
                    st.caption("💡 **Tip:** This is a bash script. Make sure commands are properly formatted!")
                
                edited_content = st.text_area(
                    f"Edit {selected_file}:",
                    value=st.session_state.generated_configs[selected_file],
                    height=400,
                    key=f"editor_{selected_file}",
                    help="Edit the configuration file content. Changes will be applied when you click 'Apply Changes'.",
                    placeholder="Start editing your configuration file..."
                )
                
                # Show character count and basic info
                char_count = len(edited_content) if edited_content else 0
                line_count = edited_content.count('\n') + 1 if edited_content else 0
                st.caption(f"📊 **Lines:** {line_count} | **Characters:** {char_count}")
            
            # Apply changes button
            if st.button("Apply Changes", key=f"apply_{selected_file}"):
                st.session_state.generated_configs[selected_file] = edited_content
                st.success(f"✅ Changes applied to {selected_file}")
                st.rerun()
            
            # Reset to original button
            if st.button("Reset to Original", key=f"reset_{selected_file}"):
                try:
                    # Regenerate original content
                    original_configs = st.session_state.config_generator.generate_configs(
                        st.session_state.form_data
                    )
                    st.session_state.generated_configs[selected_file] = original_configs[selected_file]
                    st.success(f"✅ {selected_file} reset to original")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error resetting file: {str(e)}")
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("← Back"):
            st.session_state.current_step = 4
            st.rerun()
    with col2:
        if st.button("Regenerate All"):
            try:
                st.session_state.generated_configs = st.session_state.config_generator.generate_configs(
                    st.session_state.form_data
                )
                st.success("✅ All configuration files regenerated!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error regenerating configurations: {str(e)}")
    with col3:
        if st.button("Next Step →", type="primary"):
            st.session_state.current_step = 6
            st.rerun()

def create_zip_file():
    """Create ZIP file with all configurations"""
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Add generated configuration files
        for file_path, content in st.session_state.generated_configs.items():
            zip_file.writestr(file_path, content)
        
        # Add uploaded files
        for file_type, file_data in st.session_state.uploaded_files.items():
            if file_type == 'pdb_file':
                zip_file.writestr(f"common_files/{st.session_state.form_data.get('protein_name', 'protein')}.pdb", 
                                file_data['content'])
            elif file_type == 'prmtop_file':
                zip_file.writestr(f"common_files/{st.session_state.form_data.get('protein_name', 'protein')}.prmtop", 
                                file_data['content'])
    
    zip_buffer.seek(0)
    return zip_buffer

def render_download():
    """Render download step"""
    st.markdown('<div class="step-header"><h2>📥 Download Configuration Bundle</h2></div>', unsafe_allow_html=True)
    
    if not st.session_state.generated_configs:
        st.error("❌ No configuration files generated. Please go back and complete the setup.")
        return
    
    st.success("🎉 Your ParGaMD configuration is ready!")
    
    # Create download button
    zip_file = create_zip_file()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"ParGaMD_config_{timestamp}.zip"
    
    st.download_button(
        label="📦 Download Configuration Bundle",
        data=zip_file.getvalue(),
        file_name=filename,
        mime="application/zip",
        type="primary",
        help="Download all configuration files as a ZIP archive"
    )
    
    # Show file contents
    st.subheader("📁 Bundle Contents")
    
    with st.expander("View generated files"):
        for file_path, content in st.session_state.generated_configs.items():
            st.write(f"**{file_path}**")
            st.code(content, language='yaml' if file_path.endswith('.cfg') else 'bash')
            st.divider()
    
    # Navigation
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("← Back to Edit"):
            st.session_state.current_step = 5
            st.rerun()
    with col2:
        if st.button("🔄 Start New Configuration"):
            # Reset session state
            st.session_state.current_step = 1
            st.session_state.form_data = {}
            st.session_state.uploaded_files = {}
            st.session_state.generated_configs = {}
            st.rerun()

def main():
    """Main application function"""
    render_header()
    render_step_indicator()
    
    # Render current step
    if st.session_state.current_step == 1:
        render_system_setup()
    elif st.session_state.current_step == 2:
        render_molecular_system()
    elif st.session_state.current_step == 3:
        render_we_parameters()
    elif st.session_state.current_step == 4:
        render_gpu_options()
    elif st.session_state.current_step == 5:
        render_review_and_edit()
    elif st.session_state.current_step == 6:
        render_download()

if __name__ == "__main__":
    main()
