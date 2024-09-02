import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QDialog, QDialogButtonBox, QMessageBox, QWidget,
    QLabel, QPushButton, QTabWidget, QTableWidget, QHeaderView, QAbstractItemView,
    QGridLayout, QVBoxLayout, QHBoxLayout, QFormLayout, QTextEdit, QLineEdit, QDateEdit
    )
from PyQt6.QtCore import QSize, Qt, QDate
from models.roadmap import Roadmap
from models.objective import Objective
from models.category import Category
from models.dates import Phase, Timeframe
from models.actionables import Goal, Task
from functools import partial

class RoadmapMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.roadmap = Roadmap()
        self.start_screen()
    
    def start_screen(self):
        self.setWindowTitle("Start Screen")
        self.setMinimumSize(QSize(1200, 800))
        welcome_label = QLabel("Welcome to the Roadmap!", objectName="large-font")
        button = QPushButton("+ Create Objective")
        button.setMinimumSize(300, 50)
        button.clicked.connect(self.objective_dialog)
        layout = QGridLayout()
        layout.addWidget(QLabel(""), 0, 0)
        layout.addWidget(welcome_label, 0, 1, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(button, 1, 1)
        layout.addWidget(QLabel(""), 2, 2)
        apply_layout(self, layout)
            
    def objective_dialog(self):
        dialog = NewObjectiveDialog(self)
        dialog.show()

    def confirm_objective(self, obj: Objective):
        self.roadmap.create_objective(obj)
        self.roadmap_screen()

    def category_dialog(self):
        dialog = NewCategoryDialog(self)
        dialog.show()

    def confirm_category(self, cat: Category):
        try:
            self.roadmap.objectives[0].create_category(cat)
            print("C:", self.roadmap.objectives[0].get_categories_names())
            self.roadmap_screen()
        except Exception as e:
            popup = QMessageBox(QMessageBox.Icon.Warning, "Error", str(e) + "\n\nPlease try again", QMessageBox.StandardButton.Ok)
            popup.exec()
            popup.accepted.connect(popup.accept)

    def phase_dialog(self):
        dialog = NewPhaseDialog(self)
        dialog.show()

    def confirm_phase(self, ph: Phase):
        try:
            self.roadmap.objectives[0].create_phase(ph)
            print("PH:", self.roadmap.objectives[0].get_phases_names())
            self.roadmap_screen()
        except Exception as e:
            popup = QMessageBox(QMessageBox.Icon.Warning, "Error", str(e) + "\n\nPlease try again", QMessageBox.StandardButton.Ok)
            popup.exec()
            popup.accepted.connect(popup.accept)

    def goal_dialog(self, category, phase):
        dialog = NewGoalDialog(self, category, phase)
        dialog.show()

    def confirm_goal(self, gl: Goal):
        try:
            self.roadmap.objectives[0].add_goal(gl)
            print("G:", self.roadmap.objectives[0].get_goals_names())
            self.roadmap_screen()
        except Exception as e:
            popup = QMessageBox(QMessageBox.Icon.Warning, "Error", str(e) + "\n\nPlease try again", QMessageBox.StandardButton.Ok)
            popup.exec()
            popup.accepted.connect(popup.accept)

    def goal_details(self, goal):
        dialog = GoalDetailsDialog(self, goal)
        dialog.show()

    def roadmap_screen(self):
        first_objective = self.roadmap.objectives[0]
        self.setWindowTitle("Roadmap")
        description_label = QLabel("Objective: " + first_objective.description)
        timeframe_label = QLabel(self.format_timeframe(first_objective.timeframe))
        layout = QVBoxLayout()
        roadmap_table = QTableWidget(2, 2)
        def row_count():
            return roadmap_table.rowCount()
        def col_count():
            return roadmap_table.columnCount()  
        self.format_table(roadmap_table)       
        self.format_categories(first_objective, roadmap_table, row_count)
        self.format_phases(first_objective, roadmap_table, col_count)
        self.format_category_and_phase_buttons(roadmap_table, row_count, col_count)
        self.format_goals_and_goal_buttons(first_objective, roadmap_table, row_count, col_count)
        layout.addWidget(description_label, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(timeframe_label, 0, Qt.AlignmentFlag.AlignCenter) 
        layout.addWidget(roadmap_table)
        apply_layout(self, layout)

    def format_timeframe(self, tf : Timeframe):
        start_date_string = tf.start.strftime("%b %d, %Y")
        end_date_string = tf.end.strftime("%b %d, %Y")
        timeframe_string = start_date_string + " - " + end_date_string
        return timeframe_string
    
    def format_table(self, roadmap_table: QTableWidget):
        roadmap_table.verticalHeader().setVisible(False)
        roadmap_table.verticalHeader().setStretchLastSection(True)
        roadmap_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        roadmap_table.verticalHeader().setDefaultSectionSize(100) 
        roadmap_table.horizontalHeader().setVisible(False)
        roadmap_table.horizontalHeader().setStretchLastSection(True)
        roadmap_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        roadmap_table.horizontalHeader().setDefaultSectionSize(320)
        roadmap_table.setColumnWidth(0, 200)
        roadmap_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        roadmap_table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        roadmap_table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def format_categories(self, first_objective: Objective, roadmap_table: QTableWidget, row_count):
        for cat in first_objective.categories:
            roadmap_table.insertRow(row_count() - 1)
            cat_label = QLabel(cat.name)
            cat_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            roadmap_table.setCellWidget(row_count() - 2, 0, cat_label)

    def format_phases(self, first_objective: Objective, roadmap_table: QTableWidget, col_count):
        for ph in first_objective.phases:
            roadmap_table.insertColumn(col_count() - 1)
            phase_label = QLabel(ph.name + "\n" + self.format_timeframe(ph.timeframe))
            phase_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            roadmap_table.setCellWidget(0, col_count() - 2, phase_label)

    def format_category_and_phase_buttons(self, roadmap_table: QTableWidget, row_count, col_count):
        category_button = QPushButton("+ Category")
        phase_button = QPushButton("+ Phase")
        roadmap_table.setCellWidget(row_count() - 1, 0, category_button)
        roadmap_table.setCellWidget(0, col_count() - 1, phase_button)
        category_button.clicked.connect(self.category_dialog)
        phase_button.clicked.connect(self.phase_dialog)

    def format_goals_and_goal_buttons(self, first_objective: Objective, roadmap_table: QTableWidget, row_count, col_count):
        for col in range(1, col_count() - 1):
            ph = first_objective.phases[col - 1]
            for row in range(1, row_count() - 1):
                cat = first_objective.categories[row - 1]
                goals_and_goal_button = QWidget()
                goals_layout = QVBoxLayout()
                for goal in first_objective.goals:
                    if goal.category == cat and goal.phase == ph:
                        goal_details_button = QPushButton("Goal: " + goal.name)
                        goal_details_button.clicked.connect(partial(self.goal_details, goal))
                        goals_layout.addWidget(goal_details_button)
                goal_button = QPushButton("+ Goal")
                goal_button.clicked.connect(partial(self.goal_dialog, cat, ph)) 
                goals_layout.addWidget(goal_button)
                goals_and_goal_button.setLayout(goals_layout)
                roadmap_table.setCellWidget(row, col, goals_and_goal_button)

class NewCreationDialog(QDialog):
    def __init__(self, window: RoadmapMainWindow):
        super().__init__(window)
        self.setWindowTitle("Create")
        self.setMinimumSize(QSize(600, 400))
        self.setVisible(True)

class NewObjectiveDialog(NewCreationDialog):
    def __init__(self, window):
        super().__init__(window)        
        self.setWindowTitle("Create Objective")
        description_field = QTextEdit()
        description_field.setMaximumSize(600, 100)
        start_date_field = QDateEdit()
        format_date_field(start_date_field)
        end_date_field = QDateEdit()
        format_date_field(end_date_field)
        dialog_buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)
        layout = QFormLayout()
        layout.addRow("Objective\nDescription:", description_field)
        layout.addRow("Start date:", start_date_field)
        layout.addRow("End date:", end_date_field)
        layout.addRow(dialog_buttons)
        self.setLayout(layout)
        dialog_buttons.rejected.connect(self.reject)
        dialog_buttons.accepted.connect(self.accept)
        dialog_buttons.accepted.connect(lambda: window.confirm_objective(
            Objective(description_field.toPlainText(), start_date_field.date().toPyDate(), end_date_field.date().toPyDate())))

class NewCategoryDialog(NewCreationDialog):
    def __init__(self, window):
        super().__init__(window)
        self.setWindowTitle("Create New Category")
        name_field = QLineEdit()
        dialog_buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)
        layout = QFormLayout()
        layout.addRow("Name: ", name_field)
        layout.addRow(dialog_buttons)
        dialog_buttons.accepted.connect(self.accept)
        dialog_buttons.accepted.connect(lambda: window.confirm_category(Category(name_field.text())))
        dialog_buttons.rejected.connect(self.reject)
        self.setLayout(layout)

