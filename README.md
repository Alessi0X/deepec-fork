#DeepEC

##Procedure

**Note**: 
Size of the protein sequence input file should be adjusted according to the memory size of your computer. 
This source code requires Python 3.9, 3.10, 3.11, 3.12, or 3.13.

1. Clone the repository

        git clone https://bitbucket.org/kaistsystemsbiology/deepec.git

2. Install DIAMOND (sequence alignment tool)

    **Ubuntu/Debian:**
    
        sudo apt-get update
        sudo apt-get install diamond-aligner

    **macOS (using Homebrew):**
    
        brew install diamond

    **Or download from:** https://github.com/bbuchfink/diamond

3. Create a virtual environment (recommended)

        python -m venv deepec_env
        source deepec_env/bin/activate  # On Windows: deepec_env\Scripts\activate

4. Upgrade pip

        pip install --upgrade pip

5. Install Python dependencies

        pip install -r requirements.txt

   If installation fails, install packages individually with pre-built wheels:

        pip install tensorflow numpy scipy pandas scikit-learn h5py biopython

**Important**: The pre-trained model files (.h5) and label encoders (.pkl) were created with Keras 2.1.6 and scikit-learn 0.19. The code includes compatibility layers to load these legacy files with modern TensorFlow 2.x and scikit-learn 1.3+.

##Example

- Run DeepEC

        python deepec.py -i ./example/test.fa -o ./output

##Verification (Optional)

To verify that the upgraded version produces the same results as the original:

**Automated Docker comparison (recommended):**

        chmod +x test_comparison.sh
        ./test_comparison.sh

**Note:** Docker needs at least 4GB RAM allocated. If build fails with memory errors:
- Docker Desktop → Settings → Resources → Memory → Increase to 6-8GB
- Restart Docker Desktop and try again

This script:
1. Builds a Docker image with the original conda environment and old code
2. Runs the legacy version inside Docker (outputs written to host via volume mount)
3. Runs the new Python 3.13 version locally
4. Compares the outputs with the comparison script

**Manual Docker test:**

        # Build legacy version container
        docker build -f Dockerfile.legacy -t deepec:legacy .
        
        # Run legacy version (outputs to local directory)
        docker run --rm -v "$(pwd):/data" deepec:legacy \
            -i /data/example/test.fa -o /data/output_old
        
        # Run new version
        python deepec.py -i example/test.fa -o output_new
        
        # Compare
        python compare_outputs.py output_old output_new

Expected: EC number predictions should match exactly. DNN activity scores may differ slightly (< 0.001) due to TensorFlow version differences. 

