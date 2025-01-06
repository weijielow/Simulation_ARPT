import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import random
class InitialSettingsDialog(simpledialog.Dialog):
    def body(self, master):
        self.title("Initial Simulation Settings")

        # Public Transport Frequency
        ttk.Label(master, text="Public Transport Frequency Level:").grid(row=0, column=0, sticky=tk.W)
        self.transport_freq_value = ttk.Label(master, text="0.50")  # Label for slider value
        self.transport_freq_value.grid(row=0, column=2, sticky=tk.E)
        self.transport_freq_slider = ttk.Scale(master, from_=0, to=1, orient=tk.HORIZONTAL,
                                               command=self.update_transport_freq_value)
        self.transport_freq_slider.set(0.5)  # Set to middle
        ttk.Label(master, text="Weak").grid(row=1, column=0, sticky=tk.E)
        ttk.Label(master, text="Strong").grid(row=1, column=2, sticky=tk.E)
        self.transport_freq_slider.grid(row=1, column=1, sticky="we")

        # Affordable Rate
        ttk.Label(master, text="Affordable Rate:").grid(row=2, column=0, sticky=tk.W)
        self.affordable_rate_value = ttk.Label(master, text="0.50")  # Label for slider value
        self.affordable_rate_value.grid(row=2, column=2, sticky=tk.E)
        self.affordable_rate_slider = ttk.Scale(master, from_=0, to=1, orient=tk.HORIZONTAL,
                                                command=self.update_affordable_rate_value)
        self.affordable_rate_slider.set(0.5)  # Set to middle
        ttk.Label(master, text="Weak").grid(row=3, column=0, sticky=tk.E)
        ttk.Label(master, text="Strong").grid(row=3, column=2, sticky=tk.E)
        self.affordable_rate_slider.grid(row=3, column=1, sticky="we")

        # Facility Availability
        ttk.Label(master, text="Facility Availability Level:").grid(row=4, column=0, sticky=tk.W)
        self.facility_avail_value = ttk.Label(master, text="0.50")  # Label for slider value
        self.facility_avail_value.grid(row=4, column=2, sticky=tk.E)
        self.facility_avail_slider = ttk.Scale(master, from_=0, to=1, orient=tk.HORIZONTAL,
                                               command=self.update_facility_avail_value)
        self.facility_avail_slider.set(0.5)  # Set to middle
        ttk.Label(master, text="Weak").grid(row=5, column=0, sticky=tk.E)
        ttk.Label(master, text="Strong").grid(row=5, column=2, sticky=tk.E)
        self.facility_avail_slider.grid(row=5, column=1, sticky="we")

        # Safety Level
        ttk.Label(master, text="Safety Level:").grid(row=6, column=0, sticky=tk.W)
        self.safety_level_value = ttk.Label(master, text="0.50")  # Label for slider value
        self.safety_level_value.grid(row=6, column=2, sticky=tk.E)
        self.safety_level_slider = ttk.Scale(master, from_=0, to=1, orient=tk.HORIZONTAL,
                                             command=self.update_safety_level_value)
        self.safety_level_slider.set(0.5)  # Set to middle
        ttk.Label(master, text="Weak").grid(row=7, column=0, sticky=tk.E)
        ttk.Label(master, text="Strong").grid(row=7, column=2, sticky=tk.E)
        self.safety_level_slider.grid(row=7, column=1, sticky="we")

        # Number of Days to Simulate (Text Input)
        ttk.Label(master, text="Number of Months to Simulate:").grid(row=8, column=0, sticky=tk.W)
        self.simulation_days_entry = ttk.Entry(master)
        self.simulation_days_entry.insert(0, "100")  # Default value
        self.simulation_days_entry.grid(row=8, column=1, columnspan=2, sticky="we")

        return self.transport_freq_slider  # initial focus

    # Methods to update slider values dynamically
    def update_transport_freq_value(self, value):
        self.transport_freq_value.config(text=f"{float(value):.2f}")

    def update_affordable_rate_value(self, value):
        self.affordable_rate_value.config(text=f"{float(value):.2f}")

    def update_facility_avail_value(self, value):
        self.facility_avail_value.config(text=f"{float(value):.2f}")

    def update_safety_level_value(self, value):
        self.safety_level_value.config(text=f"{float(value):.2f}")

    def apply(self):
        try:
            simulation_days_str = self.simulation_days_entry.get()
            # Check if the input is empty
            if not simulation_days_str:
                raise ValueError("The number of days cannot be empty.")

            simulation_days = int(simulation_days_str)
            if simulation_days <= 0:
                raise ValueError("The number of days must be greater than zero.")

            self.result = {
                "transport_freq": self.transport_freq_slider.get(),
                "affordable_rate": self.affordable_rate_slider.get(),
                "facility_avail": self.facility_avail_slider.get(),
                "safety_level": self.safety_level_slider.get(),
                "simulation_days": simulation_days
            }


        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            self.result = None  # Ensure result remains None to indicate invalid input


