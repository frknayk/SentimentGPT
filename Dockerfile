# Use the official Python 3.9 image
FROM python:3.10
 
# Set the working directory to /code
WORKDIR /code

RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.rpm.sh | bash
RUN yum install git-lfs -y
RUN git lfs install
RUN git clone https://huggingface.co/facebook/bart-large-mnli/tree/main/pytorch_model.bin /tmp/model
COPY /temp/model /app/resources

# Copy the current directory contents into the container at /code
COPY ./requirements.txt /code/requirements.txt
 
# Install requirements.txt 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
 
# Set up a new user named "user" with user ID 1000
RUN useradd -m -u 1000 user
# Switch to the "user" user
USER user
# Set home to the user's home directory
ENV HOME=/home/user \\
    PATH=/home/user/.local/bin:$PATH

# Set the working directory to the user's home directory
WORKDIR $HOME/app
 
# Copy the current directory contents into the container at $HOME/app setting the owner to the user
COPY --chown=user . $HOME/app
 
# Start the FastAPI app on port 7860, the default port expected by Spaces
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]