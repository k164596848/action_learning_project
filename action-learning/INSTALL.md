# Install Guide (for Ubuntu 18.04)

## ToC

- [OpenPose](#openpose-install) release version 14.0, 15.0, 16.0 comfied it could work.
- [Server](#server-install)

## OpenPose Install

1. clone openpose project

   ```bash
   git clone https://github.com/CMU-Perceptual-Computing-Lab/openpose
   cd openpose
   ```

2. install cuda

   ```bash
   sudo ./scripts/ubuntu/install_cuda.sh
   ```

3. install cuDNN

   ```bash
   sudo ./scripts/ubuntu/install_cudnn.sh
   ```

4. install caffe prerequisites

   ```bash
   sudo bash ./scripts/ubuntu/install_deps.sh
   ```

5. install opencv

   ```bash
   sudo apt-get install libopencv-dev
   ```

6. `reboot`
7. configuration

   ```bash
   cd openpose
   mkdir build
   cd build
   sudo snap install cmake --classic  # cmake must >= 3.12
   cmake ..
   ```

8. building

   ```bash
   make -j`nproc`
   ```

9. export environment path (absolute path)

   ```bash
   export OPENPOSE=/path/to/your/openpose/
   ```

### Server Install

1. install Python 3.7+
2. check python version and pip

   ```bash
   python -V  # 3.7+
   pip -V  # is installed as python
   ```

3. clone action learning project

   ```bash
   git clone https://github.com/cgm-lab/action-learning.git
   cd action-learning
   ```

4. install requirements

   ```bash
   pip install -r requirements.txt
   ```

### Run

```bash:3
python app.py
```
