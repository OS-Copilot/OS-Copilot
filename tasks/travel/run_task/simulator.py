import json
import os
from datetime import datetime

import requests
# from utils.config_manager import ConfigManager

# config_manager = ConfigManager()
time_format = "%Y-%m-%d %H:%M"


def query_database(query):
    try:
        response = requests.post(
            "http://localhost:8079/tools/database",
            json={'queries': [query]}
        ).json()
        print(f'response={response}')
        return response[0]['result']
    except Exception as e:
        print(f'run error{e}')


def get_ticket(number):
    query = f"SELECT * FROM railway\nWHERE number = '{number}';"
    # config_manager.clear_proxies()

    item = query_database(query)
    # config_manager.apply_proxies()

    if item is None or len(item) == 0:
        return None
    item = item[0]
    ticket = {
        "number": item[0],
        "origin": item[1],
        "destination": item[2],
        "departure_time": datetime.strptime(item[3], '%Y-%m-%d %H:%M:%S'),
        "arrival_time": datetime.strptime(item[4], '%Y-%m-%d %H:%M:%S'),
        "duration": item[5],
        "price": item[6]
    }
    print(f'ticket {number} = {ticket}')
    return ticket


# def get_opening_hours(spot):
#     query = f"SELECT * FROM place\nWHERE name = '{spot}';"
#     config_manager.clear_proxies()

#     item = query_database(query)
#     config_manager.apply_proxies()
#     if item is None or len(item) == 0:
#         return None
#     item = item[0]
#     opening_hours_begin = item[3]
#     opening_hours_end = item[4]
#     return opening_hours_begin, opening_hours_end


def get_in_city_transport(origin, destination):
    return 0


def create_object(class_name: str, attributes: dict):
    cls = globals().get(class_name)
    if cls:
        return cls(**attributes)
    else:
        raise ValueError(f"Class '{class_name}' not found.")


class Constraint:
    def check(self, state: dict, error_instruction: str):
        # 0: waiting for satisfying
        # 1: satisfied
        # 2: violated
        pass

    def get_err_msg(self):
        pass


class CityDurationConstraint(Constraint):
    def __init__(self, city, days):
        self.city = city
        self.days = days

    def check(self, state: dict, error_instruction: str):
        if f'days_{self.city}' not in state.keys() or state[f'days_{self.city}'] == 0:
            return 0
        elif state[f'days_{self.city}'] >= self.days:
            return 1
        else:
            state['error'].append(f"{error_instruction}City duration error: have stayed in {self.city}"
                                  f" for only {state[f'days_{self.city}']} days")
            return 2

    def get_err_msg(self):
        return f"Stay in {self.city} for less than {self.days} days"


class SpotDurationConstraint(Constraint):
    def __init__(self, spot, minutes):
        self.spot = spot
        self.minutes = minutes

    def check(self, state: dict, error_instruction: str):
        if f'minutes_{self.spot}' not in state.keys() or state[f'minutes_{self.spot}'] == 0:
            return 0
        elif state[f'minutes_{self.spot}'] >= self.minutes:
            return 1
        else:
            state['error'].append(f"{error_instruction}Spot visiting time error: have stayed in {self.spot}"
                                  f" for only {state[f'minutes_{self.spot}']} minutes")
            return 2

    def get_err_msg(self):
        return f"visit {self.spot} for less than {self.minutes} minutes"


