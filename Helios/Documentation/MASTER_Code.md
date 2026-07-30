```hls

type MASTER
group MG_MasterServer

import configmanager 
import poolmanager 
import systemutils as su
import math
import fs

cat startup {

	set su.status 0

	create cfg = fs.load(loose=true; “./config/cfg.txt" )
	i16 cf_len = cfg.lenb() 
	set cfg.release = true 
	
	set algorithm su.algorithm.random() # for creation signature generation

	create IWST = new(ntree())  # Internal Worker Slave n-ary Tree :
	create SWORKER(pid=003) as swcfg 
	create SWORKER(pid=002) as swpm
	create CHILDMANAGER = su.manager(IWST) as mcm 
	# gives spawn(), kill(), dig(), search(pid), jump() and separate() functions for process management.



	swcfg.initialize(configmanager.type.main; i32 new( algorithm.generate()) ) 
	# only referenced, not called or run.
	swpm.initialize(poolmanager.type.main; i32 new(algorithm.generate())) 

	mcm.proc.spawn(swcfg)  #adds the workers to the manager
	mcm.proc.spawn(swpm) 


	mcm.proc(pid=003).buffer = new(su.buffer[cf_len])  
	mcm.proc(pid=002).buffer = new(su.buffer[16384]) #16MiB starting pool.
	mcm.proc(pid=002).late_realloc = true     
	mcm.proc(pid=002).search_site = mcm.proc(pid=002).buffer     # source site for reallocation setting - config.

	mcm.proc(pid=002).start()  ||| mcm.proc(pid=002).separate() ||| hold mcm.proc(pid=002)  ||| clutch mcm.proc(pid=002) as mpm 

	#Parallel process: ‘hold’ keeps the assigned variable in context memory till something requests it which then it gives and removes from memory. Sets the swpm to start as soon as the right side executes. Separates swpm from the pipeline by removing it from Master Child Manager and Deleting it's creation_signature. ‘Clutch’ does the same as hold except it keeps a connection open for calls and streams.

	set su.pool mpm.waypoint 

	set su.status 1 
	#switching to running.
	switch running

}


cat running {

}


cat halt {


}


cat exit {


}

```