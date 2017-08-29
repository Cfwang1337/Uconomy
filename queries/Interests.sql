with element_reference AS
        (SELECT "element_id"
              ,"element_name"
              ,"description"
          FROM "content_model_reference"),

        job_titles AS
        (SELECT "onetsoc_code"
              ,"title"
              ,"description"
          FROM "occupation_data"),

        to_pivot AS
        (SELECT "interests"."onetsoc_code"
              ,title
			  ,job_titles."description"
              ,element_name
              ,((data_value - 0)/(7-0)) AS data_value_normalized
          FROM "interests"
          LEFT JOIN element_reference ON interests.element_id = element_reference.element_id
          LEFT JOIN job_titles ON "interests".onetsoc_code = job_titles.onetsoc_code
          WHERE scale_id = 'OI'),


        holland AS
        (SELECT
            to_pivot.onetsoc_code,
            title,
			description,
            MAX(CASE WHEN element_name = 'Realistic' THEN data_value_normalized ELSE NULL END) AS realistic,
            MAX(CASE WHEN element_name = 'Investigative' THEN data_value_normalized ELSE NULL END) AS investigative,
            MAX(CASE WHEN element_name = 'Artistic' THEN data_value_normalized ELSE NULL END) AS artistic,
            MAX(CASE WHEN element_name = 'Social' THEN data_value_normalized ELSE NULL END) AS social,
            MAX(CASE WHEN element_name = 'Enterprising' THEN data_value_normalized ELSE NULL END) AS enterprising,
            MAX(CASE WHEN element_name = 'Conventional' THEN data_value_normalized ELSE NULL END) AS conventional
        FROM
            to_pivot
        GROUP BY
            onetsoc_code, title, description)

        SELECT
            holland.onetsoc_code,
            title,
            "description",
            realistic,
            investigative,
            artistic,
            social,
            enterprising,
            conventional
        FROM holland