class NodeInputDialog(simpledialog.Dialog):
    def __init__(self, parent):
        # Track previous values of sliders
        self.previous_values = {"primary": 0, "secondary": 0, "tertiary": 0, "quaternary": 0}
        self.weights = {"primary": 0.25, "secondary": 0.5, "tertiary": 0.75, "quaternary": 1.0}
        super().__init__(parent)

    def body(self, master):
        self.title("Node Details")

        # Rearranged sequence: Total Land as the first questions

        ttk.Label(master, text="Total Land (km²):").grid(row=0, column=0)
        self.land_entry = ttk.Entry(master)
        self.land_entry.grid(row=0, column=1)

        # Changed Government Regulation to dropdown menu
        ttk.Label(master, text="Government Regulation:").grid(row=1, column=0)
        self.government_regulation_var = tk.StringVar(value="Select Regulation")
        self.government_regulation_dropdown = ttk.Combobox(master, textvariable=self.government_regulation_var)
        self.government_regulation_dropdown['values'] = [
            "Irregular Regulation", "Weak Regulation", "Intermediate Regulation", "Strong Regulation"
        ]
        self.government_regulation_dropdown.grid(row=1, column=1)

        # Public Transit Rate
        ttk.Label(master, text="Public Transit Rate:").grid(row=2, column=0, sticky=tk.W)
        self.public_transit_value = ttk.Label(master, text="0.50")  # Label for slider value
        self.public_transit_value.grid(row=2, column=2, sticky=tk.E)
        self.public_transit_slider = ttk.Scale(master, from_=0, to=1, orient=tk.HORIZONTAL,
                                               command=self.update_public_transit_value)
        self.public_transit_slider.set(0.5)  # Set to middle
        ttk.Label(master, text="Low").grid(row=3, column=0, sticky=tk.E)
        ttk.Label(master, text="High").grid(row=3, column=2, sticky=tk.E)
        self.public_transit_slider.grid(row=3, column=1, sticky="we")

        # Percentage of Usable Land
        ttk.Label(master, text="Percentage of Usable Land:").grid(row=4, column=0, sticky=tk.W)
        self.land_usable_value = ttk.Label(master, text="50%")  # Label for slider value
        self.land_usable_value.grid(row=4, column=2, sticky=tk.E)
        self.land_usable_slider = ttk.Scale(master, from_=0, to=100, orient=tk.HORIZONTAL,
                                            command=self.update_land_usable_value)
        self.land_usable_slider.set(50)  # Set to middle
        ttk.Label(master, text="0%").grid(row=5, column=0, sticky=tk.E)
        ttk.Label(master, text="100%").grid(row=5, column=2, sticky=tk.E)
        self.land_usable_slider.grid(row=5, column=1, sticky="we")

        # Sliders for Economic Activity Types
        ttk.Label(master, text="").grid(row=6, column=0, sticky=tk.W)
        ttk.Label(master, text="Economic Activity Type:").grid(row=7, column=0, sticky=tk.W)
        self.weight_button = ttk.Button(master, text="Weights", command=self.open_weight_dialog)
        self.weight_button.grid(row=7, column=1, sticky=tk.W)

        # Primary Activity Level Slider
        ttk.Label(master, text="Primary Activity Level:").grid(row=8, column=0, sticky=tk.W)
        self.primary_value = tk.DoubleVar(value=0.0)  # Separate variable for slider value
        self.primary_value_label = ttk.Label(master, text="0.00")
        self.primary_value_label.grid(row=8, column=2, sticky=tk.E)
        self.primary_slider = ttk.Scale(master, from_=0, to=1, orient=tk.HORIZONTAL,
                                        command=self.update_sliders, variable=self.primary_value)
        self.primary_slider.grid(row=9, column=1, sticky="we")
        ttk.Label(master, text="Low").grid(row=9, column=0, sticky=tk.E)
        ttk.Label(master, text="High").grid(row=9, column=2, sticky=tk.E)

        # Secondary Activity Level Slider
        ttk.Label(master, text="Secondary Activity Level:").grid(row=10, column=0, sticky=tk.W)
        self.secondary_value = tk.DoubleVar(value=0.0)  # Separate variable for slider value
        self.secondary_value_label = ttk.Label(master, text="0.00")
        self.secondary_value_label.grid(row=10, column=2, sticky=tk.E)
        self.secondary_slider = ttk.Scale(master, from_=0, to=1, orient=tk.HORIZONTAL,
                                          command=self.update_sliders, variable=self.secondary_value)
        self.secondary_slider.grid(row=11, column=1, sticky="we")
        ttk.Label(master, text="Low").grid(row=11, column=0, sticky=tk.E)
        ttk.Label(master, text="High").grid(row=11, column=2, sticky=tk.E)

        # Tertiary Activity Level Slider
        ttk.Label(master, text="Tertiary Activity Level:").grid(row=12, column=0, sticky=tk.W)
        self.tertiary_value = tk.DoubleVar(value=0.0)  # Separate variable for slider value
        self.tertiary_value_label = ttk.Label(master, text="0.00")
        self.tertiary_value_label.grid(row=12, column=2, sticky=tk.E)
        self.tertiary_slider = ttk.Scale(master, from_=0, to=1, orient=tk.HORIZONTAL,
                                         command=self.update_sliders, variable=self.tertiary_value)
        self.tertiary_slider.grid(row=13, column=1, sticky="we")
        ttk.Label(master, text="Low").grid(row=13, column=0, sticky=tk.E)
        ttk.Label(master, text="High").grid(row=13, column=2, sticky=tk.E)

        # Quaternary Activity Level Slider
        ttk.Label(master, text="Quaternary Activity Level:").grid(row=14, column=0, sticky=tk.W)
        self.quaternary_value = tk.DoubleVar(value=0.0)  # Separate variable for slider value
        self.quaternary_value_label = ttk.Label(master, text="0.00")
        self.quaternary_value_label.grid(row=14, column=2, sticky=tk.E)
        self.quaternary_slider = ttk.Scale(master, from_=0, to=1, orient=tk.HORIZONTAL,
                                           command=self.update_sliders, variable=self.quaternary_value)
        self.quaternary_slider.grid(row=15, column=1, sticky="we")
        ttk.Label(master, text="Low").grid(row=15, column=0, sticky=tk.E)
        ttk.Label(master, text="High").grid(row=15, column=2, sticky=tk.E)

        return self.land_entry  # initial focus

    def update_public_transit_value(self, value):
        self.public_transit_value.config(text=f"{float(value):.2f}")

    def update_land_usable_value(self, value):
        self.land_usable_value.config(text=f"{int(float(value))}%")

    def update_sliders(self, *args):
        # Get current slider values
        primary_value = self.primary_value.get()
        secondary_value = self.secondary_value.get()
        tertiary_value = self.tertiary_value.get()
        quaternary_value = self.quaternary_value.get()

        # Total current values
        total = primary_value + secondary_value + tertiary_value + quaternary_value

        # Check if total exceeds 1
        if total > 1:
            # Revert the slider that triggered the event
            if self.previous_values["primary"] != primary_value:
                self.primary_slider.set(self.previous_values["primary"])
            elif self.previous_values["secondary"] != secondary_value:
                self.secondary_slider.set(self.previous_values["secondary"])
            elif self.previous_values["tertiary"] != tertiary_value:
                self.tertiary_slider.set(self.previous_values["tertiary"])
            elif self.previous_values["quaternary"] != quaternary_value:
                self.quaternary_slider.set(self.previous_values["quaternary"])

        # Update displayed values
        self.primary_value_label.config(text=f"{self.primary_slider.get():.2f}")
        self.secondary_value_label.config(text=f"{self.secondary_slider.get():.2f}")
        self.tertiary_value_label.config(text=f"{self.tertiary_slider.get():.2f}")
        self.quaternary_value_label.config(text=f"{self.quaternary_slider.get():.2f}")

        # Update previous values
        self.previous_values["primary"] = self.primary_value.get()
        self.previous_values["secondary"] = self.secondary_value.get()
        self.previous_values["tertiary"] = self.tertiary_value.get()
        self.previous_values["quaternary"] = self.quaternary_value.get()

    def open_weight_dialog(self):
        dialog = WeightAdjustmentDialog(self, self.weights)
        if dialog.result:
            self.weights = dialog.result  # Update weights

    def apply(self):
        try:
            # Map government regulation selection to values
            regulation_mapping = {
                "Weak Regulation": 0.25,
                "Intermediate Regulation": 0.5,
                "Strong Regulation": 0.75,
                "Irregular Regulation": "Irregular"  # Special case
            }

            # Validate total land input
            total_land = self.land_entry.get()
            if not total_land.strip() or float(total_land) <= 0:
                raise ValueError("Total Land cannot be empty or zero.")

            # Validate government regulation selection
            regulation_value = regulation_mapping.get(self.government_regulation_var.get(), None)
            if regulation_value is None:
                raise ValueError("Government Regulation must be selected.")

            # Handle irregular regulation separately
            if regulation_value == "Irregular":
                regulation_value = 1  # Initial value
                self.irregular_flag = True  # Flag for irregular behavior
            else:
                self.irregular_flag = False

            # Validate economic activity levels
            primary_value = self.primary_value.get()
            secondary_value = self.secondary_value.get()
            tertiary_value = self.tertiary_value.get()
            quaternary_value = self.quaternary_value.get()
            total_activity_level = primary_value + secondary_value + tertiary_value + quaternary_value

            if total_activity_level != 1.0:
                raise ValueError("The sum of Economic Activity Levels must equal 1.")

            # Calculate final economic activity value
            final_value = (primary_value * self.weights["primary"] +
                           secondary_value * self.weights["secondary"] +
                           tertiary_value * self.weights["tertiary"] +
                           quaternary_value * self.weights["quaternary"])

            # Set result dictionary
            self.result = {
                "total_land": float(total_land),
                "government_regulation": regulation_value,
                "irregular_flag": self.irregular_flag,  # Track if regulation is irregular
                "public_transit_rate": float(self.public_transit_slider.get()),
                "usable_land": float(self.land_usable_slider.get() / 100),
                "economic_activity_level": final_value
            }
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            self.result = None


