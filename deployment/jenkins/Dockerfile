# Base Jenkins LTS with JDK 21 (Based on Debian Bookworm)
FROM jenkins/jenkins:lts-jdk21


# Switch to root to install packages
USER root


# 1. Install basic tools and prerequisites for adding external repositories
#    Added python3 and python-is-python3 so 'python' command works for your DAG script
RUN apt-get update && \
    apt-get install -y \
        ca-certificates \
        curl \
        gnupg \
        lsb-release \
        git \
        openssh-client \
        sudo \
        vim \
        unzip \
        python3 \
        python3-pip \
        python3-venv \
        python-is-python3 \
    && rm -rf /var/lib/apt/lists/*


# 2. Add Docker's Official GPG Key
RUN mkdir -p /etc/apt/keyrings && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    chmod a+r /etc/apt/keyrings/docker.gpg


# 3. Add Docker's Official Repository
RUN echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null


# 4. Install the specific 'docker-ce-cli' package
#    This gets the latest version (e.g., v27.x) compatible with Windows Docker Desktop
RUN apt-get update && \
    apt-get install -y docker-ce-cli && \
    rm -rf /var/lib/apt/lists/*


# Create Docker group and add Jenkins user (Standard practice, though TCP bypasses this need)
RUN groupadd -for -g 999 docker && \
    usermod -aG docker jenkins


# Create .ssh folder for Jenkins and add GitHub to known_hosts
RUN mkdir -p /var/jenkins_home/.ssh && \
    ssh-keyscan -t ed25519 github.com >> /var/jenkins_home/.ssh/known_hosts && \
    chown -R jenkins:jenkins /var/jenkins_home/.ssh && \
    chmod 700 /var/jenkins_home/.ssh && \
    chmod 644 /var/jenkins_home/.ssh/known_hosts


# Switch back to Jenkins user
USER jenkins


# Set working directory
WORKDIR /var/jenkins_home


# Expose Jenkins ports
EXPOSE 8080 50000