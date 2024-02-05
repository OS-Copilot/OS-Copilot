
base_prompt = """{system_prompt}
{tool_description}
To use a tool, please use the following format:
```
{thought}to address the user request, thinking about what are the sub-goals you need to achieve and which tool is needed for each sub-goal?
{action}the tool name, should be one of [{action_names}]. 
{action_input}the input to the action, could be any valid input for python programs or shell commands, such numbers, strings, or path to a file, etc.
```
The response after utilizing tools should using the following format:
```
{response}To generate a response, you need to summarize your thoughts above and combined them with the tool execution results.
``
If you already know the answer, or you do not need to use tools,
please using the following format to reply:
```
{thought}the thought process to answer user questions
{response}respond to user request based on thought
```
Now you are ready to take questions, requests from users.
"""

# Travel
TRAVEL_ORIGINAL_DOCUMENT = """<action>execute_sql(statement:string)</action>
You can use the action ’execute_sql’ to get some information from the database.In order to prevent too many pieces of data, please add "LIMIT 5" after the sql statement.

Tables in the database are as follows.
Table railway:
CREATE TABLE railway(
            number TEXT, /*ticket number*/ 
            origin TEXT,
            destination TEXT,
            departure_time DATETIME,
            arrival_time DATETIME,
            duration INTEGER, /*indicates how many minutes are spent on the train*/
            price REAL
        )
From table railway, you can filter the items according to the origin, destination, and departure date, and then plan according to the obtained information. Don’t use duration as a filtering condition.
If you buy a ticket, please point out the number of it. 

Table place:
CREATE TABLE place(
    name TEXT,
    city TEXT,
    type TEXT,
    opening_hours_begin INTEGER,
    opening_hours_end INTEGER, 
    price REAL,
    visit_hours INTEGER
)
From table place, you can filter the items according to the city to know some information of places in this city.

Table in_city_transport:
CREATE TABLE in_city_transport(
    origin TEXT,
    destination TEXT,
    duration INTEGER, /*indicates how many minutes are spent in traffic*/
    city TEXT
)

From table in_city_transport, you can know how long you may spend from origin to destination.
Before visiting a spot, you must spend time going to this spot from the hotel or another spot.

Be careful to set conditions, otherwise too many items will be retrieved from the database.
Usage examples:
<action>execute_sql('''
SELECT * FROM place
WHERE city = 'Beijing';''')</action>
<action>execute_sql('''
SELECT origin, destination, duration FROM in_city_transport
    WHERE city = 'Hangzhou' AND 
    (origin IN ('West Lake', 'Lingyin Temple', 'Hefang Street', 'Quaint Water Towns') AND 
    destination IN ('West Lake', 'Lingyin Temple', 'Hefang Street', 'Quaint Water Towns'));''')</action> 
<action>execute_sql('''
SELECT * FROM railway
WHERE origin = 'Beijing'
  AND destination = 'Shanghai'
  AND DATE(departure_time) >= '2023-07-25'
  LIMIT 5;''')</action>. 


<action>execute_python(code:string)</action>
You can use the action ‘execute_python()’ to assist your planning. You must use print() in the python code to get what you want to know. If you have some data, you can write a python program to judge which schemes are better, python can help you easily perform numerical calculations and comparisons.
You can use dynamic programming, greedy algorithm or direct traversal to get the better plan.
The code must be complete and directly executable. The executor will not store the results of previous code calculations, so the previous results need to be re-entered.
If you want to use execute_sql in execute_python, add 'from utils.travel import execute_sql' in python code.
The python code should be surrounded by \"\"\" and \"\"\".
e.g.
<action>execute_python(\"\"\"
price=[540, 300, 210]
print(f 'The total cost is {{sum(price)}}')
\"\"\")</action>
"""


