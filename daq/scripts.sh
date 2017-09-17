
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
    daq.init
    daq.cd
    daq.configure
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
    gunicorn daq.wsgi -b 0.0.0.0:8888

}

# print command usage to console
daq.help() {
    echo
    echo ======================================================================
    echo DAQ COMMANDS
    echo
    echo ----------------------------------------------------------------------
    echo COMMONLY USED COMMANDS
    echo
    echo "daq.server     # start the daq server"
    echo
    echo "daq.init       # set conda to the daq python install"
    echo
    echo "daq.ngrok      # allow ngrok access to this computer"
    echo
    echo "daq.backup     # dump the database to a json file in the dbdump directory"
    echo
    echo
    echo ----------------------------------------------------------------------
    echo RARELY USED COMMANDS
    echo
    echo "daq.cd         # change to the daq server directory"
    echo
    echo "daq.configure  # Do initial server setup"
    echo
    echo "daq.infect     # alter the .bashrc to have non-python daq commands"
    echo
    echo "daq.remote     # command run by another computer to log into this one"
    echo
    echo "daq.update     # update to the most recent software versions"
    echo
    echo "daq.version    # print the current daq version"

}

############ END DAQ FUNCTIONS #############################



