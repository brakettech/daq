
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
    ngrok tcp  --region=us --remote-addr braket@1.tcp.ngrok.io:22084 22
}

# daq to connect to remote (windows) machine
daq.remote() {
    ssh rob@1.tcp.ngrok.io -p 22084

}

# daq to connect to remote (windows) machine
daq.cd() {
    cd ~/daq_server/

}
############ END DAQ FUNCTIONS #############################