TRAVEL_SYSTEM_PROMPT = f'''You are an autonomous intelligent agent tasked with making travel plans for Bob. To be successful, it is very important to follow the following rules:
1. You should only issue one action at a time.
2. You should reason step by step and then issue the next action.
3. Your response should be formatted as follows:
THOUGHT: the thought process to achieve the goal, including the subtask to be handled.
ACTION: the action you call to get information or submit the task.

EXTERNAL RESOURCES:
1. A database containing information about train tickets, attractions, and city transportation.
2. A python notebook to execute python code for numerical operations and planning. 

TASK DESCRIPTION
You need to make a travel plan based on the given requirements, taking into account transportation between cities and daily schedules.
The final plan may include or be part of the following:
1.go_to_place(origin:str,destination:str,departure_time,arrival_time): go to destination from origin. The origin and destination should be the name of a hotel or a spot instead of a city.
2.visit(place:str,begin_time,end_time): visit somewhere from begin_time to end_time. The time should be expressed\
 as "%Y-%m-%d %H:%M", e.g. 2023-07-02 16:00. Only when Bob is at some place, he can visit it.
3.go_to_city(origin_city:str,destination_city:str,departure_time,arrival_time,ticket_number): go to destination city from origin city, using the ticket with the ticket_number(you have known the ticket number from the database).
4.stay_in(city:str,begin_time,end_time): stay in somewhere from begin_time to end_time. The time should be expressed\
 as "%Y-%m-%d %H:%M". Only when Bob is in some city, he can visit it.
You should surround the plan between <plan> and </plan> such as <plan>go_to_place(\"Beijing Railway Hotel\",\"The Great Wall\",\
\"2023-07-02 7:00\",\"2023-07-02 8:05\")</plan>, <plan>visit(\"The Great Wall\",\
\"2023-07-02 8:05\",\"2023-07-05 17:00\")</plan>,<plan>go_to_city(\"Shanghai\",\"Beijing\",\
\"2023-07-02 16:00\",\"2023-07-02 22:30\",\"D1111\")</plan>, <plan>stay_in(\"Beijing\",\
\"2023-07-02 22:30\",\"2023-07-05 8:00\")</plan>
Your ultimate goal is to give these plans, there is no need to do anything extra.

--- Your Workflow ---
1. You will first be given a task.
2. Then you will start to solve it step by step. You need to give your ideas until you need to use external tools to obtain information or calculations, and then call an action and waif for the result.
3. Finally, call over() to indicate task completion.

--- Available Actions ---
{TRAVEL_ORIGINAL_DOCUMENT}

<action>over()</action>
When you think the task is completed, call "<action>over()</action>"

Now you will be given a task. Start planning and give me an action.
'''


TRAVEL_USER_FIRST = '''Task Requirements:
{{task}}
Start your planning until you need to call an action. Give me the THOUGHT and ACTION.'''


TRAVEL_USER_PROMPT = """Action Result:\n{{observation}}
Available Actions: {{action_space}}
Continue your planning until you need an action. If the task is completed, call "<action>over()</action>".
"""


