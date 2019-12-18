from tkinter import *
import os
from collections import defaultdict
import csv


class InputWindow:
    def __init__(self, master=None):
        self.master = master

        self.path = None
        self.path_label = None
        self.output_label = None
        self.path_entry = None
        self.output_entry = None
        self.processBtn = None
        # self.exitBtn = None

        self.create_window()

    def create_window(self):
        self.path_label = Label(self.master, text="Enter path to directory: ")
        self.path_label.grid(row=0, column=0)

        self.output_label = Label(self.master, text="Enter path for the output file: ")
        self.output_label.grid(row=1, column=0)

        # self.path_entry = Entry(self.master, bd=1)
        self.path_entry = Entry(self.master, width=35)
        self.path_entry.grid(row=0, column=1)

        # self.output_entry = Entry(self.master, bd=1)
        self.output_entry = Entry(self.master, width=35)
        self.output_entry.grid(row=1, column=1)

        # self.processBtn = Button(self.master, text='Process', command=self.get_path_from_text_field)
        # self.processBtn.grid(row=2, column=0)
        self.processBtn = Button(self.master, text='Process & Exit', command=self.get_path_from_text_field_exit)
        self.processBtn.grid(row=1, column=2)
        # self.exitBtn = Button(self.master, text='Exit', command=self.master.destroy)
        # self.exitBtn.grid(row=2, column=1)

    def get_path_from_text_field_exit(self):
        self.path = (self.path_entry.get(), self.output_entry.get())
        self.master.destroy()

    def get_path_from_text_field(self):
        self.path = (self.path_entry.get(), self.output_entry.get())


def get_relevant_files(path: str) -> defaultdict:
    results = defaultdict(list)

    for directory in os.listdir(path):
        if os.path.isfile(os.path.join(path, directory)):
            pass
        else:
            directory_path = os.path.join(path, directory) + "/"
            for file in os.listdir(directory_path):
                split_file = file.split("_")
                if "DL" in split_file:
                    file_path = os.path.join(directory_path, file)
                    results[directory_path].append(file_path)
    return results


def get_module_name_from_filestring(filename: str) -> list:
    filename_split = filename.split("/")

    module_name = filename_split[-2]
    return [module_name]


def get_data_of_jth_file(path: str) -> list:

    module_name = get_module_name_from_filestring(path)

    with open(path, "r") as file:
        reader = csv.reader(file)
        data = list(reader)[18:-1]
        data[0] = data[0] + data[1]
        del data[1]

        data[0] = ['DEVICE'] + data[0]

        first_two_lines_flag = 0

        cleaned_data = []
        for entry in data:
            cleaned_entry = entry[0:6]
            first_two_lines_flag += 1
            for value in entry[6:]:
                if value is not '':
                    cleaned_entry.append(value)
            new_entry = module_name + cleaned_entry if first_two_lines_flag > 2 else cleaned_entry
            cleaned_data.append(new_entry)
        return cleaned_data


def write_data_to_target_csv(data: list, path: str) -> None:
    with open(path, "w") as target:
        writer = csv.writer(target)
        for block in data:
            for file in block:
                for row in file:
                    writer.writerow(row)
    print("All CSVs joined successfully!")


def create_output_file(files: defaultdict, output: str) -> None:
    # sorting the directories in ascending order and keeping the order in a list
    ordered_file_names = sorted(files)

    # for each directory, sort the list of entries by name (more importantly date) in ascending order (older->newer)
    for key in ordered_file_names:
        files[key] = sorted(files[key])

    i = len(files[ordered_file_names[0]])

    entire_file_text = []

    for j in range(i):
        all_entries_one_date = []
        for key in ordered_file_names:
            all_entries_one_date.append(get_data_of_jth_file(files[key][j]))
            all_entries_one_date.append([])
        entire_file_text.append(all_entries_one_date)

    write_data_to_target_csv(entire_file_text, output_path)


if __name__ == '__main__':
    master_window = Tk()
    master_window.title('CSVJoiner')

    sub_window = InputWindow(master_window)
    master_window.mainloop()
    root_path, output_path = sub_window.path

    test = get_relevant_files(root_path)
    create_output_file(test, output_path)