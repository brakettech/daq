
############ DAQ FUNCTIONS #############################
# function to put daq tools on the path\n
daq.init() {
    export PATH="$HOME/miniconda/bin:$PATH"
    export PATH="$HOME/miniconda3/bin:$PATH"
    export PATH="$HOME/anaconda/bin:$PATH"
    export PATH="$HOME/anaconda3/bin:$PATH"
    export PATH=/Users/rob/anaconda3/bin:$PATH
    . activate daq
}

# function that allows remote ssh access via ngrok
daq.ngrok() {
    sudo service ssh --full-restart
    ngrok tcp  --log stdout --region=us --remote-addr braket@1.tcp.ngrok.io:22084 22
}

# command to connect to remote (windows) machine
daq.remote() {
    ssh rob@1.tcp.ngrok.io -p 22084

}

# command to connect to remote (windows) machine
daq.cd() {
    cd ~/daq_server/

}

# command to start server
daq.server() {
    echo
    echo
    echo ===============================================
    echo
    echo Point your browser to http://localhost:8888
    echo
    echo ctrl-c to shut-down server
    echo
    echo ===============================================
    echo
    daq.cd
    gunicorn daq.wsgi -b 0.0.0.0:8888

}

############ END DAQ FUNCTIONS #############################



