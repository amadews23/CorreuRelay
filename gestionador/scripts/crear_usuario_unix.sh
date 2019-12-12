#!/bin/bash
useradd $1 -m -s /bin/bash
echo -e "$2\n$2" | passwd $1
