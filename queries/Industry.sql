WITH occupations AS 
(SELECT 
onetsoc_code,
title,
description
FROM occupation_data),


with_rank AS
(SELECT
occupation_level_metadata.onetsoc_code,
title,
response,
percent,
row_number() OVER (PARTITION BY occupation_level_metadata.onetsoc_code, title ORDER BY percent DESC) as rank_percent
FROM
occupation_level_metadata
LEFT JOIN occupations ON occupations.onetsoc_code = occupation_level_metadata.onetsoc_code
WHERE item = 'NAICS Sector'
AND percent > 0)

SELECT * FROM with_rank
ORDER BY percent desc