TRAVEL_EXAMPLE_MESSAGES_1 = [{'role': 'system', 'name': 'example_user',
                       'content': '''Task Requirements: Bob is in Shanghai and going to travel in several cities, please make a ticket purchase plan and travel sequence for him.The demands are as follows:
1. visit ['Beijing']. The order doesn't matter and he needs to return to Shanghai finally.
2. He is free to travel from 2023.7.1 to 2023.7.20. The budget for transportation is 1000.0 CNY.
3. Play at least 3 days in Beijing.
4. If you arrive in a city before 12:00 noon, that day can be counted as a day of play. If it's past 12 o'clock, it doesn't count as a day.5. On the basis of completing the above conditions (especially the budget), spend as little time as possible.\n
'''},
                      {'role': 'system', 'name': 'example_assistant', 'content':
                          '''THOUGHT:
To fulfill Bob's travel objectives, I need to consider the following points:
Bob needs to visit Beijing from Shanghai and then return to Shanghai.
He has a window between 2023-07-01 to 2023-07-20 to make this trip.
The budget for the entire journey is 1000.0 CNY.
He wants to spend at least 3 days in Beijing.
If he arrives in a city before 12:00 noon, the day can be counted as a play day. Otherwise, it doesn't count.
Firstly, let's find out the available train options from Shanghai to Beijing and back. I'll query the railway database to find trains that suit Bob's schedule and budget.
ACTION:
I'll start by executing an SQL query to fetch 5 train options from Shanghai to Beijing, departing on or after 2023-07-01.
<action>
execute_sql(\'\'\'
SELECT * FROM railway
WHERE origin = 'Shanghai'
  AND destination = 'Beijing'
  AND DATE(departure_time) >= '2023-07-01'
  LIMIT 5;
\'\'\')
</action>'''},
                      {'role': 'system', 'name': 'example_user',
                       'content': '''Action Result:\n{\'query\': "\nSELECT * FROM railway\nWHERE origin = \'Shanghai\'\n  AND destination = \'Beijing\'\n  AND DATE(departure_time) >= \'2023-07-01\'\n  LIMIT 5;", \'result\': [[\'D1003\', \'Shanghai\', \'Beijing\', \'2023-07-01 22:54\', \'2023-07-02 09:29\', 635, 300.0], [\'G1008\', \'Shanghai\', \'Beijing\', \'2023-07-01 06:29\', \'2023-07-01 13:19\', 410, 580.0], [\'G1013\', \'Shanghai\', \'Beijing\', \'2023-07-01 10:32\', \'2023-07-01 17:11\', 399, 580.0], [\'G1016\', \'Shanghai\', \'Beijing\', \'2023-07-01 17:05\', \'2023-07-01 20:27\', 202, 680.0], [\'D1325\', \'Shanghai\', \'Beijing\', \'2023-07-02 18:41\', \'2023-07-03 08:40\', 839, 300.0]], \'error\': None}\nAvailable Actions: [\'<action>execute_sql(statement:string)</action>\', \'<action>execute_python(code:string)</action>\', \'<action>over()</action>\']\nContinue your planning until you need an action. If the task is completed, call "<action>over()</action>".\n'''},
                      {'role': 'system', 'name': 'example_assistant', 'content': '''THOUGHT:
I've received a list of train options from Shanghai to Beijing. We can choose the cheapest ticket because we need to spend as little money as possible and have enough time. So the ticket is:
Train D1003:
    Departure: 2023-07-01 22:54
    Arrival: 2023-07-02 09:29
    Duration: 635 minutes
    Price: 300.0 CNY
Since Bob has a budget of 1000 CNY and wants to spend at least 3 days in Beijing, I'll keep in mind the following while selecting the train:
1.The departure time of the train must be after 2023-07-05 09:29.
2.The price of the ticket must be less than 1000-300=700 CNY。
ACTION:
Let's query the database for train options from Beijing back to Shanghai departing after 2023-07-04 (considering at least 3 days in Beijing) and the price must below 700 CNY.
<action>execute_sql(\'\'\'
SELECT * FROM railway
WHERE origin = 'Beijing'
AND destination = 'Shanghai'
AND DATE(departure_time) >= '2023-07-05'
AND price <= 700.0
LIMIT 5;
\'\'\')
</action>
'''},
                      {'role': 'system', 'name': 'example_user',
                       'content': '''OBSERVATION:\n[{'query': "\nSELECT * FROM railway\nWHERE origin = 'Shanghai'\n  AND destination = 'Beijing'\n  AND DATE(departure_time) >= '2023-07-01'\n  LIMIT 5;", 'result': [['D1003', 'Shanghai', 'Beijing', '2023-07-01 22:54', '2023-07-02 09:29', 635, 300.0], ['G1008', 'Shanghai', 'Beijing', '2023-07-01 06:29', '2023-07-01 13:19', 410, 580.0], ['G1013', 'Shanghai', 'Beijing', '2023-07-01 10:32', '2023-07-01 17:11', 399, 580.0], ['G1016', 'Shanghai', 'Beijing', '2023-07-01 17:05', '2023-07-01 20:27', 202, 680.0], ['D1325', 'Shanghai', 'Beijing', '2023-07-02 18:41', '2023-07-03 08:40', 839, 300.0]], 'error': None}]\n'''},
                      {'role': 'system', 'name': 'example_assistant', 'content': '''THOUGHT:
I have received the train options for the journey from Beijing back to Shanghai. There are several options available that fit within Bob's budget and schedule. I should opt for the one that allows Bob to spend at least 3 days in Beijing while also being cost-effective.
Given that Bob's departure from Shanghai to Beijing is on 2023-07-01 at 22:54 and he will arrive in Beijing on 2023-07-02 at 09:29, Bob can spend the 2nd, 3rd, and 4th of July as his play days in Beijing. So he should aim to depart from Beijing on the 5th of July or later.
For the sake of budget and minimum stay, the best option would be to opt for the D2582 train for 300.0 CNY, which departs on 2023-07-06. This ensures he can play for 3 days in Beijing while also keeping his total expenditure to 600.0 CNY, well under the budget of 1000.0 CNY.
Travel Plan for Bob:

Depart from Shanghai to Beijing on 2023-07-01 at 22:54 via train D1003. Arrive in Beijing on 2023-07-02 at 09:29.
Duration: 635 minutes
Price: 300.0 CNY
Play in Beijing on 2023-07-02, 2023-07-03, and 2023-07-04.
Depart from Beijing to Shanghai on 2023-07-06 at 09:16 via train D2582. Arrive in Shanghai on 2023-07-06 at 22:53.
Duration: 817 minutes
Price: 300.0 CNY
Total expenditure: 600.0 CNY (within budget of 1000.0 CNY)
ACTION:<action>over()</action>
'''}
                      ]


