-- CREATE extension tablefunc;

WITH pivoted AS
(
SELECT * FROM crosstab(
'WITH 
  elements_ref as
 (SELECT element_id
      ,element_name
  FROM content_model_reference),


scales as
(SELECT scale_id
      ,scale_name
  FROM scales_reference),

activities_ref AS
(SELECT work_activities.onetsoc_code
    ,work_activities.element_id
    ,element_name
      ,work_activities.scale_id
    ,scale_name
  ,data_value
  FROM work_activities
  LEFT JOIN elements_ref ON elements_ref.element_id = work_activities.element_id
  LEFT JOIN scales ON scales.scale_id = work_activities.scale_id),

activity_category AS

(SELECT element_id as category_id
      ,element_name as category_name
  FROM content_model_reference
  WHERE LENGTH(element_id) = 5),

activity_level AS
(SELECT
       onetsoc_code
    ,category_name ||  '' - '' || element_name AS element_name
    ,data_value
    ,((data_value - 0)/(7-0)) AS data_value_normalized
    ,ROW_NUMBER() OVER (PARTITION  BY onetsoc_code ORDER BY data_value DESC) as row_index
  FROM activities_ref
  LEFT JOIN activity_category on activity_category.category_id = LEFT(element_id, 5)
  WHERE scale_name = ''Level''),

activity_importance AS
(SELECT
       onetsoc_code
    ,category_name ||  '' - '' || element_name AS element_name
    ,data_value
    ,((data_value - 0)/(7-0)) AS data_value_normalized
    ,ROW_NUMBER() OVER (PARTITION  BY onetsoc_code ORDER BY data_value DESC) as row_index
  FROM activities_ref
  LEFT JOIN activity_category on activity_category.category_id = LEFT(element_id, 5)
  WHERE scale_name = ''Importance''),
    
preprocess AS
(
SELECT
activity_level.onetsoc_code,
activity_level.element_name,
(activity_level.data_value_normalized + activity_importance.data_value_normalized)/2 AS product_normalized
FROM activity_level
LEFT JOIN activity_importance on activity_importance.onetsoc_code = activity_level.onetsoc_code
AND activity_importance.element_name = activity_level.element_name)
    
SELECT
onetsoc_code,
element_name,
product_normalized
FROM
preprocess
ORDER BY 1,2')
AS pivoted(
onetsoc_code CHARACTER(10),
"Information Input - Estimating the Quantifiable Characteristics of Products, Events, or Information" NUMERIC ,
"Information Input - Getting Information" NUMERIC,
"Information Input - Identifying Objects, Actions, and Events" NUMERIC ,
"Information Input - Inspecting Equipment, Structures, or Material" NUMERIC ,
"Information Input - Monitor Processes, Materials, or Surroundings" NUMERIC ,
"Interacting With Others - Assisting and Caring for Others" NUMERIC ,
"Interacting With Others - Coaching and Developing Others" NUMERIC ,
"Interacting With Others - Communicating with Persons Outside Organization" NUMERIC ,
"Interacting With Others - Communicating with Supervisors, Peers, or Subordinates" NUMERIC ,
"Interacting With Others - Coordinating the Work and Activities of Others" NUMERIC ,
"Interacting With Others - Developing and Building Teams" NUMERIC ,
"Interacting With Others - Establishing and Maintaining Interpersonal Relationships" NUMERIC ,
"Interacting With Others - Guiding, Directing, and Motivating Subordinates" NUMERIC ,
"Interacting With Others - Interpreting the Meaning of Information for Others" NUMERIC ,
"Interacting With Others - Monitoring and Controlling Resources" NUMERIC ,
"Interacting With Others - Performing Administrative Activities" NUMERIC ,
"Interacting With Others - Performing for or Working Directly with the Public" NUMERIC ,
"Interacting With Others - Provide Consultation and Advice to Others" NUMERIC ,
"Interacting With Others - Resolving Conflicts and Negotiating with Others" NUMERIC ,
"Interacting With Others - Selling or Influencing Others" NUMERIC ,
"Interacting With Others - Staffing Organizational Units" NUMERIC ,
"Interacting With Others - Training and Teaching Others" NUMERIC ,
"Mental Processes - Analyzing Data or Information" NUMERIC ,
"Mental Processes - Developing Objectives and Strategies" NUMERIC ,
"Mental Processes - Evaluating Information to Determine Compliance with Standards" NUMERIC ,
"Mental Processes - Judging the Qualities of Things, Services, or People" NUMERIC ,
"Mental Processes - Making Decisions and Solving Problems" NUMERIC ,
"Mental Processes - Organizing, Planning, and Prioritizing Work" NUMERIC ,
"Mental Processes - Processing Information" NUMERIC ,
"Mental Processes - Scheduling Work and Activities" NUMERIC ,
"Mental Processes - Thinking Creatively" NUMERIC ,
"Mental Processes - Updating and Using Relevant Knowledge" NUMERIC ,
"Work Output - Controlling Machines and Processes" NUMERIC ,
"Work Output - Documenting/Recording Information" NUMERIC ,
"Work Output - Drafting, Laying Out, and Specifying Technical Devices, Parts, and Equipment" NUMERIC ,
"Work Output - Handling and Moving Objects" NUMERIC ,
"Work Output - Interacting With Computers" NUMERIC ,
"Work Output - Operating Vehicles, Mechanized Devices, or Equipment" NUMERIC ,
"Work Output - Performing General Physical Activities" NUMERIC ,
"Work Output - Repairing and Maintaining Electronic Equipment" NUMERIC ,
"Work Output - Repairing and Maintaining Mechanical Equipment" NUMERIC)),
    
work_activities AS
(SELECT
onetsoc_code,
(
"Work Output - Performing General Physical Activities" +
"Work Output - Handling and Moving Objects"
)/2 AS physically_demanding,

(
"Information Input - Monitor Processes, Materials, or Surroundings" +
"Information Input - Identifying Objects, Actions, and Events" +
"Information Input - Inspecting Equipment, Structures, or Material"
)/3 AS sensorily_demanding,

(
"Information Input - Getting Information" +
"Information Input - Monitor Processes, Materials, or Surroundings" +
"Mental Processes - Judging the Qualities of Things, Services, or People" +
"Mental Processes - Processing Information" +
"Mental Processes - Analyzing Data or Information" +
"Mental Processes - Making Decisions and Solving Problems" +
"Mental Processes - Thinking Creatively" +
"Mental Processes - Updating and Using Relevant Knowledge" +
"Mental Processes - Developing Objectives and Strategies"
)/9 AS intellectually_demanding_problem_solving,


"Mental Processes - Thinking Creatively"
AS intellectually_demanding_creativity,

"Interacting With Others - Assisting and Caring for Others"
AS people_caring,

(
"Interacting With Others - Training and Teaching Others" +
"Interacting With Others - Coaching and Developing Others")
/2 AS people_teaching_and_instructing,

(
"Interacting With Others - Performing for or Working Directly with the Public" +
"Interacting With Others - Selling or Influencing Others" +
"Interacting With Others - Communicating with Persons Outside Organization"
)/3 AS people_persuading,

(
"Mental Processes - Judging the Qualities of Things, Services, or People" +
"Mental Processes - Developing Objectives and Strategies" +
"Mental Processes - Scheduling Work and Activities" +
"Mental Processes - Organizing, Planning, and Prioritizing Work" +
"Interacting With Others - Performing Administrative Activities" +
"Interacting With Others - Staffing Organizational Units" +
"Interacting With Others - Monitoring and Controlling Resources" +
"Interacting With Others - Resolving Conflicts and Negotiating with Others" +
"Interacting With Others - Coordinating the Work and Activities of Others" +
"Interacting With Others - Developing and Building Teams"
)/10 AS people_leading,

(
"Information Input - Inspecting Equipment, Structures, or Material" +
"Work Output - Controlling Machines and Processes" +
"Work Output - Operating Vehicles, Mechanized Devices, or Equipment"
)/3 AS things_machines_operate,

(
"Work Output - Repairing and Maintaining Mechanical Equipment" +
"Work Output - Repairing and Maintaining Electronic Equipment"
)/2 AS things_machines_maintain,

"Work Output - Interacting With Computers"
AS things_computers,

"Work Output - Operating Vehicles, Mechanized Devices, or Equipment"
AS things_vehicles_heavy_machinery

FROM
pivoted)    
 
SELECT
   occupation_data.onetsoc_code
  ,occupation_data.title
  ,description
  ,physically_demanding
  ,sensorily_demanding
  ,intellectually_demanding_problem_solving
  ,intellectually_demanding_creativity
  ,people_caring
  ,people_teaching_and_instructing
  ,people_persuading
  ,people_leading
  ,things_machines_operate
  ,things_machines_maintain
  ,things_computers
  ,things_vehicles_heavy_machinery
FROM
occupation_data
LEFT JOIN work_activities ON work_activities.onetsoc_code = occupation_data.onetsoc_code