class TravelSimulator:
    def __init__(self, begin_time, end_time, origin_city, origin_place=None, budget=999999, check_opening_hours=False,
                 check_meal=False, type=1, one_day=0, limit='time',money_min=0,money_max=99999,time_min=0,time_max=99999):
        self.state = {'error': [],
                      'cost': 0,
                      'track': []}
        begin_time = datetime.strptime(begin_time, time_format)
        end_time = datetime.strptime(end_time, time_format)
        self.time = begin_time
        self.end_time = end_time
        self.city = origin_city
        self.place = origin_place
        self.check_opening_hours = check_opening_hours
        self.budget = budget
        self.constraints = []
        self.check_meal = check_meal
        self.type = type
        self.one_day = one_day
        self.limit = limit
        self.money_min=money_min
        self.money_max=money_max
        self.time_min=time_min
        self.time_max=time_max

        self.elementary_right = 0
        self.elementary_wrong = 0
        self.intermediate_right = 0
        self.intermediate_wrong = 0

    def create_constraints(self, para_dict):
        constrains = []
        for class_name, attributes_list in para_dict.items():
            if isinstance(attributes_list, list):
                for attributes in attributes_list:
                    constrains.append(create_object(class_name, attributes))
            elif isinstance(attributes_list, dict):
                constrains.append(create_object(class_name, attributes_list))
        self.constraints = constrains

    def action(self, action_str):
        # eval('self.' + action_str)
        try:
            # Use eval to execute the string as Python code.
            # The local scope is set to the methods of the current instance.
            eval('self.' + action_str)

        except Exception as e:
            print(f"An error occurred: {e} in self.{action_str}")
            # raise e

    def check_time_money(self, error_instruction):
        if self.budget < 0:
            self.state['error'].append(f'{error_instruction}Over budget')
        if self.time > self.end_time:
            self.state['error'].append(f'{error_instruction}Time limit({self.end_time}) exceeded.')

    def go_to_city(self, origin: str, destination: str, departure_time, arrival_time, ticket_number):
        error_instruction = f'Error in \"goto_city({origin},{destination},{departure_time},{arrival_time},{ticket_number})\"\n'

        departure_time = datetime.strptime(departure_time, time_format)
        arrival_time = datetime.strptime(arrival_time, time_format)

        ticket = get_ticket(ticket_number)
        if ticket is None:
            self.state['error'].append(f'{error_instruction}Ticket error: no ticket {ticket_number}')
            self.elementary_wrong += 1
        elif not (ticket['origin'] == origin and ticket['destination'] == destination and
                  ticket['departure_time'] == departure_time and ticket['arrival_time'] == arrival_time):
            self.state['error'].append(f'{error_instruction}Ticket error: ticket does not match the itinerary')
            self.elementary_wrong += 1
        else:
            self.elementary_right += 1

        if origin != self.city:
            self.state['error'].append(f'{error_instruction}Position error: In {self.city},not {origin}')
            self.elementary_wrong += 1
        else:
            self.elementary_right += 1
        if departure_time < self.time:
            self.state['error'].append(f'{error_instruction}Time error: already {self.time}, beyond the departure time')
            self.elementary_wrong += 1
        else:
            self.elementary_right += 1

        if self.time != departure_time:
            self.stay_in(city=self.city, begin_time=self.time, end_time=departure_time)

        for constraint in self.constraints:
            if isinstance(constraint, CityDurationConstraint):
                constraint.check(state=self.state, error_instruction=error_instruction)

        self.time = arrival_time
        self.city = destination
        self.budget -= ticket['price']

        self.check_time_money(error_instruction)

        self.state['track'].append({'begin_time': departure_time, 'end_time': arrival_time, 'action': 'go_to_city'})

    def go_to_place(self, origin: str, destination: str, departure_time, arrival_time):
        error_instruction = f'Error in \"go_to_place({origin},{destination},{departure_time},{arrival_time})\"\n'

        departure_time = datetime.strptime(departure_time, time_format)
        arrival_time = datetime.strptime(arrival_time, time_format)
        if origin != self.place:
            self.state['error'].append(f'{error_instruction}Position error: In {self.place},not {origin}')
            self.elementary_wrong += 1
        else:
            self.elementary_right += 1
        if departure_time < self.time:
            self.state['error'].append(f'{error_instruction}Time error: already {self.time}, beyond the departure time')
            self.elementary_wrong += 1
        else:
            self.elementary_right += 1

        if self.time != departure_time:
            self.visit(place=self.place, begin_time=self.time, end_time=departure_time)

        # for constraint in self.constraints:
        #     if isinstance(constraint, SpotDurationConstraint):
        #         constraint.check(state=self.state, error_instruction=error_instruction)
        self.time = arrival_time
        self.place = destination
        # self.check_time_money(error_instruction)

        self.state['track'].append({'begin_time': departure_time, 'end_time': arrival_time, 'action': 'go_to_place'})

    def stay_in(self, city: str, begin_time, end_time):
        if self.type == 3:
            pass

        error_instruction = f'Error in \"stay_in({city},{begin_time},{end_time})\"\n'

        if isinstance(begin_time, str):
            begin_time = datetime.strptime(begin_time, time_format)
        if isinstance(end_time, str):
            end_time = datetime.strptime(end_time, time_format)

        # TODO:判断天数
        if begin_time < self.time:
            self.state['error'].append(f'{error_instruction}Time error: already {self.time}, beyond the begin_time')
            self.elementary_wrong += 1
        else:
            self.elementary_right += 1

        if self.city != city:
            self.state['error'].append(f'{error_instruction}Position error: In {self.city},not {city}')
            self.city = city
            self.elementary_wrong += 1
        else:
            self.elementary_right += 1
        self.time = end_time
        self.check_time_money(error_instruction)

        duration = end_time - begin_time
        if f'days_{city}' in self.state.keys():
            self.state[f'days_{city}'] += duration.days
        else:
            self.state[f'days_{city}'] = duration.days

        self.state['track'].append({'begin_time': begin_time, 'end_time': end_time, 'action': 'stay_in'})

    def visit(self, place: str, begin_time, end_time):

        error_instruction = f'Error in \"visit({place},{begin_time},{end_time})\"\n'
        if isinstance(begin_time, str):
            begin_time = datetime.strptime(begin_time, time_format)
        if isinstance(end_time, str):
            end_time = datetime.strptime(end_time, time_format)
        if begin_time < self.time:
            self.state['error'].append(f'{error_instruction}Time error: already {self.time}, beyond the begin_time')
            self.elementary_wrong += 1
        else:
            self.elementary_right += 1
        if self.place != place:
            self.state['error'].append(f'{error_instruction}Position error: In {self.place},not {place}')
            self.place = place
            self.elementary_wrong += 1
        else:
            self.elementary_right += 1
        self.time = end_time
        self.check_time_money(error_instruction)

        if self.check_opening_hours:
            opening_hours_begin, opening_hours_end = get_opening_hours(spot=self.place)
            t1 = datetime.strptime(f"{opening_hours_begin}:00", "%H:%M").time()
            if opening_hours_end == 24:
                t2 = datetime.strptime(f"23:59", "%H:%M").time()
            else:
                t2 = datetime.strptime(f"{opening_hours_end}:00", "%H:%M").time()
            if begin_time.time() >= t1 and end_time.time() <= t2:
                self.intermediate_right += 1
            else:
                self.state['error'].append(f'{error_instruction}Opening hours error: visit outside of opening hours')
                self.intermediate_wrong += 1

        duration = end_time - begin_time

        if f'minutes_{place}' in self.state.keys():
            self.state[f'minutes_{place}'] += duration.total_seconds() / 60
        else:
            self.state[f'minutes_{place}'] = int(duration.total_seconds() / 60)

        # for constraint in self.constraints:
        #     if isinstance(constraint, SpotDurationConstraint):
        #         constraint.check(state=self.state, error_instruction=error_instruction)

        self.state['track'].append({'begin_time': begin_time, 'end_time': end_time, 'action': 'visit'})

    def over(self):
        for constraint in self.constraints:
            if isinstance(constraint, CityDurationConstraint) or isinstance(constraint, SpotDurationConstraint):
                result = constraint.check(state=self.state, error_instruction='')
                if result == 0 or result == 2:
                    self.state['error'].append(constraint.get_err_msg())
                    self.intermediate_wrong += 1
                else:
                    self.intermediate_right += 1

        def is_overlapping(begin1, end1, begin2, end2):
            return not (end1 <= begin2 or end2 <= begin1)

        if self.check_meal:
            meal_times = [['12:00', '13:00'], ['18:30', '19:30']]
            for meal_time in meal_times:
                meal_begin = datetime.strptime(meal_time[0], "%H:%M").time()
                meal_end = datetime.strptime(meal_time[1], "%H:%M").time()
                is_satisfied = True
                for t in self.state['track']:
                    if t['action'] in ['go_to_place', 'visit']:
                        if is_overlapping(meal_begin, meal_end, t['begin_time'].time(), t['end_time'].time()):
                            is_satisfied = False
                if is_satisfied:
                    self.intermediate_right += 1
                else:
                    self.intermediate_wrong += 1
                    self.state['error'].append(
                        f'Meal error: No meal time reserved from {meal_time[0]} to {meal_time[1]}')

    def get_errors(self):
        return self.state['error']

    def get_score(self):
        print(f'e_right={self.elementary_right}')
        print(f'e_wrong={self.elementary_wrong}')
        print(f'i_right={self.intermediate_right}')
        print(f'i_wrong={self.intermediate_wrong}')
        self.state['e_right'] = self.elementary_right
        self.state['e_wrong'] = self.elementary_wrong
        self.state['i_right'] = self.intermediate_right
        self.state['i_wrong'] = self.intermediate_wrong
        if (self.elementary_right + self.elementary_wrong) == 0:
            self.elementary_wrong = 1
        if (self.intermediate_right + self.intermediate_wrong) == 0:
            self.intermediate_wrong = 1

        elementary_score = self.elementary_right / (self.elementary_right + self.elementary_wrong) * 60
        intermediate_score = self.intermediate_right / (self.intermediate_right + self.intermediate_wrong) * 20
        advanced_score = 0
        score = elementary_score
        if score == 60:
            score += intermediate_score
        if score == 80:
            score += advanced_score
        return score


# print(get_opening_hours('Tiananmen Square'))
# print(get_ticket('D1000'))