class WeightAdjustmentDialog(simpledialog.Dialog):
    def __init__(self, parent, current_weights):
        self.current_weights = current_weights  # Dictionary of current weights
        super().__init__(parent)

    def body(self, master):
        self.title("Adjust Weights")

        ttk.Label(master, text="Primary Activity Weight:").grid(row=0, column=0)
        self.primary_weight_entry = ttk.Entry(master)
        self.primary_weight_entry.insert(0, str(self.current_weights["primary"]))
        self.primary_weight_entry.grid(row=0, column=1)

        ttk.Label(master, text="Secondary Activity Weight:").grid(row=1, column=0)
        self.secondary_weight_entry = ttk.Entry(master)
        self.secondary_weight_entry.insert(0, str(self.current_weights["secondary"]))
        self.secondary_weight_entry.grid(row=1, column=1)

        ttk.Label(master, text="Tertiary Activity Weight:").grid(row=2, column=0)
        self.tertiary_weight_entry = ttk.Entry(master)
        self.tertiary_weight_entry.insert(0, str(self.current_weights["tertiary"]))
        self.tertiary_weight_entry.grid(row=2, column=1)

        ttk.Label(master, text="Quaternary Activity Weight:").grid(row=3, column=0)
        self.quaternary_weight_entry = ttk.Entry(master)
        self.quaternary_weight_entry.insert(0, str(self.current_weights["quaternary"]))
        self.quaternary_weight_entry.grid(row=3, column=1)

        return self.primary_weight_entry

    def apply(self):
        try:
            self.result = {
                "primary": float(self.primary_weight_entry.get()),
                "secondary": float(self.secondary_weight_entry.get()),
                "tertiary": float(self.tertiary_weight_entry.get()),
                "quaternary": float(self.quaternary_weight_entry.get())
            }
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid weights.")
            self.result = None

