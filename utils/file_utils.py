import csv
import os


def save_to_csv(data, file_name="jobs.csv", save_path="/Users/gundale/Documents/untitled folder"):
    """
    Saves job data to a CSV file.
    """
    if not data:
        print("⚠️ No data to save.")
        return

    # Ensure the directory exists
    os.makedirs(save_path, exist_ok=True)

    # Define full file path
    file_path = os.path.join(save_path, file_name)
    print(f"📝 Saving to: {file_path}")  # Debugging

    # Define correct fieldnames
    fieldnames = ["title", "company", "location", "link", "timestamp"]

    # 🔥 Reformat data keys before saving
    formatted_data = [
        {
            "title": job.get("Title", ""),
            "company": job.get("Company", ""),
            "location": job.get("Location", ""),
            "link": job.get("Link", ""),
            "timestamp": job.get("timestamp", ""),
        }
        for job in data
    ]

    try:
        file_exists = os.path.exists(file_path)

        with open(file_path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Write header only if file is new
            if not file_exists:
                writer.writeheader()

            writer.writerows(formatted_data)

        print(f"Successfully written {len(data)} job(s) to {file_path}")

    except Exception as e:
        print(f"Error writing CSV: {e}")
