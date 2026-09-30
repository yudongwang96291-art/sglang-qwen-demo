Qwen3.5-2B Deployment with SGLang and Docker


Workflow: Python query.py ->(HTTP POST) -> http://localhost:30000/v1/chat/completions -> SGLang Server -> Qwen3.5-2B -> GPU
Docker provides the environment in which SGLang runs: Ubuntu/WSL 2 -> Docker -> SGLang container -> Qwen3.5-2B


Step 1: hardware and software requirements
Windows + NVIDIA GPU + Docker Desktop + WSL 2 + Ubuntu 24.04 LTS + Python3 + Qwen3.5-2B +SGLang

"nvidia-smi" -> confirm that Windows can see the NVIDIA GPU


Step 2: install and configure WSL 2 (used to provide a Linux envrionment)

"wsl --status" -> confirm taht the default WSL version is 2

"wsl --list --verbose" -> check installed distributions (initially, no Linux distribution installed)

"wsl --list --online" -> list all available distributions (used Ubuntu 24.04)

"wsl --install -d Ubuntu-24.04" -> install Ubuntu 24.04


Step 3: enable required Windows features

Win + R -> optionalfeatures -> enable Virtual Machine Platform + Windows Subsystem for Linux

Task Manager -> Performance -> CPU -> enable Virtualization 


Step 4: install Docker Desktop and enable WSL integration

In Docker Desktop: Settings -> Resources -> WSL Integration

Why Docker is used:

Docker provides an isolated software environment containing the dependencies needed to run SGLang.

Instead of installing all of SGLang's dependencies directly into Ubuntu, the SGLang Docker image provides the required environment inside a container.


Step 5: verify Docker GPU access

"sudo usermod -aG docker $USER" -> give Ubuntu user permission to use Docker without typing sudo every time

"docker run --rm --gpus all nvidia/cuda:12.8.0-base-ubuntu24.04 nvidia-smi" -> should show GPU


Step 6: create the project directory

"cd ~"

"mkdir -p sglang-project"

"cd ~/sglang-project"


Step 7: create a Python virutal environment

"sudo apt update" -> refresh Ubuntu's list pf packages

"sudo apt install python3-venv" -> install the support needed for Python's built-in virtual environment

"cd ~/sglang-project"

"python3 -m venv .venv" -> create the vritual environment

"source .venv/bin/activate" -> activate the virtual environment



Step 8: install Hugging Face Hub

"python -m pip -U huggingface_hub" -> hf command-line tool for downloading models from Hugging Face


Step 9: download the Qwen3.5-2B model

"hf download Qwen/Qwen3.5-2B --local-dir ./Qwen3.5-2B" 


Step 10: download the SGLang Docker image

"docker pull lmsysorg/sglang:latest" (this will take some time)


Step 11: start the SGLang server

"cker run --gpus all \
  --shm-size 32g \
  -p 30000:30000 \
  -v ~/sglang-project/Qwen3.5-2B:/models/Qwen3.5-2B \
  --ipc=host \
  lmsysorg/sglang:latest \
  python3 -m sglang.launch_server \
    --model-path /models/Qwen3.5-2B \
    --host 0.0.0.0 \
    --port 30000
"

"--gpus all" -> give the Docker container access to the NVIDIA GPU
"--shm-size 32g" -> provide a larger shared-memory allocation to the container
"-p 30000:30000" -> maps port 30000 on the container to port 30000 on the host, which allows other programs on the laptop to communicate with SGLang through: http://localhost:30000
"-v ~/sglang-project/Qwen3.5-2B:/models/Qwen3.5-2B" -> mount the local model directory into the Docker container, which lets the local path (~/sglang-project/Qwen3.5-2B) become /models/Qwen3.5-2B
"--model-path /models/Qwen3.5-2B" -> tell SGLang where the model is located inside the container
"--host 0.0.0.0" -> allow SGLang to listen for incoming connections on the container's network interfaces
"--port 30000" -> start the API server on port 30000

Once the model was loaded successfully, the SGLang terminal displayed: server is fired up and ready to roll


Step 12: open the SGLang API documentation

Open a browser and visit: http://localhost:30000/docs
Among the available endpoints, (/v1/chat/completions) this endpoint is used to send chat prompts to the model.


Step 13: check the model being served

"curl http://localhost:30000/v1/models" -> send a HTTP request and show which model is being served, which will tell you the model ID


Step 14: install the Python HTTP library

"python -m pip install requests" (activate the environment before executing the command)


Step 15: create and run the python script 

"nano ~/sglang-project/query.py" -> create the Python script

"python ~/sglang-project/query.py"






























