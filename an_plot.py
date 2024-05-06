# import matplotlib.pyplot as plt
# import numpy as np
#
# # Expanded list of subtask labels with hypothetical frequencies
expanded_subtasks = ['PU', 'GOT', 'NT', 'RH', 'CS', 'GDT', 'ST', 'RT', 'HO', 'HV', 'PT', 'THP', 'CG',
                     'AF', 'LA', 'SO', 'SI', 'EC']
# # Assuming an even distribution of occurrences for simplicity
# expanded_frequencies = np.random.randint(40, 150, size=len(expanded_subtasks))
#
# # Generate a unique color for each subtask using a colormap
# colors = plt.cm.viridis(np.linspace(0, 1, len(expanded_subtasks)))
#
# # Plotting the expanded subtask frequencies
# plt.figure(figsize=(16, 9))
# plt.bar(expanded_subtasks, expanded_frequencies, color=colors)
# plt.title('Distribution of Subtask Labels Across Tasks', fontsize=22)
# plt.xlabel('Subtask Label', fontsize=16)
# plt.ylabel('Frequency', fontsize=16)
# plt.xticks(rotation=45)
# plt.tight_layout()
# # save as pdf
# plt.savefig('expanded_subtask_frequencies.pdf')
# plt.show()
#
#
#
#
import matplotlib.pyplot as plt
import numpy as np
# Task types for visualization
selected_task_types = ['BIAH', 'Tower', 'Stairway', 'Bridge']

# Generating hypothetical frequency data for each subtask across selected task types
# This time, ensuring we include all 20 subtasks
np.random.seed(42)
all_freq_data = np.random.randint(1, 15, size=(len(expanded_subtasks), len(selected_task_types)))

# Preparing the plot
fig, axes = plt.subplots(len(selected_task_types), 1, figsize=(18, 20), sharey=True)

for i, task_type in enumerate(selected_task_types):
    axes[i].bar(expanded_subtasks, all_freq_data[:, i], color=np.random.rand(3,))
    axes[i].set_title(f'Subtask Frequency in {task_type} Task', fontsize=16)
    axes[i].set_ylabel('Frequency', fontsize=16)
    axes[i].set_ylim(0, 20)  # Assuming a maximum frequency to ensure consistency in scale

plt.xlabel('Subtask Labels', fontsize=16)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('subtask_frequency_by_task_type.pdf')
plt.show()
