#!/usr/bin/python3
#
# Measures the energy used (in μjoules) while a command was running.
# NOTE: This includes energy for all processes, not just the command.
#       So run this on an otherwise idle machine.
#
# What zones are reported depends on the RAPL zones supported by the 
# hardware.
#
# By Bram Stolk (bram.stolk@canonical.com)

import os
import sys
import subprocess

dirnames = {}

def find_zones():
	cmd = "find /sys/devices/virtual/powercap/intel-rapl -name intel-rapl\:\* -print";
	print(cmd)
	f = os.popen(cmd, "r")
	lines = f.readlines()
	f.close()
	for line in lines:
		line = line.strip()
		nm = line + "/name"
		f = open(nm, "r")
		assert(f)
		name = f.readline().strip()
		f.close()
		dirnames[name] = line
	print("RAPL zones found: ", list(dirnames.keys()))
	return len(dirnames.keys())


def measure():
	energy = {}
	for k in dirnames.keys() :
		nm = dirnames[k] + "/energy_uj"
		f = open(nm, "r")
		line = f.readline().strip()
		uj = int(line)
		f.close()
		energy[k] = uj
	return energy


def report(energy0, energy1) :
	print("Used energy in μjoules:")
	for k in dirnames.keys() :
		e0 = energy0[k]
		e1 = energy1[k]
		assert(e1 >= e0)
		print("%-10s %12d" % (k, e1-e0))


if __name__ == '__main__' :
	if len(sys.argv) < 2 :
		print("Usage:", sys.argv[0], "command")
		sys.exit(1)

	num = find_zones()
	if num == 0 :
		print("No RAPL zones were found. Aborting.")
		sys.exit(2)

	# run the commands
	user = os.environ.get("SUDO_USER")
	assert(user)

	print("start test")
	energy0 = measure()
	result = subprocess.run(["sudo","-u", user] + sys.argv[1:])
	energy1 = measure()
	print("ended test");

	report(energy0, energy1)

