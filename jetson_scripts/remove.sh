#! /bin/bash

echo "removing data from jetson 1"
sshpass -p "AFRL1D49." ssh -p 22  afrl@192.168.0.150 'cd /home/afrl/Desktop/data; echo "AFRL1D49." | sudo -S rm -r 2*; echo "AFRL1D49." | sudo -S rm -r 1* '

echo "removing data from jetson 2"
sshpass -p "AFRL1D49." ssh -p 22 afrl@192.168.0.100 'cd /home/afrl/Desktop/data; echo "AFRL1D49." | sudo -S rm -r 2*; echo "AFRL1D49." | sudo -S rm -r 1*'