class Node:
    def __init__(self, canvas, x, y, name, transport_freq=0, affordable_rate=0, facility_avail=0, safety_level=0):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.name = name
        self.irregular_flag = False
        self.simulation_days = 0
        self.day_counter = 0
        self.connections = []  # Store connected nodes here
        self.government_regulation = 0
        self.amount_of_land_usable = 0
        self.land_use_rate = 0.5
        self.public_transit_rate = 0
        self.economic_activity_type = 0
        self.total_land = 0
        self.usable_land = 0
        self.total_land_use = 0
        self.amount_of_land_used = 0
        self.movement_ratio = 0
        self.economic_activity_level = 0
        self.employment_rate = 0
        self.quality_of_life = 0
        self.willingness_to_travel = 0.5
        self.short_term_accessibility = 0
        self.long_term_accessibility = 0.5
        self.short_term_economic_activity_level = 0
        self.long_term_economic_activity_level = 0.5
        self.short_term_employment_rate = 0
        self.long_term_employment_rate = 0.5
        self.short_term_quality_of_life = 0
        self.long_term_quality_of_life = 0.5
        self.total_land_usable = 0
        self.convenience_level = 0
        self.public_transport_frequency = transport_freq
        self.affordable_rate = affordable_rate
        self.facility_availability = facility_avail
        self.safety_level = safety_level
        self.history = {
            'public_transit_rate': [],
            'land_use_rate': [],
            'movement_ratio': [],
            'short_term_accessibility': [],
            'long_term_accessibility': [],
            'short_term_economic_activity_level': [],
            'long_term_economic_activity_level': [],
            'short_term_employment_rate': [],
            'long_term_employment_rate': [],
            'short_term_quality_of_life': [],
            'long_term_quality_of_life': [],
            'willingness_to_travel': []
        }
        self.create_node()

    def create_node(self):
        self.oval = self.canvas.create_oval(self.x - 10, self.y - 10, self.x + 10, self.y + 10, fill='blue')
        self.text = self.canvas.create_text(self.x, self.y, text=self.name, fill='white')
        self.canvas.tag_bind(self.oval, '<Button-1>', self.on_click)
        self.canvas.tag_bind(self.text, '<Button-1>', self.on_click)

    def on_click(self, event):
        if not SimulationGUI.drawing_line:
            self.edit_node()

    def edit_node(self):
        dialog = NodeInputDialog(self.canvas)
        if dialog.result:
            self.total_land = dialog.result["total_land"]
            self.government_regulation = dialog.result["government_regulation"]
            self.public_transit_rate = dialog.result["public_transit_rate"]
            self.usable_land = dialog.result["usable_land"]
            self.economic_activity_level = dialog.result["economic_activity_level"]
            self.irregular_flag = dialog.result["irregular_flag"]
            self.update_display()

    def update_display(self):
        info = ""
        for node in self.canvas.master.nodes:
            info += (f"Node {node.name}:\n"
                     f"Government Regulation: {node.government_regulation}\n"
                     f"Public Transit Rate: {node.public_transit_rate}\n"
                     f"total land: {node.total_land}\n\n")
        SimulationGUI.node_info_label.config(text=info)

    def update_attributes(self, delta_t, days):
        # Define unique coefficients for each variable in every equation
        lr1, lr2, lr3 = 0.33, 0.33, 0.34  # Coefficients for Land Use Rate (Lr)
        mr = 0.5  # Coefficients for Movement Ratio (Mr)
        ra = 0.5  # Coefficients for Public Transit Adoption Rate (Ra)
        cr = 0.5  # Coefficients for Convenience rate (Cr)
        wl1, wl2, wl3, = 0.33, 0.33, 0.34  # Coefficients for Willingness to Travel (Wl)
        el = 0.5  # Coefficients for Economic Activity Level (El)
        er = 0.5  # Coefficients for Employment Rate (Er)
        ql = 0.5  # Coefficients for Quality of Life (Ql)
        ac = 0.5  # Coefficients for Accessibility (Ac)

        # Rate control factor
        gamma = 0.8

        # Retrieve simulating days, and check irregular regulation

        self.simulation_days = days
        if self.irregular_flag:
            if self.day_counter >= (self.simulation_days / 2):
                self.government_regulation = 0
        self.day_counter += 1

        # Temporary variables for the current time step
        initial_usable_land = self.usable_land
        initial_land_use_rate = self.land_use_rate
        initial_willingness_to_travel = self.willingness_to_travel
        initial_public_transit_rate = self.public_transit_rate
        initial_long_term_economic_activity_level = self.long_term_economic_activity_level
        initial_long_term_employment_rate = self.long_term_employment_rate
        initial_long_term_quality_of_life = self.long_term_quality_of_life
        initial_long_term_accessibility = self.long_term_accessibility

        # 1. Update total amount of usable land
        updated_usable_land = initial_usable_land + delta_t * gamma * (
                self.government_regulation - initial_usable_land
        ) * initial_usable_land * (1 - initial_usable_land)

        # Calculate total usable land (Tu)
        self.total_land_usable = initial_usable_land * self.total_land

        # Calculate amount of land used (Al)
        self.amount_of_land_used = self.land_use_rate * self.total_land_usable

        # 2. Update Land Use Rate (Lr)
        updated_land_use_rate = initial_land_use_rate + gamma * delta_t * (
                lr1 * initial_long_term_economic_activity_level
                + lr2 * (self.amount_of_land_used / self.total_land)
                + lr3 * self.connectivity()
                - initial_land_use_rate
        ) * initial_land_use_rate * (1 - initial_land_use_rate)

        # Update Movement Ratio (Mr)
        self.movement_ratio = mr * initial_long_term_economic_activity_level + (1 - mr) * initial_willingness_to_travel

        # Update Public Transit Adoption Rate (Ra)
        updated_public_transit_rate = initial_public_transit_rate + gamma * delta_t * (
            ra * self.government_regulation
            + (1 - ra) * initial_willingness_to_travel
            - initial_public_transit_rate
        ) * initial_public_transit_rate * (1 - initial_public_transit_rate)

        # Update Convenience Rate (Cr) - static calculation based on frequency, affordability, facility availability
        self.convenience_level = (cr * self.public_transport_frequency + (1 - cr) * self.affordable_rate) * self.facility_availability

        # Update Willingness to Travel (Wl)
        updated_willingness_to_travel = initial_willingness_to_travel + gamma * delta_t * (
                wl1 * self.connectivity()
                + wl2 * self.safety_level
                + wl3 * self.convenience_level
                - initial_willingness_to_travel
        ) * initial_willingness_to_travel * (1 - initial_willingness_to_travel)

        # Update Economic Activity Level (El) - Short-term and long-term calculation
        self.short_term_economic_activity_level = self.government_regulation * (
                + el * initial_land_use_rate
                + (1 - el) * self.movement_ratio
        )
        updated_long_term_economic_activity_level = initial_long_term_economic_activity_level + gamma * delta_t * (
                self.short_term_economic_activity_level - initial_long_term_economic_activity_level
        ) * initial_long_term_economic_activity_level * (1 - initial_long_term_economic_activity_level)

        # Update Employment Rate (Er)
        self.short_term_employment_rate = (
                er * self.movement_ratio
                + (1 - er) * initial_long_term_economic_activity_level
        )
        updated_long_term_employment_rate = initial_long_term_employment_rate + gamma * delta_t * (
                self.short_term_employment_rate - initial_long_term_employment_rate
        ) * initial_long_term_employment_rate * (1 - initial_long_term_employment_rate)

        # Update Accessibility
        self.short_term_accessibility = ac * initial_land_use_rate + (1 - ac) * self.convenience_level

        updated_long_term_accessibility = initial_long_term_accessibility + gamma * delta_t * (
                self.short_term_accessibility - initial_long_term_accessibility
        ) * initial_long_term_accessibility * (1 - initial_long_term_accessibility)

        # Update Quality of Life (Ql)
        self.short_term_quality_of_life = (
                ql * initial_long_term_employment_rate
                + (1 - ql) * initial_long_term_accessibility
        )
        updated_long_term_quality_of_life = initial_long_term_quality_of_life + gamma * delta_t * (
                self.short_term_quality_of_life - initial_long_term_quality_of_life
        ) * initial_long_term_quality_of_life * (1 - initial_long_term_quality_of_life)

        # Batch update all attributes at the end of the time step
        self.usable_land = updated_usable_land
        self.land_use_rate = updated_land_use_rate
        self.willingness_to_travel = updated_willingness_to_travel
        self.public_transit_rate = updated_public_transit_rate
        self.long_term_economic_activity_level = updated_long_term_economic_activity_level
        self.long_term_employment_rate = updated_long_term_employment_rate
        self.long_term_accessibility = updated_long_term_accessibility
        self.long_term_quality_of_life = updated_long_term_quality_of_life

    def connectivity(self):
        return len(self.connections)

    def update_history(self):
        self.history['public_transit_rate'].append(self.public_transit_rate)
        self.history['land_use_rate'].append(self.land_use_rate)
        self.history['movement_ratio'].append(self.movement_ratio)
        self.history['short_term_accessibility'].append(self.short_term_accessibility)
        self.history['long_term_accessibility'].append(self.long_term_accessibility)
        self.history['short_term_economic_activity_level'].append(self.short_term_economic_activity_level)
        self.history['long_term_economic_activity_level'].append(self.long_term_economic_activity_level)
        self.history['short_term_employment_rate'].append(self.short_term_employment_rate)
        self.history['long_term_employment_rate'].append(self.long_term_employment_rate)
        self.history['short_term_quality_of_life'].append(self.short_term_quality_of_life)
        self.history['long_term_quality_of_life'].append(self.long_term_quality_of_life)
        self.history['willingness_to_travel'].append(self.willingness_to_travel)


