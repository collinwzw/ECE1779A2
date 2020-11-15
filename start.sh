#!/bin/bash
manager_dir='.ECE1779A2Qiwei'
auto_scaling_dir='autoscaling'

cd $manage_dir && python3 ResourceManager.py &> manage.log &
cd $manage_dir/$auto_scaling_dir && python3 autoscaling.py &> autoscaling.log &