class NewPhaseDialog(NewCreationDialog):
    def __init__(self, window):
        super().__init__(window)
        self.setWindowTitle("Create New Phase")
        name_field = QLineEdit()
        start_date_field = QDateEdit()
        format_date_field(start_date_field)
        end_date_field = QDateEdit()
        format_date_field(end_date_field)
        dialog_buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)
        layout = QFormLayout()
        layout.addRow("Name:", name_field)
        layout.addRow("Start Date:", start_date_field)
        layout.addRow("End Date:", end_date_field)
        layout.addRow(dialog_buttons)
        dialog_buttons.accepted.connect(self.accept)
        dialog_buttons.accepted.connect(lambda: window.confirm_phase(
            Phase(name_field.text(), start_date_field.date().toPyDate(), end_date_field.date().toPyDate())))
        dialog_buttons.rejected.connect(self.reject)
        self.setLayout(layout)

class NewGoalDialog(NewCreationDialog):
    def __init__(self, window: RoadmapMainWindow, category, phase):
        super().__init__(window)        
        self.setWindowTitle("Create Goal")        
        name_field = QLineEdit()
        description_field = QTextEdit()
        description_field.setMaximumSize(600, 100)
        dialog_buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)
        layout = QFormLayout()
        layout.addRow("Name:", name_field)
        layout.addRow("Description:", description_field)
        layout.addRow(dialog_buttons)
        dialog_buttons.rejected.connect(self.reject)
        dialog_buttons.accepted.connect(self.accept)
        dialog_buttons.accepted.connect(lambda: window.confirm_goal(
            Goal(name_field.text(), category, description_field.toPlainText(), phase)))
        self.setLayout(layout)

