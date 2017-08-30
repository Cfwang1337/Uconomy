-- CREATE extension tablefunc;

WITH pivoted AS
(
SELECT * FROM crosstab(
'WITH scales as
(SELECT "scale_id"
      ,"scale_name"
      ,"minimum"
      ,"maximum"
  FROM "scales_reference"),

elements_ref as
 (SELECT "element_id"
      ,"element_name"
      ,"description"
  FROM "content_model_reference"),

skill_category AS

(SELECT "element_id" as category_id
      ,"element_name" as category_name
      ,"description" as category_description
  FROM "content_model_reference"
  WHERE LENGTH(element_id) = 5),

skill_broad_category AS

(SELECT "element_id" as broad_category_id
      ,"element_name" as broad_category_name
      ,"description" as broad_category_description
  FROM "content_model_reference"
  WHERE LENGTH(element_id) = 3),

final_ref AS
(SELECT abilities."onetsoc_code"
	  ,category_name
	  ,broad_category_name
      ,elements_ref."element_id"
	  ,element_name
      ,elements_ref."description"
	  ,scales."scale_id"
	  ,scale_name
      ,"data_value"
    ,''Abilities'' as category
  FROM abilities
  LEFT JOIN scales ON scales.scale_id = abilities.scale_id
  LEFT JOIN elements_ref on elements_ref.element_id = abilities.element_id
  LEFT JOIN occupation_data ON occupation_data.onetsoc_code = abilities.onetsoc_code
  LEFT JOIN skill_category ON skill_category.category_id = LEFT(abilities.element_id, 5)
  LEFT JOIN skill_broad_category ON skill_broad_category.broad_category_id = LEFT(abilities.element_id, 3)
UNION
SELECT skills."onetsoc_code"
	  ,category_name
	  ,broad_category_name
      ,elements_ref."element_id"
	  ,element_name
      ,elements_ref."description"
	  ,scales."scale_id"
	  ,scale_name
      ,"data_value"
    ,''Skills'' as category
  FROM skills
  LEFT JOIN scales ON scales.scale_id = skills.scale_id
  LEFT JOIN elements_ref on elements_ref.element_id = skills.element_id
  LEFT JOIN occupation_data ON occupation_data.onetsoc_code = skills.onetsoc_code
  LEFT JOIN skill_category ON skill_category.category_id = LEFT(skills.element_id, 5)
  LEFT JOIN skill_broad_category ON skill_broad_category.broad_category_id = LEFT(skills.element_id, 3)
UNION
SELECT knowledge."onetsoc_code"
	  ,category_name
	  ,broad_category_name
      ,elements_ref."element_id"
	  ,element_name
      ,elements_ref."description"
	  ,scales."scale_id"
	  ,scale_name
      ,"data_value"
    ,''Knowledge'' as category
  FROM knowledge
  LEFT JOIN scales ON scales.scale_id = knowledge.scale_id
  LEFT JOIN elements_ref on elements_ref.element_id = knowledge.element_id
  LEFT JOIN skill_category ON skill_category.category_id = LEFT(knowledge.element_id, 5)
  LEFT JOIN skill_broad_category ON skill_broad_category.broad_category_id = LEFT(knowledge.element_id, 3)
  ),

ska_importance AS (SELECT
       "onetsoc_code"
	  ,broad_category_name
	  ,category_name
      ,"element_id"
	  ,category || '' - '' || category_name || '' - '' || element_name AS element_name
      ,"description"
	  ,"scale_id"
	  ,scale_name
      ,"data_value"
  ,((data_value - 0)/(7-0)) AS data_value_normalized
  FROM final_ref
  WHERE scale_name = ''Importance''
),

ska_level AS (SELECT
       "onetsoc_code"
	  ,broad_category_name
	  ,category_name
      ,"element_id"
	  ,category || '' - '' || category_name || '' - '' || element_name AS element_name
      ,"description"
	  ,"scale_id"
	  ,scale_name
      ,"data_value"
  ,((data_value - 0)/(7-0)) AS data_value_normalized
  FROM final_ref
  WHERE scale_name = ''Level''
),

preprocess AS
(
SELECT
ska_level.onetsoc_code,
ska_level.element_name,
(ska_level.data_value_normalized + ska_importance.data_value_normalized)/2 AS product_normalized
FROM ska_level
LEFT JOIN ska_importance on ska_importance.onetsoc_code = ska_level.onetsoc_code
AND ska_importance.element_name = ska_level.element_name)

SELECT
onetsoc_code,
element_name,
product_normalized
FROM
preprocess
ORDER BY 1,2')
AS pivoted(
onetsoc_code CHARACTER(10),
"Abilities - Cognitive Abilities - Category Flexibility" NUMERIC,
"Abilities - Cognitive Abilities - Deductive Reasoning" NUMERIC,
"Abilities - Cognitive Abilities - Flexibility of Closure" NUMERIC,
"Abilities - Cognitive Abilities - Fluency of Ideas" NUMERIC,
"Abilities - Cognitive Abilities - Inductive Reasoning" NUMERIC,
"Abilities - Cognitive Abilities - Information Ordering" NUMERIC,
"Abilities - Cognitive Abilities - Mathematical Reasoning" NUMERIC,
"Abilities - Cognitive Abilities - Memorization" NUMERIC,
"Abilities - Cognitive Abilities - Number Facility" NUMERIC,
"Abilities - Cognitive Abilities - Oral Comprehension" NUMERIC,
"Abilities - Cognitive Abilities - Oral Expression" NUMERIC,
"Abilities - Cognitive Abilities - Originality" NUMERIC,
"Abilities - Cognitive Abilities - Perceptual Speed" NUMERIC,
"Abilities - Cognitive Abilities - Problem Sensitivity" NUMERIC,
"Abilities - Cognitive Abilities - Selective Attention" NUMERIC,
"Abilities - Cognitive Abilities - Spatial Orientation" NUMERIC,
"Abilities - Cognitive Abilities - Speed of Closure" NUMERIC,
"Abilities - Cognitive Abilities - Time Sharing" NUMERIC,
"Abilities - Cognitive Abilities - Visualization" NUMERIC,
"Abilities - Cognitive Abilities - Written Comprehension" NUMERIC,
"Abilities - Cognitive Abilities - Written Expression" NUMERIC,
"Abilities - Physical Abilities - Dynamic Flexibility" NUMERIC,
"Abilities - Physical Abilities - Dynamic Strength" NUMERIC,
"Abilities - Physical Abilities - Explosive Strength" NUMERIC,
"Abilities - Physical Abilities - Extent Flexibility" NUMERIC,
"Abilities - Physical Abilities - Gross Body Coordination" NUMERIC,
"Abilities - Physical Abilities - Gross Body Equilibrium" NUMERIC,
"Abilities - Physical Abilities - Stamina" NUMERIC,
"Abilities - Physical Abilities - Static Strength" NUMERIC,
"Abilities - Physical Abilities - Trunk Strength" NUMERIC,
"Abilities - Psychomotor Abilities - Arm-Hand Steadiness" NUMERIC,
"Abilities - Psychomotor Abilities - Control Precision" NUMERIC,
"Abilities - Psychomotor Abilities - Finger Dexterity" NUMERIC,
"Abilities - Psychomotor Abilities - Manual Dexterity" NUMERIC,
"Abilities - Psychomotor Abilities - Multilimb Coordination" NUMERIC,
"Abilities - Psychomotor Abilities - Rate Control" NUMERIC,
"Abilities - Psychomotor Abilities - Reaction Time" NUMERIC,
"Abilities - Psychomotor Abilities - Response Orientation" NUMERIC,
"Abilities - Psychomotor Abilities - Speed of Limb Movement" NUMERIC,
"Abilities - Psychomotor Abilities - Wrist-Finger Speed" NUMERIC,
"Abilities - Sensory Abilities - Auditory Attention" NUMERIC,
"Abilities - Sensory Abilities - Depth Perception" NUMERIC,
"Abilities - Sensory Abilities - Far Vision" NUMERIC,
"Abilities - Sensory Abilities - Glare Sensitivity" NUMERIC,
"Abilities - Sensory Abilities - Hearing Sensitivity" NUMERIC,
"Abilities - Sensory Abilities - Near Vision" NUMERIC,
"Abilities - Sensory Abilities - Night Vision" NUMERIC,
"Abilities - Sensory Abilities - Peripheral Vision" NUMERIC,
"Abilities - Sensory Abilities - Sound Localization" NUMERIC,
"Abilities - Sensory Abilities - Speech Clarity" NUMERIC,
"Abilities - Sensory Abilities - Speech Recognition" NUMERIC,
"Abilities - Sensory Abilities - Visual Color Discrimination" NUMERIC,
"Knowledge - Arts and Humanities - English Language" NUMERIC,
"Knowledge - Arts and Humanities - Fine Arts" NUMERIC,
"Knowledge - Arts and Humanities - Foreign Language" NUMERIC,
"Knowledge - Arts and Humanities - History and Archeology" NUMERIC,
"Knowledge - Arts and Humanities - Philosophy and Theology" NUMERIC,
"Knowledge - Business and Management - Administration and Management" NUMERIC,
"Knowledge - Business and Management - Clerical" NUMERIC,
"Knowledge - Business and Management - Customer and Personal Service" NUMERIC,
"Knowledge - Business and Management - Economics and Accounting" NUMERIC,
"Knowledge - Business and Management - Personnel and Human Resources" NUMERIC,
"Knowledge - Business and Management - Sales and Marketing" NUMERIC,
"Knowledge - Business and Management - Transportation" NUMERIC,
"Knowledge - Communications - Communications and Media" NUMERIC,
"Knowledge - Communications - Telecommunications" NUMERIC,
"Knowledge - Education and Training - Education and Training" NUMERIC,
"Knowledge - Engineering and Technology - Building and Construction" NUMERIC,
"Knowledge - Engineering and Technology - Computers and Electronics" NUMERIC,
"Knowledge - Engineering and Technology - Design" NUMERIC,
"Knowledge - Engineering and Technology - Engineering and Technology" NUMERIC,
"Knowledge - Engineering and Technology - Mechanical" NUMERIC,
"Knowledge - Health Services - Medicine and Dentistry" NUMERIC,
"Knowledge - Health Services - Therapy and Counseling" NUMERIC,
"Knowledge - Law and Public Safety - Law and Government" NUMERIC,
"Knowledge - Law and Public Safety - Public Safety and Security" NUMERIC,
"Knowledge - Manufacturing and Production - Food Production" NUMERIC,
"Knowledge - Manufacturing and Production - Production and Processing" NUMERIC,
"Knowledge - Mathematics and Science - Biology" NUMERIC,
"Knowledge - Mathematics and Science - Chemistry" NUMERIC,
"Knowledge - Mathematics and Science - Geography" NUMERIC,
"Knowledge - Mathematics and Science - Mathematics" NUMERIC,
"Knowledge - Mathematics and Science - Physics" NUMERIC,
"Knowledge - Mathematics and Science - Psychology" NUMERIC,
"Knowledge - Mathematics and Science - Sociology and Anthropology" NUMERIC,
"Skills - Complex Problem Solving Skills - Complex Problem Solving" NUMERIC,
"Skills - Content - Active Listening" NUMERIC,
"Skills - Content - Mathematics" NUMERIC,
"Skills - Content - Reading Comprehension" NUMERIC,
"Skills - Content - Science" NUMERIC,
"Skills - Content - Speaking" NUMERIC,
"Skills - Content - Writing" NUMERIC,
"Skills - Process - Active Learning" NUMERIC,
"Skills - Process - Critical Thinking" NUMERIC,
"Skills - Process - Learning Strategies" NUMERIC,
"Skills - Process - Monitoring" NUMERIC,
"Skills - Resource Management Skills - Management of Financial Resources" NUMERIC,
"Skills - Resource Management Skills - Management of Material Resources" NUMERIC,
"Skills - Resource Management Skills - Management of Personnel Resources" NUMERIC,
"Skills - Resource Management Skills - Time Management" NUMERIC,
"Skills - Social Skills - Coordination" NUMERIC,
"Skills - Social Skills - Instructing" NUMERIC,
"Skills - Social Skills - Negotiation" NUMERIC,
"Skills - Social Skills - Persuasion" NUMERIC,
"Skills - Social Skills - Service Orientation" NUMERIC,
"Skills - Social Skills - Social Perceptiveness" NUMERIC,
"Skills - Systems Skills - Judgment and Decision Making" NUMERIC,
"Skills - Systems Skills - Systems Analysis" NUMERIC,
"Skills - Systems Skills - Systems Evaluation" NUMERIC,
"Skills - Technical Skills - Equipment Maintenance" NUMERIC,
"Skills - Technical Skills - Equipment Selection" NUMERIC,
"Skills - Technical Skills - Installation" NUMERIC,
"Skills - Technical Skills - Operation and Control" NUMERIC,
"Skills - Technical Skills - Operation Monitoring" NUMERIC,
"Skills - Technical Skills - Operations Analysis" NUMERIC,
"Skills - Technical Skills - Programming" NUMERIC,
"Skills - Technical Skills - Quality Control Analysis" NUMERIC,
"Skills - Technical Skills - Repairing" NUMERIC,
"Skills - Technical Skills - Technology Design" NUMERIC,
"Skills - Technical Skills - Troubleshooting" NUMERIC))

SELECT * FROM pivoted
