from uuid import UUID


class DBNotFoundError(Exception):
    def __init__(self, table_name: str, entity_id: int | str | UUID = ""):
        self.table_name = table_name
        self.entity_id = entity_id
