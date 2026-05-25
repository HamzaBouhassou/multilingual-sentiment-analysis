import json
import matplotlib.pyplot as plt
from collections import defaultdict

# Load the filtered comments JSON file
file_path = 'frang1_comments.json'

with open(file_path, 'r', encoding='utf-8') as f:
    comments = json.load(f)

# Initialize counters
total_comments = len(comments)
positive_comments = 0
negative_comments = 0
video_stats = defaultdict(lambda: {'positive': 0, 'negative': 0, 'total': 0})

# Process each comment
for comment in comments:
    video_id = comment.get('video_id', None)
    label = comment.get('label', None)

    if video_id is not None and label is not None:
        if label == 1:
            positive_comments += 1
            video_stats[video_id]['positive'] += 1
        elif label == 0:
            negative_comments += 1
            video_stats[video_id]['negative'] += 1
        
        video_stats[video_id]['total'] += 1
    else:
        print(f"Warning: Comment missing 'video_id' or 'labilise': {comment}")

# Calculate total percentages
total_positive_percentage = (positive_comments / total_comments) * 100
total_negative_percentage = (negative_comments / total_comments) * 100

# Generate statistics for each video and prepare data for grouped bar chart
video_labels = []
video_positive_counts = []
video_negative_counts = []

for video_id, stats in video_stats.items():
    total_video_comments = stats['total']
    positive_count = stats['positive']
    negative_count = stats['negative']

    if total_video_comments > 0:  # Exclude videos with zero comments
        video_labels.append(video_id)
        video_positive_counts.append(positive_count)
        video_negative_counts.append(negative_count)

        # Print video statistics
        print(f"Video ID: {video_id}")
        print(f"  Total Comments: {total_video_comments}")
        print(f"  Positive Comments: {positive_count}")
        print(f"  Negative Comments: {negative_count}\n")

# Print overall statistics
print("Overall Statistics (excluding Neutral Comments):")
print(f"Total Comments: {total_comments}")
print(f"Positive Comments: {positive_comments} ({total_positive_percentage:.2f}%)")
print(f"Negative Comments: {negative_comments} ({total_negative_percentage:.2f}%)\n")

# Plot grouped bar chart for video statistics
fig, ax = plt.subplots(figsize=(12, 8))
bar_width = 0.35
index = range(len(video_labels))

bar1 = ax.bar(index, video_positive_counts, bar_width, label='Positive', color='#66c2a5')
bar2 = ax.bar([i + bar_width for i in index], video_negative_counts, bar_width, label='Negative', color='#fc8d62')

ax.set_xlabel('Video IDs')
ax.set_ylabel('Number of Comments')
ax.set_title('Number of Positive and Negative Comments per Video')
ax.set_xticks([i + bar_width / 2 for i in index])
ax.set_xticklabels(video_labels, rotation=45, ha='right')
ax.legend()

plt.tight_layout()
plt.show()

# Plot pie chart for overall statistics (excluding Neutral Comments)
labels = ['Positive', 'Negative']
sizes = [positive_comments, negative_comments]
colors = ['#66c2a5', '#fc8d62']
explode = (0.1, 0)  # explode 1st slice (Positive)

plt.figure(figsize=(8, 6))
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
plt.title('Overall Sentiment Distribution of Comments (excluding Neutral)')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()
