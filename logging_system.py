from dataclasses import dataclass, asdict
from datetime import datetime
import json
from psycopg2 import sql
from typing import Optional
from loomie_core.connections import set_postgres_conn


@dataclass
class LoomieInteractionLog:
    session_id: Optional[str] = None
    user_info: Optional[dict] = None
    customer_code: Optional[str] = None
    input_datetime: Optional[datetime] = None
    user_input: Optional[str] = None
    model_response: Optional[str] = None
    model_response_time_ms: Optional[int] = None

    def update_log(self, attribute, value):
        if hasattr(self, attribute):
            setattr(self, attribute, value)
        else:
            raise AttributeError(
                f"'{attribute}' is not a valid attribute of LoomieInteractionLog"
            )

    def to_json(self):
        log_dict = asdict(self)

        if log_dict["input_datetime"] and isinstance(
            log_dict["input_datetime"], datetime
        ):
            log_dict["input_datetime"] = log_dict["input_datetime"].isoformat()

        return json.dumps(log_dict)

    def insert_log_entry(self):
        conn = set_postgres_conn()

        with conn.cursor() as cursor:
            query = sql.SQL(
                """
                INSERT INTO loomie_logs.loomie_core (log_data, session_id, input_datetime)
                VALUES (%s, %s, %s)
            """
            )
            log_json = self.to_json()
            cursor.execute(query, (log_json, self.session_id, self.input_datetime))
            conn.commit()
