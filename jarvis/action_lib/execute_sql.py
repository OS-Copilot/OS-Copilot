from jarvis.action.base_action import BaseAction


_COMMAND = """
from jarvis.action_lib.execute_sql import execute_sql
action = execute_sql()
action.run(db_path='../tasks/travel/database/travel.db', query='PRAGMA table_info(railway)')
"""


class execute_sql(BaseAction):
    def __init__(self) -> None:
        super().__init__()
        self._description = "Using turn_on_light_mode() will change your system into the light mode."

    def __call__(self, query: str = 'PRAGMA table_info(railway)'):
        if not query:
            return "No query, return"
        import sqlite3

        conn = sqlite3.connect('../../tasks/travel/database/travel.db')
        cursor = conn.cursor()
        results = {
            "query": query,
            "result": None,
            "error": None
        }
        try:
            cursor.execute(query)
            results['result'] = cursor.fetchall()
        except Exception as e:
            results['error'] = str(e)
        conn.commit()
        conn.close()

        return results

    # @property
    # def _command(self):
    #     return self._python(_COMMAND)

    # def _success(self):
    #     return "Successfully turned the system into the Light Mode"

    # def __call__(self, *args, **kwargs):
    #
    #     command = 'shortcuts run "Dark Mode"'
    #     try:
    #         # result = subprocess.run([command, "Dark Mode"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    #         result = subprocess.run([command], capture_output=True, check=True,
    #                                 text=True, shell=True, timeout=self.timeout, stdin=subprocess.DEVNULL)
    #         if result.returncode == 0:
    #             return result
    #     except subprocess.CalledProcessError as e:
    #         return e
        # except subprocess.TimeoutExpired:
        #     raise TimeoutError(f"Command '{command}' timed out after {self.timeout} seconds.")

