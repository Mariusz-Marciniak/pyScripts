import time
import os
import subprocess
import decorateSqlFile

mysql_user = "clw"
mysql_password = "myclw"
archive_dumps_path = "/home/mariusz/Downloads/dumps"

def previous_day_to_string() :
	prev_day = time.localtime(time.time() - 60*60*24*2)
	return time.strftime("%Y_%m_%d", prev_day)

previous_day =  previous_day_to_string()

def interview() :
	options_map = {}
	do_backup = raw_input("BACKUP: Do you want to create backup [y/n]:")
	if(do_backup.upper() == 'Y'):
		host = raw_input("BACKUP: Please input host name (default: slodzarchdb01):")
		if host=="":
			host = "slodzarchdb01"
		options_map["bck_host"] = host
		
		b_db = raw_input("BACKUP: Please input database name (default: clw):")
		if b_db=="":
			# b_db = "clw_production_%s" % previous_day
			b_db = "clw"
		options_map["bck_db"] = b_db
		
                b_trustees = raw_input("BACKUP: Please specify trustees to backup (default: 141,371,416,421,451,506,521,561,646,691,776,781):")
                if b_trustees=="":
                        b_trustees = "141,371,416,421,451,506,521,561,646,691,776,781"
                options_map["bck_trustees"] = b_trustees

	
		do_restore = raw_input("RESTORE: Do you want to restore backup on local server [y/n]:")
		if(do_restore.upper() == 'Y'):
			r_db = raw_input("RESTORE: Please input database name (default: clw):")
			if r_db=="":
				r_db = "clw"
			options_map["restore_db"] = r_db 

		do_archive = raw_input("ARCHIVE: Do you want to archive backup file [y/n]:")
		if(do_archive.upper() == 'Y'):
			default_name = "%s.sql" % previous_day
			file = raw_input("ARCHIVE: Please input backup file name [%s]:" % default_name)
			if file=="":
				file = default_name
			options_map["archive_file"] = file
	else :
		do_restore_from_file = raw_input("RESTORE FROM FILE: Do you want to restore backup from file [y/n]:")
		if(do_restore_from_file.upper() == 'Y'):
			r_file_path = raw_input("RESTORE FROM FILE: Enter file path:")
			options_map["restore_from_file"] = r_file_path
			r_db = raw_input("RESTORE FROM FILE: Please input database name (default: clw):")
			if r_db=="":
				r_db = "clw"
			options_map["restore_db"] = r_db
	return options_map

def backup(host, db, trustees) :
	filepath = "%s/%s.sql" % (archive_dumps_path, time.time())
	backup_command = "./dumptool/dump_trustee.sh -h %s -u %s -p %s -d %s -t %s -o %s" % (host, mysql_user, mysql_password, db, trustees, filepath)
	print ("Backup in progress. Please wait...")
	subprocess.call(backup_command, shell=True)
	print("Operation finished")

	return filepath

def restore(path, db) :
	restore_command = "mysql -u %s -p%s %s < %s" % (mysql_user, mysql_password, db, path)
	print ("Restore in progress. Please wait...")
	subprocess.call(restore_command, shell=True)
	print("Operation finished")

def archive_backup(path, file) :
	print("Archiving...")
	os.system("cat %s > %s/%s" % (path, archive_dumps_path, file))
	print("Archive done")

def remove(path) :
	os.remove(path)

options_map = interview()
if("bck_host" in options_map):
	path = backup(options_map["bck_host"],options_map["bck_db"], options_map["bck_trustees"])
        if("archive_file" in options_map):
                archive_backup(path, options_map["archive_file"])

	if("restore_db" in options_map):
		restore(path, options_map["restore_db"])
	
	remove(path)
elif("restore_from_file" in options_map):
	restore(options_map["restore_from_file"], options_map["restore_db"])
