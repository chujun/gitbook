

```
show engine innodb status;
```

在mysql5.7版本上面输出的完整内容(除了简化了过多的TRANSACTIONS)
```
***************************[ 1. row ]***************************
Type   | InnoDB
Name   |
Status |
=====================================
2020-12-18 11:38:39 0x7f8befff6700 INNODB MONITOR OUTPUT
=====================================
Per second averages calculated from the last 35 seconds
-----------------
BACKGROUND THREAD
-----------------
srv_master_thread loops: 2710875 srv_active, 0 srv_shutdown, 106 srv_idle
srv_master_thread log flush and writes: 2710981
----------
SEMAPHORES
----------
OS WAIT ARRAY INFO: reservation count 693002
OS WAIT ARRAY INFO: signal count 914680
RW-shared spins 0, rounds 2561935, OS waits 575646
RW-excl spins 0, rounds 3971774, OS waits 7535
RW-sx spins 12645, rounds 182765, OS waits 469
Spin rounds per wait: 2561935.00 RW-shared, 3971774.00 RW-excl, 14.45 RW-sx
------------------------
LATEST FOREIGN KEY ERROR
------------------------
2020-11-23 20:55:01 0x7f8bfdb36700 Transaction:
TRANSACTION 3864087190, ACTIVE 0 sec inserting
mysql tables in use 1, locked 1
2 lock struct(s), heap size 1136, 0 row lock(s), undo log entries 1
MySQL thread id 676078, OS thread handle 140239233574656, query id 266025047 10.184.12.8 ahs_user update
/* ApplicationName=DataGrip 2020.2.3 */ insert into annotate_file (task_id,
                           original_file_url,
                           algorithm_annotation,
                           manual_annotation,
                           manual_annotation_count,
                           tag,
                           type,
                           difficulty_level,
                           operator_id,
                           operator_name,
                           create_dt,
                           update_dt,
                           description)
    VALUE
Foreign key constraint fails for table `creative_ai_training`.`annotate_file`:
,
  CONSTRAINT `FKomunqyiflergyqo8j32mvpihk` FOREIGN KEY (`task_id`) REFERENCES `annotate_task` (`id`)

  Trying to add in child table, in index idx_task_id tuple:
DATA TUPLE: 2 fields;
 0: len 4; hex 80000812; asc     ;;
 1: len 4; hex 800007d2; asc     ;;

But in parent table `creative_ai_training`.`annotate_task`, in index PRIMARY,
the closest match we can find is record:
PHYSICAL RECORD: n_fields 14; compact format; info bits 0
 0: len 4; hex 800007d2; asc     ;;
 1: len 6; hex 0000dc297007; asc    )p ;;
 2: len 7; hex 2200009e0c1c77; asc "     w;;
 3: len 1; hex 87; asc  ;;
 4: len 0; hex ; asc ;;
 5: len 4; hex 56302e32; asc V0.2;;
 6: len 1; hex 85; asc  ;;
 7: len 24; hex 356639626331646630383334623430303163353732653062; asc 5f9bc1df0834b4001c572e0b;;
 8: len 1; hex 83; asc  ;;
 9: len 4; hex 80000207; asc     ;;
 10: len 23; hex e5b8b8e6a091e69e9728427566666572746368616e6729; asc          (Buffertchang);;
 11: len 5; hex 99a7bd05dc; asc      ;;
 12: len 5; hex 99a7c5157b; asc     {;;
 13: SQL NULL;

------------
TRANSACTIONS
------------
Trx id counter 4049098321
Purge done for trx's n:o < 4049098321 undo n:o < 0 state: running but idle
History list length 0
LIST OF TRANSACTIONS FOR EACH SESSION:
---TRANSACTION 421717718728464, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
---TRANSACTION 421717718722080, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
---TRANSACTION 421717718719344, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
---TRANSACTION 421717718609904, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
---TRANSACTION 421717718761296, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
---TRANSACTION 421717718754000, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
---TRANSACTION 421717718711136, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
---TRANSACTION 421717718667360, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
---TRANSACTION 421717718608992, not started
0 lock struct(s), heap size 1136, 0 row lock(s)

---TRANSACTION 421717718604432, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
---TRANSACTION 421717718631792, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
---TRANSACTION 421717718804160, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
---TRANSACTION 421717718811456, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
---TRANSACTION 421717718806896, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
---TRANSACTION 421717718789568, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
---TRANSACTION 421717718768592, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
---TRANSACTION 421717718764032, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
---TRANSACTION 421717718758560, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
---TRANSACTION 421717718736672, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
---TRANSACTION 421717718756736, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
---TRANSACTION 421717718747616, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
---TRANSACTION 421717718713872, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
---TRANSACTION 421717718686512, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
---TRANSACTION 421717718666448, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
---TRANSACTION 421717718646384, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
---TRANSACTION 421717718627232, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
---TRANSACTION 421717718701104, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
---TRANSACTION 421717718707488, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
---TRANSACTION 421717718748528, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
---TRANSACTION 421717718733024, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
---TRANSACTION 421717718690160, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
---TRANSACTION 421717718606256, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
---TRANSACTION 421717718665536, not started
0 lock struct(s), heap size 1136, 0 row lock(s)
.....
0 lock struct(s), heap size 1136, 0 row lock(s)
--------
FILE I/O
--------
I/O thread 0 state: waiting for i/o request (insert buffer thread)
I/O thread 1 state: waiting for i/o request (log thread)
I/O thread 2 state: waiting for i/o request (read thread)
I/O thread 3 state: waiting for i/o request (read thread)
I/O thread 4 state: waiting for i/o request (read thread)
I/O thread 5 state: waiting for i/o request (read thread)
I/O thread 6 state: waiting for i/o request (write thread)
I/O thread 7 state: waiting for i/o request (write thread)
I/O thread 8 state: waiting for i/o request (write thread)
I/O thread 9 state: waiting for i/o request (write thread)
Pending normal aio reads: [0, 0, 0, 0] , aio writes: [0, 0, 0, 0] ,
 ibuf aio reads:, log i/o's:, sync i/o's:
Pending flushes (fsync) log: 0; buffer pool: 0
17132022 OS file reads, 129093260 OS file writes, 126183733 OS fsyncs
0.03 reads/s, 16384 avg bytes/read, 36.86 writes/s, 35.83 fsyncs/s
-------------------------------------
INSERT BUFFER AND ADAPTIVE HASH INDEX
-------------------------------------
Ibuf: size 1, free list len 2868, seg size 2870, 51092 merges
merged operations:
 insert 190082, delete mark 1752108, delete 179595
discarded operations:
 insert 0, delete mark 0, delete 0
Hash table size 763771, node heap has 127 buffer(s)
Hash table size 763771, node heap has 1156 buffer(s)
Hash table size 763771, node heap has 552 buffer(s)

Hash table size 763771, node heap has 528 buffer(s)
Hash table size 763771, node heap has 980 buffer(s)
Hash table size 763771, node heap has 264 buffer(s)
Hash table size 763771, node heap has 2229 buffer(s)
Hash table size 763771, node heap has 1328 buffer(s)
2459.64 hash searches/s, 1408.79 non-hash searches/s
---
LOG
---
Log sequence number 2992140559934
Log flushed up to   2992140557755
Pages flushed up to 2991952365634
Last checkpoint at  2991952365634
0 pending log flushes, 0 pending chkp writes
125605471 log i/o's done, 35.60 log i/o's/second
----------------------
BUFFER POOL AND MEMORY
----------------------
Total large memory allocated 3160866816
Dictionary memory allocated 15070482
Buffer pool size   188416
Free buffers       1024
Database pages     180228
Old database pages 66509
Modified db pages  3119
Pending reads      0
Pending writes: LRU 0, flush list 0, single page 0
Pages made young 36123139, not young 568550733
0.00 youngs/s, 0.00 non-youngs/s
Pages read 17129587, created 958702, written 3211647
0.00 reads/s, 0.00 creates/s, 0.00 writes/s
Buffer pool hit rate 1000 / 1000, young-making rate 0 / 1000 not 0 / 1000
Pages read ahead 0.00/s, evicted without access 0.00/s, Random read ahead 0.00/s
LRU len: 180228, unzip_LRU len: 0
I/O sum[139]:cur[1], unzip sum[0]:cur[0]
--------------
ROW OPERATIONS
--------------
0 queries inside InnoDB, 0 queries in queue
0 read views open inside InnoDB
Process ID=33113, Main thread ID=140239054030592, state: sleeping
Number of rows inserted 2583680654, updated 103606119, deleted 20696983, read 158041809970
1016.83 inserts/s, 27.86 updates/s, 5.14 deletes/s, 49013.23 reads/s
----------------------------
END OF INNODB MONITOR OUTPUT
============================
```