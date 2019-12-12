#!/bin/bash
usermod -l $1 $2
usermod -d /home/$1 -m $1
groupmod -n $1 $2
