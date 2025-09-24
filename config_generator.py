#!/usr/bin/env python3
"""
ParGaMD Configuration Generator
Extracted from Flask app for Streamlit use
"""

import os
from jinja2 import Template
from typing import Dict, List, Any

class ParGaMDConfigGenerator:
    """Generate configuration files for ParGaMD experiments"""
    
    def __init__(self):
        self.templates = self._load_templates()
    
    def _load_templates(self):
        """Load Jinja2 templates for configuration files"""
        return {
            'west_cfg': self._get_west_cfg_template(),
            'env_sh': self._get_env_sh_template(),
            'runseg_sh': self._get_runseg_sh_template(),
            'run_cmd_sh': self._get_run_cmd_sh_template(),
            'run_we_sh': self._get_run_we_sh_template()
        }
    
    def _get_west_cfg_template(self):
        return Template("""# The master WEST configuration file for a simulation.
# vi: set filetype=yaml :
---
west: 
  system:
    driver: westpa.core.systems.WESTSystem
    system_options:
      # Dimensionality of your progress coordinate
      pcoord_ndim: {{ pcoord_ndim }}
      # Number of data points per iteration
      # Needs to be pcoord_len >= 2 (minimum of parent, last frame) to work with most analysis tools
      pcoord_len: {{ pcoord_len }}
      # Data type for your progress coordinate 
      pcoord_dtype: !!python/name:numpy.float32
      bins:
        type: RectilinearBinMapper
        # The edges of the bins 
        boundaries:         
{% for cv_bin in cv_bins %}
          - {{ cv_bin }}
{% endfor %}
      # Number walkers per bin
      bin_target_counts: {{ bin_target_counts }}
  propagation:
    max_total_iterations: {{ max_total_iterations }}
    max_run_wallclock:    47:30:00
    propagator:           executable
    gen_istates:          false
  data:
    west_data_file: west.h5
    datasets:
      - name:        pcoord
        scaleoffset: 4
      - name:        coord
        dtype:       float32
        scaleoffset: 3
    data_refs:
      segment:       $WEST_SIM_ROOT/traj_segs/{segment.n_iter:06d}/{segment.seg_id:06d}
      basis_state:   $WEST_SIM_ROOT/bstates/{basis_state.auxref}
      initial_state: $WEST_SIM_ROOT/istates/{initial_state.iter_created}/{initial_state.state_id}.rst
  plugins:
  executable:
    environ:
      PROPAGATION_DEBUG: 1
    datasets:
      - name:    coord
        enabled: false
    propagator:
      executable: $WEST_SIM_ROOT/westpa_scripts/runseg.sh
      stdout:     $WEST_SIM_ROOT/seg_logs/{segment.n_iter:06d}/{segment.seg_id:06d}.log
      stderr:     stdout
      stdin:      null
      cwd:        null
      environ:
        SEG_DEBUG: 1
    get_pcoord:
      executable: $WEST_SIM_ROOT/westpa_scripts/get_pcoord.sh
      stdout:     /dev/null 
      stderr:     stdout
    gen_istate:
      executable: $WEST_SIM_ROOT/westpa_scripts/gen_istate.sh
      stdout:     /dev/null 
      stderr:     stdout
    post_iteration:
      enabled:    true
      executable: $WEST_SIM_ROOT/westpa_scripts/post_iter.sh
      stderr:     stdout
    pre_iteration:
      enabled:    false
      executable: $WEST_SIM_ROOT/westpa_scripts/pre_iter.sh
      stderr:     stdout
""")
    
    def _get_env_sh_template(self):
        return Template("""#!/bin/bash

source ~/.bash_profile
module purge
module load shared
module load gpu/0.15.4
module load slurm
module load openmpi/4.0.4
module load cuda/11.0.2
module load amber/20-patch15
conda activate westpa-2.0

export PATH=$PATH:$HOME/bin
export PYTHONPATH=$HOME/miniconda3/envs/westpa-2.0/bin/python
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH

# Explicitly name our simulation root directory
if [[ -z "$WEST_SIM_ROOT" ]]; then
    export WEST_SIM_ROOT="$PWD"
fi

export SIM_NAME=$(basename $WEST_SIM_ROOT)
echo "simulation $SIM_NAME root is $WEST_SIM_ROOT"

# Set up environment for dynamics
source $AMBERHOME/amber.sh

# Set runtime commands (this is said to be easier on the filesystem)
export NODELOC="${WEST_SIM_ROOT:-$PWD}"
export USE_LOCAL_SCRATCH=1

export WM_ZMQ_MASTER_HEARTBEAT=100
export WM_ZMQ_WORKER_HEARTBEAT=100
export WM_ZMQ_TIMEOUT_FACTOR=300
export BASH=$SWROOT/bin/bash
export PERL=$SWROOT/usr/bin/perl
export ZSH=$SWROOT/bin/zsh
export IFCONFIG=$SWROOT/bin/ifconfig
export CUT=$SWROOT/usr/bin/cut
export TR=$SWROOT/usr/bin/tr
export LN=$SWROOT/bin/ln
export CP=$SWROOT/bin/cp
export RM=$SWROOT/bin/rm
export SED=$SWROOT/bin/sed
export CAT=$SWROOT/bin/cat
export HEAD=$SWROOT/bin/head
export TAR=$SWROOT/bin/tar
export AWK=$SWROOT/usr/bin/awk
export PASTE=$SWROOT/usr/bin/paste
export GREP=$SWROOT/bin/grep
export SORT=$SWROOT/usr/bin/sort
export UNIQ=$SWROOT/usr/bin/uniq
export HEAD=$SWROOT/usr/bin/head
export MKDIR=$SWROOT/bin/mkdir
export ECHO=$SWROOT/bin/echo
export DATE=$SWROOT/bin/date
export SANDER=$AMBERHOME/bin/sander
export PMEMD=$AMBERHOME/bin/pmemd.cuda
export CPPTRAJ=$AMBERHOME/bin/cpptraj
""")
    
    def _get_runseg_sh_template(self):
        return Template("""#!/bin/bash

if [ -n "$SEG_DEBUG" ] ; then
  set -x
  env | sort
fi

cd $WEST_SIM_ROOT
mkdir -pv $WEST_CURRENT_SEG_DATA_REF
cd $WEST_CURRENT_SEG_DATA_REF

ln -sv $WEST_SIM_ROOT/common_files/{{ protein_name }}.prmtop .
ln -sv $WEST_SIM_ROOT/common_files/gamd-restart.dat .

if [ "$WEST_CURRENT_SEG_INITPOINT_TYPE" = "SEG_INITPOINT_CONTINUES" ]; then
  sed "s/RAND/$WEST_RAND16/g" $WEST_SIM_ROOT/common_files/md.in > md.in
  ln -sv $WEST_PARENT_DATA_REF/seg.rst ./parent.rst
elif [ "$WEST_CURRENT_SEG_INITPOINT_TYPE" = "SEG_INITPOINT_NEWTRAJ" ]; then
  sed "s/RAND/$WEST_RAND16/g" $WEST_SIM_ROOT/common_files/md_init.in > md.in
  ln -sv $WEST_PARENT_DATA_REF ./parent.rst
fi

{% if enable_gpu_parallelization %}
export CUDA_DEVICES=(`echo $CUDA_VISIBLE_DEVICES_ALLOCATED | tr , ' '`)
export CUDA_VISIBLE_DEVICES=${CUDA_DEVICES[$WM_PROCESS_INDEX]}

echo "RUNSEG.SH: CUDA_VISIBLE_DEVICES_ALLOCATED = " $CUDA_VISIBLE_DEVICES_ALLOCATED
echo "RUNSEG.SH: WM_PROCESS_INDEX = " $WM_PROCESS_INDEX
echo "RUNSEG.SH: CUDA_VISIBLE_DEVICES = " $CUDA_VISIBLE_DEVICES
{% endif %}

while ! grep -q "Final Performance Info" seg.log; do
	$PMEMD -O -i md.in   -p {{ protein_name }}.prmtop  -c parent.rst \\
          -r seg.rst -x seg.nc      -o seg.log    -inf seg.nfo -gamd gamd.log
done

# Progress Coordinate Calculation
COMMAND="         parm {{ protein_name }}.prmtop\\n"
COMMAND="${COMMAND} trajin $WEST_CURRENT_SEG_DATA_REF/parent.rst\\n"
COMMAND="${COMMAND} trajin $WEST_CURRENT_SEG_DATA_REF/seg.nc\\n"
{% if has_pdb_file %}
COMMAND="${COMMAND} reference $WEST_SIM_ROOT/common_files/{{ protein_name }}.pdb\\n"
{% else %}
COMMAND="${COMMAND} reference $WEST_SIM_ROOT/common_files/{{ protein_name }}.inpcrd\\n"
{% endif %}
{{ cv_commands }}
COMMAND="${COMMAND} go\\n"

echo -e $COMMAND | $CPPTRAJ

# Extract progress coordinate values
{% if cv_count == 1 %}
cat {{ cv_output_files[0] }} | tail -n +2 | awk {'print $2'} > $WEST_PCOORD_RETURN
{% else %}
paste {% for output_file in cv_output_files %}<(cat {{ output_file }} | tail -n +2 | awk {'print $2'}) {% endfor %}>$WEST_PCOORD_RETURN
{% endif %}

# Clean up
rm -f md.in seg.nfo seg.pdb
""")
    
    def _get_run_cmd_sh_template(self):
        return Template("""#!/bin/bash
#SBATCH --job-name="{{ protein_name }}_GaMD"
#SBATCH --output="job.out"
#SBATCH --partition=gpu-shared
#SBATCH --nodes=1
#SBATCH --gpus=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=50G
#SBATCH --account={{ account }}
#SBATCH --no-requeue
#SBATCH --mail-user={{ email }}
#SBATCH --mail-type=ALL
#SBATCH -t 48:00:00

module purge
module load shared
module load gpu/0.15.4
module load slurm
module load openmpi/4.0.4
module load cuda/11.0.2
module load amber/20

export PATH=$PATH:$HOME/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH
source $AMBERHOME/amber.sh
pmemd.cuda -O -i md.in -o md.out -p {{ protein_name }}.prmtop -c {{ protein_name }}.rst -r md_cmd.rst -x md.nc
""")
    
    def _get_run_we_sh_template(self):
        return Template("""#!/bin/bash
#SBATCH --job-name="{{ protein_name }}_WE_run"
#SBATCH --output="job.out"
#SBATCH --partition=gpu-shared
#SBATCH --nodes=1
#SBATCH --gpus=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem=50G
#SBATCH --account={{ account }}
#SBATCH --no-requeue
#SBATCH --mail-user={{ email }}
#SBATCH --mail-type=ALL
#SBATCH -t 48:00:00

set -x
cd $SLURM_SUBMIT_DIR
source ~/.bashrc
module purge
module load shared
module load gpu/0.15.4
module load slurm
module load openmpi/4.0.4
module load cuda/11.0.2
module load amber/20-patch15
conda activate westpa-2.0

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH
export WEST_SIM_ROOT=$SLURM_SUBMIT_DIR
cd $WEST_SIM_ROOT
export PYTHONPATH=$HOME/miniconda3/envs/westpa-2.0/bin/python

./init.sh
echo "init.sh ran"
source env.sh || exit 1
env | sort
SERVER_INFO=$WEST_SIM_ROOT/west_zmq_info.json

#TODO: set num_gpu_per_node
num_gpu_per_node=1
rm -rf nodefilelist.txt
scontrol show hostname $SLURM_JOB_NODELIST > nodefilelist.txt

# start server
w_run --work-manager=zmq --n-workers=0 --zmq-mode=master --zmq-write-host-info=$SERVER_INFO --zmq-comm-mode=tcp &> west-$SLURM_JOBID-local.log &

# wait on host info file up to 1 min
for ((n=0; n<60; n++)); do
    if [ -e $SERVER_INFO ] ; then
        echo "== server info file $SERVER_INFO =="
        cat $SERVER_INFO
        break
    fi
    sleep 1
done

# exit if host info file doesn't appear in one minute
if ! [ -e $SERVER_INFO ] ; then
    echo 'server failed to start'
    exit 1
fi
export CUDA_VISIBLE_DEVICES=0
echo$CUDA_VISIBLE_DEVICES
for node in $(cat nodefilelist.txt); do
    ssh -o StrictHostKeyChecking=no $node $PWD/node.sh $SLURM_SUBMIT_DIR $SLURM_JOBID $node $CUDA_VISIBLE_DEVICES --work-manager=zmq --n-workers=$num_gpu_per_node --zmq-mode=client --zmq-read-host-info=$SERVER_INFO --zmq-comm-mode=tcp &
done
wait
""")
    
    def generate_bin_boundaries(self, min_val: float, max_val: float, step_size: float, include_infinite_bounds: bool = True) -> List:
        """Generate bin boundaries for progress coordinates"""
        min_val = float(min_val)
        max_val = float(max_val)
        step_size = float(step_size)
        if step_size <= 0:
            step_size = 0.1
        boundaries = []
        if include_infinite_bounds:
            boundaries.append('-inf')
        current = min_val
        num_steps = int(round((max_val - min_val) / step_size))
        for i in range(num_steps + 1):
            value = min_val + i * step_size
            boundaries.append(float(f"{value:.6g}"))
        if include_infinite_bounds:
            boundaries.append('inf')
        return boundaries
    
    def _get_cpptraj_command(self, cv_type: str, output_file: str, cv_name: str) -> str:
        """Generate CPPTRAJ command for specific CV type"""
        commands = {
            "rmsd": f'COMMAND="${{COMMAND}} rms ca-rmsd @CA reference out {output_file} mass\\n"',
            "radius_gyration": f'COMMAND="${{COMMAND}} radgyr ca-rg @CA out {output_file} mass\\n"',
            "distance": f'COMMAND="${{COMMAND}} distance {cv_name} :1@CA :10@CA out {output_file}\\n"',
            "native_contacts": f'COMMAND="${{COMMAND}} nativecontacts {cv_name} :* byresidue out {output_file}\\n"',
            "dihedral": f'COMMAND="${{COMMAND}} dihedral {cv_name} :1@C :1@N :2@CA :2@C out {output_file}\\n"',
            "hbond": f'COMMAND="${{COMMAND}} hbond {cv_name} out {output_file}\\n"',
            "surface_area": f'COMMAND="${{COMMAND}} surf {cv_name} :* out {output_file}\\n"',
            "secondary_structure": f'COMMAND="${{COMMAND}} secstruct {cv_name} :* out {output_file}\\n"',
            "custom": f'# Custom CV: {cv_name} - Manual implementation required\\n# TODO: Replace this comment with your custom CPPTRAJ command\\n# COMMAND="${{COMMAND}} [YOUR_CUSTOM_CPPTRAJ_COMMAND] out {output_file}\\n"\\n# NOTE: Make sure the result is written to {output_file} and extract value to $WEST_PCOORD_RETURN'
        }
        return commands.get(cv_type, commands["rmsd"])  # Default to RMSD
    
    def generate_configs(self, params: Dict[str, Any], uploaded_files: Dict[str, Dict] = None) -> Dict[str, str]:
        """Generate all configuration files based on user parameters"""
        configs = {}
        
        # Handle uploaded files if provided
        if uploaded_files:
            protein_name = params.get('protein_name', 'chignolin')
            
            # Handle structure files (PDB or INPCRD)
            if 'pdb_file' in uploaded_files:
                pdb_content = uploaded_files['pdb_file']['content']
                # PDB files are text files, so decode as UTF-8
                if isinstance(pdb_content, bytes):
                    try:
                        pdb_content = pdb_content.decode('utf-8')
                    except UnicodeDecodeError:
                        # Try with latin-1 if UTF-8 fails
                        pdb_content = pdb_content.decode('latin-1')
                configs[f'common_files/{protein_name}.pdb'] = pdb_content
                configs[f'cMD/{protein_name}.pdb'] = pdb_content
            
            if 'inpcrd_file' in uploaded_files:
                inpcrd_content = uploaded_files['inpcrd_file']['content']
                # INPCRD files are binary, store as base64 encoded string
                if isinstance(inpcrd_content, bytes):
                    import base64
                    inpcrd_content = base64.b64encode(inpcrd_content).decode('ascii')
                configs[f'common_files/{protein_name}.inpcrd'] = inpcrd_content
                configs[f'cMD/{protein_name}.inpcrd'] = inpcrd_content
            
            # Handle PRMTOP file
            if 'prmtop_file' in uploaded_files:
                prmtop_content = uploaded_files['prmtop_file']['content']
                # PRMTOP files are binary, store as base64 encoded string
                if isinstance(prmtop_content, bytes):
                    import base64
                    prmtop_content = base64.b64encode(prmtop_content).decode('ascii')
                configs[f'common_files/{protein_name}.prmtop'] = prmtop_content
                configs[f'cMD/{protein_name}.prmtop'] = prmtop_content
            
            # Handle optional RST file
            if 'rst_file' in uploaded_files:
                rst_content = uploaded_files['rst_file']['content']
                rst_as_bstate = params.get('rst_as_bstate', False)
                
                # RST files are binary, store as base64 encoded string
                if isinstance(rst_content, bytes):
                    import base64
                    rst_content = base64.b64encode(rst_content).decode('ascii')
                
                if rst_as_bstate:
                    # Place as bstate.rst in bstates folder for ParGaMD simulation
                    configs['bstates/bstate.rst'] = rst_content
                else:
                    # Place in cMD folder for conventional MD
                    configs[f'cMD/{protein_name}.rst'] = rst_content
        
        include_inf = bool(params.get('include_infinite_bounds', True))
        
        # Get CV list from parameters
        cv_list = params.get('cv_list', [{'type': 'rmsd', 'min': 0.0, 'max': 8.0, 'step': 0.2}])
        
        # Calculate pcoord_len based on nstlim and ntpr
        nstlim = int(params['nstlim'])
        ntpr = int(params['ntpr'])
        if ntpr <= 0:
            ntpr = 1
        pcoord_len = (nstlim // ntpr) + 1
        
        # Generate bin boundaries for each CV
        cv_bins = []
        for cv in cv_list:
            cv_bins.append(self.generate_bin_boundaries(
                cv['min'], cv['max'], cv['step'], include_inf
            ))
        
        # Generate west.cfg
        configs['west.cfg'] = self.templates['west_cfg'].render(
            pcoord_len=pcoord_len,
            pcoord_ndim=len(cv_list),
            cv_bins=cv_bins,
            bin_target_counts=int(params['bin_target_counts']),
            max_total_iterations=int(params['max_total_iterations'])
        )
        
        # Generate env.sh
        configs['env.sh'] = self.templates['env_sh'].render()
        
        # Generate commands for each CV
        cv_commands = []
        cv_output_files = []
        
        for i, cv in enumerate(cv_list):
            cv_type = cv['type']
            
            # Use custom name if available, otherwise default naming
            if cv_type == 'custom' and 'name' in cv:
                cv_name = cv['name']
                output_file = f"custom_{i+1}.dat"
            else:
                cv_name = f"CV{i+1}"
                output_file = f"{cv_type}_{i+1}.dat"
            
            cv_commands.append(self._get_cpptraj_command(cv_type, output_file, cv_name))
            cv_output_files.append(output_file)
        
        # Determine if PDB file is available
        has_pdb_file = uploaded_files and 'pdb_file' in uploaded_files if uploaded_files else False
        
        # Generate runseg.sh
        configs['westpa_scripts/runseg.sh'] = self.templates['runseg_sh'].render(
            protein_name=params['protein_name'],
            enable_gpu_parallelization=params['enable_gpu_parallelization'],
            cv_commands='\n'.join(cv_commands),
            cv_output_files=cv_output_files,
            cv_count=len(cv_list),
            has_pdb_file=has_pdb_file
        )
        
        # Generate run_cmd.sh
        configs['cMD/run_cmd.sh'] = self.templates['run_cmd_sh'].render(
            protein_name=params['protein_name'],
            account=params['account'],
            email=params['email']
        )
        
        # Generate run_WE.sh
        configs['run_WE.sh'] = self.templates['run_we_sh'].render(
            protein_name=params['protein_name'],
            account=params['account'],
            email=params['email']
        )
        
        # Generate get_pcoord.sh (for initial state analysis)
        configs['westpa_scripts/get_pcoord.sh'] = self._get_get_pcoord_sh_template().render(
            protein_name=params['protein_name'],
            cv_commands='\n'.join(cv_commands),
            cv_output_files=cv_output_files,
            cv_count=len(cv_list),
            has_pdb_file=has_pdb_file
        )
        
        # Add all main folder .sh files
        main_sh_files = ['run_data.sh', 'run.sh', 'reweight-2d.sh', 'node.sh', 'init.sh']
        for sh_file in main_sh_files:
            try:
                with open(sh_file, 'r', encoding='utf-8', errors='ignore') as f:
                    configs[sh_file] = f.read()
            except FileNotFoundError:
                # Create a basic template if file doesn't exist
                configs[sh_file] = f"#!/bin/bash\n# {sh_file}\necho 'Running {sh_file}'\n"
        
        # Add Python scripts
        python_scripts = ['simtime.py', 'data_extract.py']
        for py_file in python_scripts:
            try:
                with open(py_file, 'r', encoding='utf-8', errors='ignore') as f:
                    configs[py_file] = f.read()
            except FileNotFoundError:
                # Create a basic template if file doesn't exist
                configs[py_file] = f"#!/usr/bin/env python3\n# {py_file}\nprint('Running {py_file}')\n"
        
        # Add common_files folder contents (only if not already provided by uploaded files)
        protein_name = params.get('protein_name', 'chignolin')
        common_files = [
            'common_files/gamd-restart.dat',
            'common_files/md_init.in',
            'common_files/md.in'
        ]
        
        # Only add default structure/topology files if not provided by uploads
        if not (uploaded_files and ('pdb_file' in uploaded_files or 'inpcrd_file' in uploaded_files)):
            common_files.append(f'common_files/{protein_name}.pdb')
        
        if not (uploaded_files and 'prmtop_file' in uploaded_files):
            common_files.append(f'common_files/{protein_name}.prmtop')
        
        for file_path in common_files:
            # Skip if already in configs (from uploaded files)
            if file_path in configs:
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    configs[file_path] = f.read()
            except FileNotFoundError:
                # Create placeholder content for missing files
                if file_path.endswith('.pdb'):
                    configs[file_path] = "# Placeholder PDB file\n# Upload your protein structure here\n"
                elif file_path.endswith('.prmtop'):
                    configs[file_path] = "# Placeholder PRMTOP file\n# Upload your topology file here\n"
                else:
                    configs[file_path] = f"# Placeholder {file_path}\n"
        
        # Add bstates folder contents (only if not already provided by uploaded files)
        bstates_files = [
            'bstates/bstate_cpptraj.rst',
            'bstates/bstates.txt',
            'bstates/md.rst'
        ]
        
        # Only add default bstate.rst if not provided by uploads as bstate
        if not (uploaded_files and 'rst_file' in uploaded_files and params.get('rst_as_bstate', False)):
            bstates_files.append('bstates/bstate.rst')
        
        for file_path in bstates_files:
            # Skip if already in configs (from uploaded files)
            if file_path in configs:
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    configs[file_path] = f.read()
            except FileNotFoundError:
                # Create placeholder content for missing files
                if file_path.endswith('.rst'):
                    configs[file_path] = "# Placeholder restart file\n"
                else:
                    configs[file_path] = f"# Placeholder {file_path}\n"
        
        # Add additional cMD folder contents (only if not already provided by uploaded files)
        cmd_additional_files = [
            'cMD/md.in',
            'cMD/md_cmd.in'
        ]
        
        # Only add default structure/topology files if not provided by uploads
        if not (uploaded_files and ('pdb_file' in uploaded_files or 'inpcrd_file' in uploaded_files)):
            cmd_additional_files.append(f'cMD/{protein_name}.pdb')
        
        if not (uploaded_files and 'prmtop_file' in uploaded_files):
            cmd_additional_files.append(f'cMD/{protein_name}.prmtop')
        
        # Only add default RST file if not provided by uploads or if RST is not being used as bstate
        if not (uploaded_files and 'rst_file' in uploaded_files):
            cmd_additional_files.append(f'cMD/{protein_name}.rst')
        
        for file_path in cmd_additional_files:
            # Skip if already in configs (from uploaded files)
            if file_path in configs:
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    configs[file_path] = f.read()
            except FileNotFoundError:
                # Create placeholder content for missing files
                if file_path.endswith('.pdb'):
                    configs[file_path] = "# Placeholder PDB file\n# Upload your protein structure here\n"
                elif file_path.endswith('.prmtop'):
                    configs[file_path] = "# Placeholder PRMTOP file\n# Upload your topology file here\n"
                elif file_path.endswith('.rst'):
                    configs[file_path] = "# Placeholder restart file\n"
                else:
                    configs[file_path] = f"# Placeholder {file_path}\n"
        
        # Add additional westpa_scripts
        westpa_additional_files = [
            'westpa_scripts/cat_trajectory.py',
            'westpa_scripts/gen_istate.sh',
            'westpa_scripts/post_iter.sh',
            'westpa_scripts/tar_segs.sh'
        ]
        for file_path in westpa_additional_files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    configs[file_path] = f.read()
            except FileNotFoundError:
                # Create placeholder content for missing files
                if file_path.endswith('.py'):
                    configs[file_path] = f"#!/usr/bin/env python3\n# {file_path}\nprint('Running {file_path}')\n"
                else:
                    configs[file_path] = f"#!/bin/bash\n# {file_path}\necho 'Running {file_path}'\n"
        
        # Add documentation and utility files
        doc_files = [
            'README.md',
            'CHANGELOG.md',
            'LICENSE',
            'PyReweighting-2D.py',
            'quick_start.py',
            'nodefilelist.txt',
            'tstate.file'
        ]
        for file_path in doc_files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    configs[file_path] = f.read()
            except FileNotFoundError:
                # Create placeholder content for missing files
                if file_path.endswith('.py'):
                    configs[file_path] = f"#!/usr/bin/env python3\n# {file_path}\nprint('Running {file_path}')\n"
                else:
                    configs[file_path] = f"# Placeholder {file_path}\n"
        
        return configs
    
    def _get_get_pcoord_sh_template(self):
        return Template("""#!/bin/bash

if [ -n "$SEG_DEBUG" ] ; then
  set -x
  env | sort
fi

cd $WEST_SIM_ROOT

COMMAND="parm $WEST_SIM_ROOT/common_files/{{ protein_name }}.prmtop \\n"
COMMAND="${COMMAND} trajin $WEST_STRUCT_DATA_REF \\n"
{% if has_pdb_file %}
COMMAND="${COMMAND} reference $WEST_SIM_ROOT/common_files/{{ protein_name }}.pdb \\n"
{% else %}
COMMAND="${COMMAND} reference $WEST_SIM_ROOT/common_files/{{ protein_name }}.inpcrd \\n"
{% endif %}
{{ cv_commands }}
COMMAND="${COMMAND} go"

echo -e "${COMMAND}" | $CPPTRAJ

# Extract progress coordinate values
{% if cv_count == 1 %}
cat {{ cv_output_files[0] }} | tail -n 1 | awk {'print $2'} > $WEST_PCOORD_RETURN
{% else %}
paste {% for output_file in cv_output_files %}<(cat {{ output_file }} | tail -n 1 | awk {'print $2'}) {% endfor %}>$WEST_PCOORD_RETURN
{% endif %}

if [ -n "$SEG_DEBUG" ] ; then
  head -v $WEST_PCOORD_RETURN
fi
""")