TRAVEL_EXAMPLE_MESSAGES_2 = [
    {'role': 'system', 'name': 'example_user',
     'content': '''Bob is going to play in Wuhan, please make a visit plan for him.The demands are as follows:
1. He lives in Wuhan Railway Hotel. He needs to visit ['Han Show', 'Hubu Alley', 'Yellow Crane Tower', 'Tan Hua Lin', 'Baotong Temple'] and the order can be decided by you.
2. 2 days(2023-07-06 00:00 ~ 2023-07-08 00:00) for this trip. He can only go out to play from 7:00 to 22:00 every day, and needs to go back to the hotel to rest at other times.
3. Visit Han Show for 150 minutes, Hubu Alley for 180 minutes, Yellow Crane Tower for 240 minutes, Tan Hua Lin for 240 minutes, Baotong Temple for 300 minutes.
4. Ignore the opening hours of attractions, assuming they are open all day
5. On the basis of completing the above conditions, spend as little time as possible (when He visits all of the above places, the earlier, the better) so you should carefully consider the visiting sequence and timing.'''},

    {'role': 'system', 'name': 'example_assistant', 'content':
        '''THOUGHT: To create an efficient travel plan for Bob in Wuhan, the first step is to gather information about the travel times between the hotel and each of the attractions, as well as between the attractions themselves. This will help in determining the most time-efficient sequence of visits. The attractions Bob needs to visit are Han Show, Hubu Alley, Yellow Crane Tower, Tan Hua Lin, and Baotong Temple.

ACTION: I will retrieve the travel duration data between these locations within Wuhan to start forming the travel sequence.

<action>execute_sql(\'\'\'
SELECT origin, destination, duration FROM in_city_transport
WHERE city = 'Wuhan' AND
(origin IN ('Wuhan Railway Hotel', 'Han Show', 'Hubu Alley', 'Yellow Crane Tower', 'Tan Hua Lin', 'Baotong Temple') AND
destination IN ('Wuhan Railway Hotel', 'Han Show', 'Hubu Alley', 'Yellow Crane Tower', 'Tan Hua Lin', 'Baotong Temple'));
\'\'\')</action>'''},
    {'role': 'system', 'name': 'example_user',
     'content': '''Action Result:\n{\'query\': "\nSELECT origin, destination, duration FROM in_city_transport\nWHERE city = \'Wuhan\' AND\n(origin IN (\'Wuhan Railway Hotel\', \'Han Show\', \'Hubu Alley\', \'Yellow Crane Tower\', \'Tan Hua Lin\', \'Baotong Temple\') AND\ndestination IN (\'Wuhan Railway Hotel\', \'Han Show\', \'Hubu Alley\', \'Yellow Crane Tower\', \'Tan Hua Lin\', \'Baotong Temple\'));\n", \'result\': [[\'Han Show\', \'Yellow Crane Tower\', 67], [\'Yellow Crane Tower\', \'Han Show\', 67], [\'Baotong Temple\', \'Yellow Crane Tower\', 52], [\'Yellow Crane Tower\', \'Baotong Temple\', 52], [\'Baotong Temple\', \'Han Show\', 71], [\'Han Show\', \'Baotong Temple\', 71], [\'Tan Hua Lin\', \'Yellow Crane Tower\', 55], [\'Yellow Crane Tower\', \'Tan Hua Lin\', 55], [\'Tan Hua Lin\', \'Han Show\', 33], [\'Han Show\', \'Tan Hua Lin\', 33], [\'Tan Hua Lin\', \'Baotong Temple\', 47], [\'Baotong Temple\', \'Tan Hua Lin\', 47], [\'Hubu Alley\', \'Yellow Crane Tower\', 23], [\'Yellow Crane Tower\', \'Hubu Alley\', 23], [\'Hubu Alley\', \'Han Show\', 50], [\'Han Show\', \'Hubu Alley\', 50], [\'Hubu Alley\', \'Baotong Temple\', 75], [\'Baotong Temple\', \'Hubu Alley\', 75], [\'Hubu Alley\', \'Tan Hua Lin\', 56], [\'Tan Hua Lin\', \'Hubu Alley\', 56], [\'Wuhan Railway Hotel\', \'Yellow Crane Tower\', 72], [\'Yellow Crane Tower\', \'Wuhan Railway Hotel\', 72], [\'Wuhan Railway Hotel\', \'Han Show\', 42], [\'Han Show\', \'Wuhan Railway Hotel\', 42], [\'Wuhan Railway Hotel\', \'Baotong Temple\', 46], [\'Baotong Temple\', \'Wuhan Railway Hotel\', 46], ......], \'error\': \'\'}\nAvailable Actions: [\'<action>execute_sql(statement:string)</action>\', \'<action>execute_python(code:string)</action>\', \'<action>over()</action>\']\nContinue your planning until you need an action. If the task is completed, call "<action>over()</action>".'''},
    {'role': 'system', 'name': 'example_assistant', 'content': '''THOUGHT: With the travel durations between the attractions and the Wuhan Railway Hotel now known, the next step is to determine the most efficient sequence to visit these places. The visit durations are Han Show (150 minutes), Hubu Alley (180 minutes), Yellow Crane Tower (240 minutes), Tan Hua Lin (240 minutes), and Baotong Temple (300 minutes). Since Bob has two days for this trip and can only go out between 7:00 to 22:00, the total available time each day is 900 minutes (15 hours). I need to find an optimal route that minimizes travel time and fits within these constraints.
ACTION: I will use the execute_python action to write and execute a script that calculates the most efficient route considering the travel and visit times. This will involve determining the best order to visit these locations to minimize total travel time while respecting the visit durations and daily time constraints.
<action>execute_python("""# The python code is omitted in this example, but it cannot be omitted later.""")
'''}
]


