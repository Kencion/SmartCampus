SELECT DISTINCT
	(student_type)
FROM
	students;

UPDATE students
SET student_type = '1'
WHERE
	student_type = '普通高校本科学生';

UPDATE students
SET student_type = '2'
WHERE
	student_type = '硕士研究生';

UPDATE students
SET student_type = '3'
WHERE
	student_type = '交流生';

UPDATE students
SET student_type = '4'
WHERE
	student_type = '博士研究生';

UPDATE students
SET student_type = '5'
WHERE
	student_type = '普通进修生';

UPDATE students
SET student_type = '6'
WHERE
	student_type = '硕士专业学位研究生';

######################################
SELECT DISTINCT
	(hornorary_rank)
FROM
	students;

UPDATE students
SET hornorary_rank = '1'
WHERE
	hornorary_rank = '校级';
######################################
-- SELECT DISTINCT
-- 	(subsidy_rank)
-- FROM
-- 	students;
UPDATE students
SET subsidy_rank = '3'
WHERE
	subsidy_rank = '三等';

UPDATE students
SET subsidy_rank = '2'
WHERE
	subsidy_rank = '二等';

UPDATE students
SET subsidy_rank = '1'
WHERE
	subsidy_rank = '一等';

UPDATE students
SET subsidy_rank = '4'
WHERE
	subsidy_rank = '不分等';
######################################
DELETE
FROM
	students
WHERE
	in_out_times IN (- 1, 0)
OR score_rank IN (0, NULL) 

##############deal_with_table_card##########
UPDATE card
SET type = 'market'
WHERE
	business_name like '%小卖部%' or business_name like '%超市%' 
	or business_name like '%便利店%' or business_name like '%商场%';
	
UPDATE card
SET type = 'other'
WHERE
	business_name like '%洗衣%' or business_name like '%水控%' 
	or business_name like '%家电%' or business_name like '%赵何蒋%'
	or business_name like '%电控%' or business_name like '%药店%'
	or business_name like '%礼品%' or business_name like '%护理%'
	or business_name like '%金淘振芳%' or business_name like '%捐赠%'
	or business_name like '%克立楼总台%'or (transcation_aoumt<0 and business_name is null);
	
UPDATE card
SET type = 'snack'
WHERE
	(business_name like '%小吃%' and business_name not like '%餐厅%')  or business_name like '%外卖%' 
	or business_name like '%快餐%' or business_name like '%刀削面%'
	or business_name like '%糕点%' or business_name like '%卤面%'
	or business_name like '%杭州小笼包%' or business_name like '%韩国铁板烧%'
	or business_name like '%珍珠奶茶%' or business_name like '%全德福%'
	or business_name like '%拉面%' or business_name like '%饮%'
	or business_name like '%好粥到%' or business_name like '%河粉%'
	or business_name like '%美食%' or business_name like '%佳滋味%'
	or business_name like '%快口乐%' or business_name like '%河粉%'
	or business_name like '%咖啡%' or business_name like '%沙茶面%'
	or business_name like '%面包%' ;
	
UPDATE card
SET type = 'canteen'
WHERE
	business_name like '%餐厅%' or business_name like '%食堂%';

UPDATE card
SET type = 'study'
WHERE
	business_name like '%图书馆%' or business_name like '%书屋%'
	or business_name like '%文具%'
	or business_name like '%印%' or business_name like '%书苑%';

UPDATE card
SET type = 'exercise'
WHERE
	business_name like '%高尔夫%' or business_name like '%篮球%'
	or business_name like '%游泳%' or business_name like '%运动%';

UPDATE card
SET type = 'charge'
WHERE
	transcstion_amount>0;