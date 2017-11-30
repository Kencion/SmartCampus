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