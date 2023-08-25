from datetime import datetime, timedelta

class Appointment:
    def __init__(self, dt_start: datetime, dt_end: datetime):
        self.start = dt_start
        self.end = dt_end

    def __str__(self):
        return f'Appointment [{self.start} - {self.end}]'

    def __repr__(self):
        return self.__str__()


class Schedule:

    def __init__(self, doctor_name: str, work_start_hour: int, work_end_hour: int):
        self.doctor_name = doctor_name
        self.work_start_hour = work_start_hour
        self.work_end_hour = work_end_hour
        self.schedule = []

    def create_appointment(self, appt_date: str, start_time: str, end_time: str):
        # create appointment, reject if conflict
        try:
            dt_start = self._convert_date(appt_date, start_time)
            dt_end = self._convert_date(appt_date, end_time)
            if dt_start > dt_end:
                return False

            new_appt = Appointment(dt_start, dt_end)

            for appt in self.schedule:
                if self._is_conflict(new_appt, appt):
                    print(f'Appointment {new_appt} overlaps with previously scheduled appointment {appt}')
                    return False

            self.schedule.append(new_appt)
            return True
        except ValueError as e:
            print(e)
            return False

    def get_appointments(self, appt_date: str, start_time:str='00:00', end_time:str='23:59'):
        ''' returns all appointments within window '''
        try:
            dt_start = self._convert_date(appt_date, start_time)
            dt_end = self._convert_date(appt_date, end_time)
            return self._get_appointments(dt_start, dt_end)
        except ValueError as e:
            print(e)
            return []

    def _get_appointments(self, dt_start: datetime, dt_end:datetime=None):
        appts_in_window = []
        if not dt_end:
            dt_end = dt_start.replace(hour=23, minute=59)
        for appt in self.schedule:
            if appt.start > dt_start and appt.end < dt_end:
                appts_in_window.append(appt)
        return appts_in_window

    def get_first_appointment(self, appt_date, start_time):
        ''' find first available appointment after given time, will check the following week if nothing found '''
        try:
            dt_start = self._convert_date(appt_date, start_time)
            return self._get_first_appointment(dt_start)
        except ValueError as e:
            print(e)
            return None

    def _get_first_appointment(self, dt_start: datetime):
        days_ahead = 0
        while days_ahead < 7:
            if days_ahead > 0:
                appts = self._get_appointments(dt_start.replace(hour=0, minute=0) + timedelta(days=days_ahead))
            else:
                appts = self._get_appointments(dt_start + timedelta(days=days_ahead))
            if len(appts) > 0:
                return appts[0]
            days_ahead += 1
        return None

    def _is_valid_date(self, input_date: str, input_time: str):
        '''
        Check if input date and time are valid strings
        Uses _convert_date method and will catch any exceptions thrown

        Parameters:
            input_date (str): the date in format MM/DD/YYYY
            input_time (str): the time in format

        Returns:
            (boolean): boolean indicating if datetime string was valid and within M-F work week
        '''

        try:
            date_obj = self._convert_date(input_date, input_time)
            # M - F
            if date_obj.weekday() < 5:
                return True
            return False
        except:
            return False

    def _convert_date(self, input_date: str, input_time: str):
        '''
        Convert date and time strings to a datetime object

        Parameters:
            input_date (str): the date in format YYYY-MM-DD
            input_time (str): the time in format HH:MM

        Returns:
            date_obj (datetime): Date object from date and time strings

        Throws:
            ValueError is raised if the date_string and format can’t be parsed
        '''

        input_datetime = f'{input_date}T{input_time}'
        date_format = '%Y-%m-%dT%H:%M'
        date_obj = datetime.strptime(input_datetime, date_format)
        return date_obj

    def _is_conflict(self, appt1: Appointment, appt2: Appointment):
        ''' returns whether two appts overlap '''
        overlap = min(appt1.end, appt2.end) - max(appt1.start, appt2.start)
        return overlap > timedelta(minutes=0)

