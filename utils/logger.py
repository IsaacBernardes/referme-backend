import logging
import json


class Logger:

    def __init__(self, class_name, function, version, parameters={}):
        self.log = {
            "class": class_name,
            "function": function,
            "version": version,
            "parameters": parameters,
            "actions": [],
            "exceptions": []
        }

    def add_info_action(self, code: str, description: str):
        self.log["actions"].append(dict(
            code=code,
            type="INFO",
            description=description
        ))

    def add_common_action(self, code: str, description: str):
        self.log["actions"].append(dict(
            code=code,
            type="COMMON",
            description=description,
            success=False
        ))

    def finish_common_action(self, code: str, success: bool):
        action_index = next(
            (index for index, element in enumerate(self.log["actions"]) if element["code"] == code),
            None
        )

        if action_index is not None:
            self.log["actions"][action_index]["success"] = success

    def add_database_action(self, code: str, description: str, query: str, parameters: dict):

        formatted_query = " ".join(line.strip() for line in query.splitlines())

        formatted_parameters = parameters.copy()
        for param in formatted_parameters.keys():
            if str(param).startswith("sec_"):
                formatted_parameters[param] = "*****"

        self.log["actions"].append(dict(
            code=code,
            type="DATABASE",
            description=description,
            query=formatted_query,
            parameters=formatted_parameters,
            success=False
        ))

    def finish_database_action(self, code: str, success: bool, result=None):
        action_index = next(
            (index for index, element in enumerate(self.log["actions"]) if element["code"] == code),
            None
        )

        if action_index is not None:
            self.log["actions"][action_index]["success"] = success
            self.log["actions"][action_index]["results"] = result

    def add_exception(self, exception):
        self.log["exceptions"].append(exception)

    def save(self):
        logging.error(json.dumps(self.log, indent=4))
