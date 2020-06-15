import pickle
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, List, Union

import pandas as pd
from pyfiglet import Figlet

try:
    from termcolor import colored
except ImportError:
    colored = None


class TextAnnotation:
    def sanitize_records(self):
        if isinstance(self.records, List):
            print(f"records: list with {len(self.records)} records")
        elif isinstance(self.records, Callable):
            print("records: Callable, no of records not known")
        else:
            raise TypeError(f"`records` expected to be List or Callable, recieved {type(self.records)}")
        return 1

    def sanitize_labels(self):
        if isinstance(self.labels, List):
            print(f"labels: list with {len(self.labels)} elements")
        else:
            raise TypeError(f"`labels` expected to be List, recieved {type(self.labels)}")
        if len(self.labels) > 24:
            raise ValueError(f"Max no of labels (classes) supported: 24. Supplied: {len(self.labels)}")
        return 1

    def sanitize_output(self):
        if self.output.suffix == ".csv":
            print(f"Saving output to {self.output}")
        else:
            raise ValueError(f"`output` expected to point to a csv file, recieved {self.output}")
        return 1

    def serialize(self, path: Union[str, Path]):
        with open(Path(path), "wb") as output:
            pickle.dump(
                [self.records, self.labels, self.output, self.shortcuts, self.legal_keystrokes, self.shortcuts2labels,],
                output,
            )
        return self

    def deserialize(self, path: Union[str, Path]):
        with open(Path(path), "rb") as _input:
            (
                self.records,
                self.labels,
                self.output,
                self.shortcuts,
                self.legal_keystrokes,
                self.shortcuts2labels,
            ) = pickle.load(_input)
        return self

    def __init__(
        self,
        records: Union[List[str], Callable] = [],  # ToDo: support dataframes
        labels: List[str] = [],
        output: Union[str, Path] = None,
    ):
        self.records = records
        self.labels = labels
        self.output = Path("annotations.csv")
        if output is not None:
            self.output = Path(output)
        self.sanitize_records()
        self.sanitize_labels()
        self.sanitize_output()

        column_names = ["id", "text", "label", "user", "annotated_at"]
        self.records = pd.DataFrame(columns=column_names)
        for i in range(len(records)):
            self.records.loc[i] = {
                "id": i,
                "text": records[i],
                "label": "",
                "user": "",
                "annotated_at": "",
            }

        shortcuts_all = (
            list(range(1, 10)) + [0] + ["q", "w", "e", "r", "t", "y"] + ["a", "s", "d", "f"] + ["z", "x", "c", "v"]
        )
        shortcuts = shortcuts_all[: len(self.labels)]
        self.shortcuts = [str(s) for s in shortcuts]
        self.legal_keystrokes = self.shortcuts + ["Q", "E", "R"]
        self.shortcuts2labels = dict(zip(self.shortcuts, self.labels))

    def __call__(self, path: Union[str, Path]):
        self.deserialize(path)
        return self

    def __repr__(self):
        return f"`labels`: {self.labels} \n`output`: {self.output}, \n`shortcuts`: {self.shortcuts}, \n`legal_keystrokes`: {self.legal_keystrokes}, \n`shortcuts2labels`: {self.shortcuts2labels}"

    @staticmethod
    def cprint(s, color):
        if colored:
            print(colored(s, color))
        else:
            print(s)

    def print_prompt(self, record):
        print("-" * 20)
        print(f"Document:\n{record}\n")
        print("Labels:")
        for i in range(0, len(self.shortcuts), 2):
            self.cprint(
                f"{self.labels[i]} (press {self.shortcuts[i]}) \t {self.labels[i+1]} (press {self.shortcuts[i+1]})",
                "blue",
            )
        print("\nPress R: Re-annotate last doc (ToDo)")
        print("Press Q or E: Exit session")
        return 1

    def get_input(self):
        user_input = None
        while user_input not in self.legal_keystrokes:
            print("Prompt (case-sensitive): ")
            user_input = input()
            if user_input not in self.legal_keystrokes:
                print("Please type a valid shortcut!")
                continue
        return user_input

    def get_record(self):
        return self.records[self.records.label.eq("")].sample(1)

    def update_record(self, loc, dict):
        self.records.loc[loc] = dict
        return self

    def commit(self):
        self.records.to_csv(self.output, index=False, quotechar='"')
        self.serialize(self.output.with_suffix(".pkl"))
        return self

    def annotate(self, user_name: str = None, update_freq: int = 5):
        f = Figlet(font="slant")
        print(f.renderText("labeltext"))
        if user_name is None:
            print("Please provide your username to be associated with annotations")
            user_name = input()
        idx = 0
        while True:
            try:
                record = self.get_record()
            except ValueError:
                self.commit()
                print("All samples have been annotated")
                break
            if record is None:
                self.commit()
                break
            doc = record.text.values[0]
            loc = record.id
            self.print_prompt(doc)
            user_input = self.get_input()
            print(f"You typed {user_input}")

            if user_input in ["Q", "E"]:
                self.commit()
                break
            elif user_input in ["R"]:
                pass  # to be implemented
            elif user_input in self.shortcuts:
                label = self.shortcuts2labels[user_input]
            else:
                raise ValueError(f"Unknown shortcut. You typed {user_input}.")
            self.records.loc[loc, "label"] = label
            self.records.loc[loc, "user"] = user_name
            self.records.loc[loc, "annotated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            idx += 1
            if (idx % update_freq) == 0:
                self.commit()
        print("-" * 20)
        print("Annotation session complete")
        print(f"{idx} document(s) annotated")