class SimulationGUI(tk.Tk):
    drawing_line = False
    node_info_label = None

    def __init__(self):
        super().__init__()
        self.title("Simulation of Social-Economic Impact by ARPT")

        # Add attributes for fixed initial settings
        self.transport_freq = 0
        self.affordable_rate = 0
        self.facility_avail = 0
        self.safety_level = 0
        self.simulation_days = 0

        self.nodes = []
        self.node_names = []
        self.canvas = tk.Canvas(self, width=600, height=600, bg='white')
        self.canvas.grid(row=0, column=0, padx=10, pady=10)

        self.create_control_panel()
        self.current_line = None
        self.start_node = None

        # Prompt for fixed settings when starting
        self.get_initial_settings()

        self.canvas.bind("<ButtonPress-3>", self.start_line)
        self.canvas.bind("<B3-Motion>", self.draw_line)
        self.canvas.bind("<ButtonRelease-3>", self.finish_line)

        # Create a single graph window with empty Figure
        self.fig, self.axs = plt.subplots(2, 4, figsize=(15, 10))
        self.long_term_fig, self.long_term_axs = plt.subplots(2, 4, figsize=(15, 10))
        self.graph_window = None
        self.long_term_graph_window = None
        self.canvas_fig = None
        self.long_term_canvas = None
        self.total_days = 0

    def get_initial_settings(self):
        while True:  # Loop until valid input is received
            dialog = InitialSettingsDialog(self)
            if dialog.result:
                # If we have valid results, extract them
                self.transport_freq = dialog.result["transport_freq"]
                self.affordable_rate = dialog.result["affordable_rate"]
                self.facility_avail = dialog.result["facility_avail"]
                self.safety_level = dialog.result["safety_level"]
                self.simulation_days = dialog.result["simulation_days"]
                break  # Exit the loop if valid input is received
            else:
                # If no valid input, the dialog will remain open
                # and prompt the user to enter values again.
                continue  # Re-invoke the dialog

    def create_control_panel(self):
        control_frame = ttk.Frame(self, padding="10")
        control_frame.grid(row=0, column=1, sticky=tk.N)

        ttk.Label(control_frame, text="Number of Nodes:").grid(row=0, column=0)
        self.num_nodes_entry = ttk.Entry(control_frame)
        self.num_nodes_entry.grid(row=0, column=1)

        ttk.Button(control_frame, text="Generate Nodes", command=self.generate_nodes).grid(row=1, column=0,
                                                                                           columnspan=2)

        ttk.Button(control_frame, text="Start Simulation", command=self.start_simulation).grid(row=2, column=0,
                                                                                               columnspan=2)

        # Label or Treeview to display connections
        ttk.Label(control_frame, text="Node Information:").grid(row=3, column=0, sticky=tk.W)
        SimulationGUI.node_info_label = ttk.Label(control_frame, text="No node selected", justify=tk.LEFT)
        SimulationGUI.node_info_label.grid(row=4, column=0, columnspan=2, sticky=tk.W)

        # Label for displaying connections between nodes
        ttk.Label(control_frame, text="Connections:").grid(row=5, column=0, sticky=tk.W)
        self.connections_label = ttk.Label(control_frame, text="No connections", justify=tk.LEFT)
        self.connections_label.grid(row=6, column=0, columnspan=2, sticky=tk.W)

        # Reset button
        ttk.Button(control_frame, text="Reset", command=self.reset_simulation).grid(row=7, column=0, columnspan=2)

    def reset_simulation(self):
        # Show confirmation dialog
        confirm = messagebox.askyesno(
            title="Reset Simulation",
            message="Are you sure you want to reset the simulation? This will clear all data and nodes."
        )

        if confirm:  # Proceed only if the user confirms
            # Clear all nodes and related attributes
            self.nodes.clear()
            self.node_names.clear()
            self.canvas.delete("all")  # Clear the canvas
            self.connections_label.config(text="No connections")
            SimulationGUI.node_info_label.config(text="No node selected")

            # Reset fixed settings
            self.transport_freq = 0
            self.affordable_rate = 0
            self.facility_avail = 0
            self.safety_level = 0
            self.simulation_days = 0

            # Optionally, re-prompt for initial settings
            self.get_initial_settings()

    def generate_nodes(self):
        try:
            num_nodes = int(self.num_nodes_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of nodes.")
            return

        self.canvas.delete("all")
        self.nodes.clear()
        self.node_names = [chr(65 + i) for i in range(num_nodes)]
        placed_positions = []

        for i, name in enumerate(self.node_names):
            while True:
                x = random.randint(50, 550)
                y = random.randint(50, 550)
                if not any((abs(x - px) < 40 and abs(y - py) < 40) for px, py in placed_positions):
                    placed_positions.append((x, y))
                    break

            node = Node(
                canvas=self.canvas,
                x=x,
                y=y,
                name=name,
                transport_freq=self.transport_freq,
                affordable_rate=self.affordable_rate,
                facility_avail=self.facility_avail,
                safety_level=self.safety_level
            )
            self.nodes.append(node)

    def start_line(self, event):
        item = self.canvas.find_closest(event.x, event.y)
        if item and (self.canvas.type(item) == "oval" or self.canvas.type(item) == "text"):
            self.start_node = self.find_node_by_item(item)
            if self.start_node:  # Only start drawing if a valid node is clicked
                self.current_line = self.canvas.create_line(event.x, event.y, event.x, event.y)
                SimulationGUI.drawing_line = True

    def draw_line(self, event):
        if SimulationGUI.drawing_line and self.current_line:
            self.canvas.coords(self.current_line, self.start_node.x, self.start_node.y, event.x, event.y)

    def finish_line(self, event):
        if self.current_line:
            end_node = self.find_node_by_position(event.x, event.y)
            if end_node and end_node != self.start_node:
                if end_node not in self.start_node.connections:
                    self.canvas.create_line(self.start_node.x, self.start_node.y, end_node.x, end_node.y)
                    self.start_node.connections.append(end_node)
                    end_node.connections.append(self.start_node)
                    self.update_connections_display()  # Update display of connections
                else:
                    messagebox.showwarning("Duplicate Connection", "These nodes are already connected.")
                    self.canvas.delete(self.current_line)
            else:
                messagebox.showwarning("Invalid Connection", "Please connect two different nodes.")
                self.canvas.delete(self.current_line)

            self.current_line = None
            self.start_node = None
            SimulationGUI.drawing_line = False

    def update_connections_display(self):
        connections_text = ""
        for node in self.nodes:
            connections_text += f"{node.name}: {[n.name for n in node.connections]}\n"
        self.connections_label.config(text=connections_text)

    def find_node_by_item(self, item):
        for node in self.nodes:
            if item[0] in (node.oval, node.text):
                return node
        return None

    def find_node_by_position(self, x, y):
        for node in self.nodes:
            if node.x - 10 <= x <= node.x + 10 and node.y - 10 <= y <= node.y + 10:
                return node
        return None

    def start_simulation(self):
        for node in self.nodes:
            node.history = {key: [] for key in node.history.keys()}
        num_days = self.simulation_days
        delta_t = 1

        if not self.graph_window:
            self.create_graph_window()

        # Create long-term graph window only once
        if not self.long_term_graph_window:
            self.create_long_term_graph_window()
        for day in range(num_days):
            for node in self.nodes:
                node.update_attributes(delta_t, num_days)
                node.update_history()

            self.update_graphs(self.total_days + day)
            self.update_long_term_graphs(self.total_days + day)  # Incrementally update the long-term graphs

        self.total_days += num_days
        self.display_node_info()

        # After finishing, ask if the user wants to continue the simulation
        if messagebox.askyesno("Continue Simulation", "Do you want to continue simulating with current values?"):
            self.continue_simulation(delta_t)

    def continue_simulation(self, delta_t):
        while True:  # Loop to repeatedly ask the user if they want to continue
            # Set number of additional days for continuation
            additional_days = simpledialog.askinteger(
                "Continue Simulation",
                "How many additional months do you want to simulate?",
                minvalue=1
            )
            if not additional_days:  # Exit if the user cancels or provides no input
                break

            # Clear previous graphs and recreate them
            self.clear_graph_window()
            self.create_graph_window()

            for day in range(additional_days):
                for node in self.nodes:
                    node.update_attributes(delta_t, additional_days)
                    node.update_history()
                self.update_graphs(self.total_days + day)
                self.update_long_term_graphs(self.total_days + day)

            self.total_days += additional_days
            self.display_node_info()

            # After finishing, ask if the user wants to continue the simulation again
            if not messagebox.askyesno("Continue Simulation",
                                       "Do you want to continue simulating with current values?"):
                break

    def clear_graph_window(self):
        if self.graph_window:
            self.graph_window.destroy()  # Close existing graph window
            self.graph_window = None

    def create_graph_window(self):
        self.graph_window = tk.Toplevel(self)
        self.graph_window.title("Simulation Results")

        # Create a new figure and axes for each graph window
        self.fig = plt.figure(figsize=(15, 10))
        self.axs = [self.fig.add_subplot(2, 2, i + 1) for i in range(4)]  # Changed to 2D plots

        self.canvas_fig = FigureCanvasTkAgg(self.fig, master=self.graph_window)
        self.canvas_fig.get_tk_widget().pack(fill=tk.BOTH, expand=True)


    def update_graphs(self, day):
        # Clear all subplots before updating
        for ax in self.axs:
            ax.clear()

        # Titles for each subplot
        metrics = [
            ('Public Transit Rate', 'public_transit_rate'),
            ('Land Use Rate', 'land_use_rate'),
            ('Movement Ratio', 'movement_ratio'),
            ('Willingness to Travel', 'willingness_to_travel')
        ]

        # Loop through each subplot and metric
        for i, (title, metric) in enumerate(metrics):
            ax = self.axs[i]
            ax.set_title(title)
            ax.set_xlabel('Month')
            ax.set_ylabel('Rate')
            ax.set_ylim(0, 1)  # Set Y-axis range to 0-1

            # Plot each node’s history as a separate line
            for idx, node in enumerate(self.nodes):
                days = range(len(node.history[metric]))  # Days are simply index values
                rates = node.history[metric]  # Metric history over time
                node_label = f'Node {node.name}'

                # Create a 2D line for each node
                ax.plot(days, rates, label=node_label)

            ax.legend()  # Add a legend to each plot for node identification

        self.fig.tight_layout()
        self.canvas_fig.draw()

    def create_long_term_graph_window(self):
        self.long_term_graph_window = tk.Toplevel(self)
        self.long_term_graph_window.title("Short-Term and Long-Term Metrics")

        # Initialize figure for long-term metrics
        self.long_term_fig = plt.figure(figsize=(15, 10))
        self.long_term_axs = []

        # Metrics configuration
        metrics = [
            ('Short-Term Accessibility', 'short_term_accessibility'),
            ('Long-Term Accessibility', 'long_term_accessibility'),
            ('Short-Term Economic Activity Level', 'short_term_economic_activity_level'),
            ('Long-Term Economic Activity Level', 'long_term_economic_activity_level'),
            ('Short-Term Employment Rate', 'short_term_employment_rate'),
            ('Long-Term Employment Rate', 'long_term_employment_rate'),
            ('Short-Term Quality of Life', 'short_term_quality_of_life'),
            ('Long-Term Quality of Life', 'long_term_quality_of_life')
        ]
        self.long_term_metrics = metrics

        # Create subplots with 3D axes
        for i, (title, _) in enumerate(metrics):
            ax = self.long_term_fig.add_subplot(2, 4, i + 1, projection='3d')
            ax.set_title(title)
            ax.set_xlabel('Time Steps (Days)')
            ax.set_ylabel('Nodes')
            ax.set_ylim(0, 1)  # Set Y-axis range to 0-1
            ax.set_zlabel('Value')
            self.long_term_axs.append(ax)

        # Create canvas for the figure
        self.long_term_canvas = FigureCanvasTkAgg(self.long_term_fig, master=self.long_term_graph_window)
        self.long_term_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    import numpy as np

    def update_long_term_graphs(self, day):
        # Clear all subplots before updating
        for ax in self.long_term_axs:
            ax.clear()

        # Adjust figure size
        self.long_term_fig = plt.figure(figsize=(12, 8))  # Adjust as needed

        # Loop through each subplot and metric
        for ax, (title, metric) in zip(self.long_term_axs, self.long_term_metrics):
            ax.set_title(title)
            ax.set_xlabel('Time Steps (Days)')
            ax.set_ylabel('Nodes')
            ax.set_zlabel('Value')

            # Prepare data for surface plot
            days = np.arange(max(len(node.history[metric]) for node in self.nodes))  # X-axis (time steps)
            nodes = np.arange(len(self.nodes))  # Y-axis (nodes)
            X, Y = np.meshgrid(days, nodes)

            # Create Z-axis (values) by populating the surface data
            Z = np.zeros_like(X, dtype=float)
            for idx, node in enumerate(self.nodes):
                history_length = len(node.history[metric])
                Z[idx, :history_length] = node.history[metric]  # Assign metric values for each node

            # Create surface plot
            ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='k', alpha=0.8)

        plt.subplots_adjust(hspace=0.4, wspace=0.4)  # Adjust spacing between subplots
        self.long_term_fig.tight_layout(pad=3.0)  # Ensure tight layout with specified padding
        self.long_term_canvas.draw()

    def display_node_info(self):
        for node in self.nodes:
            print(f"Node {node.name}:")
            print(f" Government Regulation: {node.government_regulation}")
            print(f" Public Transit Rate: {node.public_transit_rate}")
            print(f" Land Use Rate: {node.land_use_rate}")
            print(f" Movement Ratio: {node.movement_ratio}")
            print(f" Short Term Economic Activity Level: {node.short_term_economic_activity_level}")
            print(f" Short Term Employment Rate: {node.short_term_employment_rate}")
            print(f" Short Term Quality of Life: {node.short_term_quality_of_life}")
            print(f" Long Term Economic Activity Level: {node.long_term_economic_activity_level}")
            print(f" Long Term Employment Rate: {node.long_term_employment_rate}")
            print(f" Long Term Quality of Life: {node.long_term_quality_of_life}")
            print(f" Willingness to Travel: {node.willingness_to_travel}")
            print(f" Connections: {[n.name for n in node.connections]}")


if __name__ == "__main__":
    app = SimulationGUI()
    app.mainloop()
