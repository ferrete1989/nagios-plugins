#!/usr/bin/env python

try:
	import redis
	import datetime
except Exception:
	msg= 'WARNING: Please check deps'
	ret=1
	print msg 
	exit(ret)

def getTimeOfSettingValue(conn, key, value):
	before_set_time = datetime.datetime.now()
	conn.set(key,value)
	set_time = (datetime.datetime.now() - before_set_time).total_seconds()
	return set_time

def getTimeOfGettingValue(conn, key):
	before_get_time = datetime.datetime.now()
	conn.get(key)
	get_time = (datetime.datetime.now() - before_get_time).total_seconds()
	return get_time

def getTimeOfDeletingValue(conn, key):
	before_delete_time = datetime.datetime.now()
	conn.delete(key)
	delete_time = (datetime.datetime.now() - before_delete_time).total_seconds()
	if conn.get(key):
		msg = "CRITICAL: Test value is already stored after delete it."
		ret = 2
		print msg
		exit(ret)
	return delete_time

def printResultMessage(times):
	msg = "OK: Conn time: " + str(times[0]) + ". Set time: " + str(times[1]) + ". Get time: " + str(times[2]) + ". Delete time: " + str(times[3])
	ret = 0
	print msg
	exit(ret)

if __name__ == '__main__':

	host = "localhost"
	password = ""
	key = "check_redis_testkey"
	value = 1

	try:
		before_conn_time = datetime.datetime.now()
		conn = redis.Redis(host=host,password=password)
		conn_time = (datetime.datetime.now() - before_conn_time).total_seconds()
		set_time = getTimeOfSettingValue(conn,key,value)
		get_time = getTimeOfGettingValue(conn,key)
		delete_time = getTimeOfDeletingValue(conn,key)
		times = [conn_time,set_time,get_time,delete_time]
		printResultMessage(times)
	except Exception as exc:
		msg = "CRITICAL: " + str(exc)
		ret = 2
		print msg
		exit(ret)
