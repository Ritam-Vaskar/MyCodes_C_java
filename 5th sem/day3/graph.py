import matplotlib.pyplot as plt


files = ['random.txt', 'random2.txt', 'random3.txt']
steps = [1495, 1429, 1451]
comparisons = [1495, 1429, 1451]
time_taken = [0.000, 0.000, 0.000]

# Plot Steps
plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)
plt.bar(files, steps, color='skyblue')
plt.title('Steps')
plt.ylabel('Count')

# Plot Comparisons
plt.subplot(1, 3, 2)
plt.bar(files, comparisons, color='salmon')
plt.title('Comparisons')
plt.ylabel('Count')

# Plot Time
plt.subplot(1, 3, 3)
plt.bar(files, time_taken, color='lightgreen')
plt.title('Time Taken (s)')
plt.ylabel('Seconds')

plt.tight_layout()
plt.show()
