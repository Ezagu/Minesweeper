import os
import sys
import shutil


class RecordManager:

    def __init__(self):
        base_dir = os.path.join(os.getenv('APPDATA'), "Minesweeper")
        os.makedirs(base_dir, exist_ok=True)

        self.path = os.path.join(base_dir, "records.csv")

        if not os.path.exists(self.path):
            if getattr(sys, 'frozen', False):  # Si es un ejecutable
                original_csv = os.path.join(sys._MEIPASS, "records.csv")
            else:
                original_csv = os.path.join(
                    os.path.dirname(__file__), "records.csv")
            shutil.copyfile(original_csv, self.path)

    def get_record_in_difficulty(self, difficulty: str):
        """Return the record in seconds of the dificculty passed"""
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as file:
                record = 0
                for line in file:
                    data = line.split(",")
                    if data[0] == difficulty:
                        record = data[1]
            return record
        else:
            return 0

    def set_record_with_difficulty(self, difficulty: str, record: str):
        """Set the record in the difficulty"""
        all_lines = None
        replace = False
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as file:
                all_lines = file.readlines()

            with open(self.path, "w", encoding="utf-8") as file:
                for line in all_lines:
                    data = line.split(',')
                    if data[0] == difficulty:
                        file.write(difficulty + ',' + record + '\n')
                        replace = True
                    else:
                        file.write(line)
                if not replace:
                    file.write(difficulty + ',' + record + '\n')
        else:
            with open(self.path, "w", encoding="utf-8") as file:
                file.write(difficulty + ',' + record + '\n')