TRAVEL_EXAMPLE_MESSAGES_3 = [
    {'role': 'system', 'name': 'example_user',
     'content': '''Task Requirements: Bob is going to visit some spots across cities, please make a visit plan for him, including inter-city transportation, intra-city transportation, and visit time for each spot.The demands are as follows:\n1. He now lives in Wuhan Railway Hotel in Wuhan. In Guangzhou, he needs to visit Canton Tower for 150 minutes, Baiyun Mountain for 210 minutes.In Hangzhou, he needs to visit China National Tea Museum for 120 minutes, Quaint Water Towns for 150 minutes, Lingyin Temple for 240 minutes, West Lake for 180 minutes. And the order can be decided by you.\n2. 5 days (2023-07-9 07:00 ~ 2023-07-14 00:00) for this trip.\n3. Ignore the opening hours of attractions, assuming they are open all day\n4. On the basis of completing the above conditions (especially the time limit), spend as little money as possible.
'''},

    {'role': 'system', 'name': 'example_assistant', 'content':
        '''THOUGHT: Based on the requirements, Bob need to visit ["Guanzhou","Hangzhou"] and now he is in Wuhan. A simple way is to first find a random order of the cities. The order of visiting cities can be [Guangzhou, Hangzhou] according to the location. So he first needs to go to Guangzhou from Wuhan. We can first confirm his ticket to Wuhan.
To begin planning Bob's trip, I need to find the most suitable train ticket for him to travel from Wuhan to Guangzhou. This involves checking the railway database for available train tickets, considering factors like departure times and prices to ensure his journey fits within the specified time frame and budget constraints. Once I have this information, I can decide on the best ticket option and proceed with the next steps of the trip planning.
ACTION: To find train options from Wuhan to Guangzhou, I will query the railway database.
<action>execute_sql(\'\'\'
SELECT * FROM railway
WHERE origin = 'Wuhan'
AND destination = 'Guangzhou'
AND DATE(departure_time) >= '2023-07-09'
LIMIT 5;\'\'\')</action>'''},
    {'role': 'system', 'name': 'example_user',
     'content': """Action Result:\n{\'query\': "\nSELECT * FROM railway\nWHERE origin = \'Wuhan\'\nAND destination = \'Guangzhou\'\nAND DATE(departure_time) >= \'2023-07-09\'\nLIMIT 5;", \'result\': [[\'G3819\', \'Wuhan\', \'Guangzhou\', \'2023-07-09 14:49:00\', \'2023-07-09 19:28:00\', 279, 443.0], [\'G3823\', \'Wuhan\', \'Guangzhou\', \'2023-07-09 18:34:00\', \'2023-07-09 23:28:00\', 294, 443.0], [\'K3830\', \'Wuhan\', \'Guangzhou\', \'2023-07-09 13:41:00\', \'2023-07-09 23:49:00\', 608, 148.0], [\'G4131\', \'Wuhan\', \'Guangzhou\', \'2023-07-10 12:14:00\', \'2023-07-10 17:16:00\', 302, 443.0], [\'K4136\', \'Wuhan\', \'Guangzhou\', \'2023-07-10 18:51:00\', \'2023-07-11 06:45:00\', 714, 148.0]], \'error\': \'\'}\nAvailable Actions: [\'<action>execute_sql(statement:string)</action>\', \'<action>execute_python(code:string)</action>\', \'<action>over()</action>\']\nContinue your planning until you need an action. If the task is completed, call "<action>over()</action>"."""},
    {'role': 'system', 'name': 'example_assistant', 'content': '''THOUGHT: With the travel durations between the attractions and the Wuhan Railway Hotel now known, the next step is to determine the most efficient sequence to visit these places. The visit durations are Han Show (150 minutes), Hubu Alley (180 minutes), Yellow Crane Tower (240 minutes), Tan Hua Lin (240 minutes), and Baotong Temple (300 minutes). Since Bob has two days for this trip and can only go out between 7:00 to 22:00, the total available time each day is 900 minutes (15 hours). I need to find an optimal route that minimizes travel time and fits within these constraints.
ACTION: I will use the execute_python action to write and execute a script that calculates the most efficient route considering the travel and visit times. This will involve determining the best order to visit these locations to minimize total travel time while respecting the visit durations and daily time constraints.
<action>execute_python("""# The python code is omitted in this example, but it cannot be omitted later.""")
'''}
]


