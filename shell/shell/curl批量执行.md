```shell
#!/bin/bash
order_nos=(
'20220310135151210694'
'20220310134342106875'
'20220310134312127600'
'20220310133903771980'
'20220310133554604523'
'20220310133539226493'
'20220310133528687761'
'20220310133156885550'
'20220310133140525053'
'20220310132650454696'
'20220310132620436743'
'20220310132609830627')

for order_no in "${order_nos[@]}"
do
	echo "order_no:$order_no"
	curl --location --request POST 'http://domain/operation' \
		--header 'Content-Type: application/json' \
	--data '{"operatorKey": "0","operatorType": 9,"operatorName": "","operatorId": null,"bizType": 1,"bizKey": "'"${order_no}"'R","lockBizKey": "'"${order_no}"'"}'
done

```