class GoalDetailsDialog(QDialog):
    def __init__(self, window: QDialog, goal: Goal):
        super().__init__(window)
        self.setWindowTitle("Goal Details")
        self.setMinimumSize(QSize(600, 400))
        self.setVisible(True)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Goal: " + goal.name))
        layout.addWidget(QLabel("Description:\n" + goal.description))
        layout.addWidget(QLabel("Sub-Actionable(s):"))
        subs_widget = QWidget()
        subs_layout = QHBoxLayout()
        for sub in goal.subs:
            if isinstance(sub, (Goal)):
                sub_details_button = QPushButton("Goal: " + sub.name)
            else:
                sub_details_button = QPushButton("Task: " + sub.name) 
            sub_details_button.clicked.connect(partial(self.details, sub))
            subs_layout.addWidget(sub_details_button)
        subs_widget.setLayout(subs_layout)
        layout.addWidget(subs_widget)
        sub_button = QPushButton("+ Sub-Actionable (Goal or Task)")
        sub_button.clicked.connect(self.accept)
        sub_button.clicked.connect(lambda: self.sub_dialog(goal))
        layout.addWidget(sub_button)
        dialog_button = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        dialog_button.clicked.connect(self.accept)
        layout.addWidget(dialog_button)
        self.setLayout(layout)
    
    def sub_dialog(self, parent_goal):
        dialog = NewSubDialog(self, parent_goal)
        dialog.show()

    def confirm_sub(self, parent: Goal, sub):
        try:
            parent.add_sub(sub)
            print("Subs:", parent.get_subs_names_and_types())
            self.goal_details(parent)
        except Exception as e:
            popup = QMessageBox(QMessageBox.Icon.Warning, "Error", str(e) + "\n\nPlease try again", QMessageBox.StandardButton.Ok)
            popup.exec()
            popup.accepted.connect(popup.accept)

    def goal_details(self, goal):
        dialog = GoalDetailsDialog(self, goal)
        dialog.show()
    
    def task_details(self, task):
        dialog = TaskDetailsDialog(self, task)
        dialog.show()

    def details(self, sub):
        if isinstance(sub, (Goal)):
            self.goal_details(sub)
        else:
            self.task_details(sub)

