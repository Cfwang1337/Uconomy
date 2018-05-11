WITH ed_ref AS
(SELECT
 scale_id,
 category,
 category_description
 FROM ete_categories
 WHERE scale_id = 'RL'),
 
 occupations AS
 (SELECT
 onetsoc_code,
 title,
 description
 from occupation_data),
 
 pre_group AS 
 (SELECT
 education_training_experience.onetsoc_code,
 title,
 description,
 education_training_experience.category,
 category_description,
 data_value
 FROM education_training_experience
 RIGHT JOIN ed_ref ON ed_ref.scale_id = education_training_experience.scale_id AND ed_ref.category = education_training_experience.category
RIGHT JOIN occupations ON occupations.onetsoc_code = education_training_experience.onetsoc_code)

SELECT
onetsoc_code,
title,
CASE WHEN SUM(data_value) > 50 THEN 'Noncollege' ELSE 'College' END AS education_level
FROM pre_group
WHERE
category < 6
GROUP BY onetsoc_code, title