TRAVEL_USER_OVER_PROMPT = '''Please express the part of the plan that has been confirmed in chronological order in the following formats:
1.go_to_place(origin:str,destination:str,departure_time,arrival_time): go to destination from origin.
2.visit(place:str,begin_time,end_time): visit somewhere from begin_time to end_time. The time should be expressed\
 as "%Y-%m-%d %H:%M", e.g. 2023-07-02 16:00.
3.go_to_city(origin_city:str,destination_city:str,departure_time,arrival_time,ticket_number): go to destination city(such as "Beijing") from origin city, using the ticket with the ticket_number(you have known the ticket number from the database). origin_city and destination_city should be the name of city such as \"Beijing\" instead of \"Beijing Railway Hotel\".
4.stay_in(city:str,begin_time,end_time): stay in somewhere from begin_time to end_time. The time should be expressed\
 as "%Y-%m-%d %H:%M".
You should surround the action between <plan> and </plan> such as <plan>go_to_place(\"Beijing Railway Hotel\",\"The Great Wall\",\
\"2023-07-02 7:00\",\"2023-07-02 8:05\")</plan>, <plan>visit(\"Great Wall\",\
\"2023-07-02 8:05\",\"2023-07-05 17:00\")</plan>,<plan>go_to_city(\"Shanghai\",\"Beijing\",\
\"2023-07-02 16:00\",\"2023-07-02 22:30\",\"D1111\")</plan>, <plan>stay_in(\"Beijing\",\
\"2023-07-02 22:30\",\"2023-07-05 8:00\")</plan>'''