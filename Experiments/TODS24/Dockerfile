FROM ubuntu:20.04

# Install base utilities
RUN apt-get update
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow
RUN apt-get -y install tzdata
RUN apt-get update && \
    apt-get install -y sudo && \
    apt-get install -y build-essential && \
    apt-get install -y wget && \
    apt-get install -y curl && \
    apt-get install -y bc && \
    apt-get install -y software-properties-common && \
    apt-get install -y unzip
RUN apt-get update

# Install java and maven
RUN apt-get install -y openjdk-11-jdk
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
RUN apt-get install -y maven

# Install PostgeSQL
RUN apt-get install -y lsb-release
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" | tee /etc/apt/sources.list.d/postgresql-pgdg.list > /dev/null
RUN apt-get update && apt-get install -y postgresql-9.5

# Install SQLServer
RUN wget -qO- https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN add-apt-repository "$(wget -qO- https://packages.microsoft.com/config/ubuntu/20.04/mssql-server-2019.list)"
RUN apt-get update && apt-get install -y mssql-server
RUN curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | tee /etc/apt/sources.list.d/msprod.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y mssql-tools unixodbc-dev
ENV PATH="$PATH:/opt/mssql-tools/bin"

# Install screen for running on the background
RUN apt-get install -y screen

# Install miniconda
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda2-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH

# Set working directory
ADD . /app/
WORKDIR /app/

# Set up the python virtual environment
RUN conda env create -f /app/Experiments/environment.yml
RUN echo "source activate anyk_env" > ~/.bashrc
ENV PATH /opt/conda/envs/env/bin:$PATH

# Comile the project and run tests
RUN mvn package

# Run the experiments when the container starts
ENTRYPOINT ["/bin/bash","/app/Experiments/TODS24/start_container.sh"]
