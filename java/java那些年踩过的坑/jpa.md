# jpa基本性能需求
* n+1问题
* 懒加载问题


# jpa碰到的那些性能问题坑问题

## 如果解决n+1query
用@BatchSize +Set关联关系

## 查询select in 并不是期望的@BatchSize数量
default-batch-fetch-size-recommended-values
https://stackoverflow.com/questions/21162172/default-batch-fetch-size-recommended-values/21481509#21481509
https://stackoverflow.com/questions/25210949/understanding-batchsize-in-hibernate

## 如何解决@OneToOne lazy 
How can I make a JPA OneToOne relation lazy
https://stackoverflow.com/questions/1444227/how-can-i-make-a-jpa-onetoone-relation-lazy
https://developer.jboss.org/docs/DOC-13960


batchsize=20
1,2,3,4...10,20

44 20+20+4
32 20+10+2
15 10+5
25 20+5
18 10+8
10 


batchsize=120
120, 60, 30, 15, 10, 9, 8, ..., 2, 1

120/2=60
120/2*2=30
120/2*2*2=15

20 15+5
30 30
11 10+1

