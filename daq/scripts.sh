
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
    ngrok tcp --log stdout --region=us --remote-addr 1.tcp.ngrok.io:22084 22
}

daq.update() {
    pip install -U braket-daq
}