class TaskDetailsDialog(QDialog):
    def __init__(self, window: GoalDetailsDialog, task: Task):
        super().__init__(window)        
        self.setWindowTitle("Task Details")
        self.setMinimumSize(QSize(600, 400))
        self.setVisible(True)
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Task: " + task.name))
        layout.addWidget(QLabel("Due Date: " + task.due.strftime("%b %d, %Y")))
        dialog_button = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        dialog_button.clicked.connect(self.accept)
        layout.addWidget(dialog_button)
        self.setLayout(layout)

class NewSubDialog(NewCreationDialog):
    def __init__(self, window, parent_goal: Goal):
        super().__init__(window)
        self.setWindowTitle("Create Sub-Actionable")
        layout = QFormLayout()
        tabs = QTabWidget()
        goal_tab = QWidget()
        goal_tab.setLayout(self.goal_fields(window, parent_goal, parent_goal.category, parent_goal.phase))
        task_tab = QWidget()
        task_tab.setLayout(self.task_fields(window, parent_goal, parent_goal.category))
        tabs.addTab(goal_tab, "Goal")        
        tabs.addTab(task_tab, "Task")
        layout.addWidget(tabs)
        self.setLayout(layout)
    
    def goal_fields(self, window: GoalDetailsDialog, parent_goal, category, phase):
        name_field = QLineEdit()
        description_field = QTextEdit()
        description_field.setMaximumSize(600, 100)
        dialog_buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)
        layout = QFormLayout()
        layout.addRow("Name:", name_field)
        layout.addRow("Description:", description_field)
        layout.addRow(dialog_buttons)
        dialog_buttons.rejected.connect(self.reject)
        dialog_buttons.accepted.connect(self.accept)
        dialog_buttons.accepted.connect(lambda: window.confirm_sub(
            parent_goal,
            Goal(name_field.text(), category, description_field.toPlainText(), phase)))
        return layout

    def task_fields(self, window: GoalDetailsDialog, parent_goal, category):
        name_field = QLineEdit()
        date_field = QDateEdit()
        format_date_field(date_field)
        dialog_buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)
        layout = QFormLayout()
        layout.addRow("Name:", name_field)
        layout.addRow("Due Date:", date_field)
        layout.addRow(dialog_buttons)
        dialog_buttons.rejected.connect(self.reject)
        dialog_buttons.accepted.connect(self.accept)
        dialog_buttons.accepted.connect(lambda: window.confirm_sub(
            parent_goal,
            Task(name_field.text(), category, date_field.date().toPyDate())))
        return layout

def format_date_field(date_field: QDateEdit):        
    date_field.setDisplayFormat("MMM d, yyyy")
    date_field.setCalendarPopup(True)
    date_field.setDate(QDate.currentDate())

def apply_layout(window: QMainWindow, layout):
    central_widget = QWidget()
    central_widget.setLayout(layout)
    window.setCentralWidget(central_widget)

def run_application():
    app = QApplication(sys.argv)
    app.setStyleSheet("""QLabel, QPushButton, QTextEdit, QLineEdit, QDateEdit, QTabWidget {font-size: 16pt}
                      QLabel#large-font {font-size: 24pt}""")
    window = RoadmapMainWindow()
    window.show()
    sys.exit(app.exec())