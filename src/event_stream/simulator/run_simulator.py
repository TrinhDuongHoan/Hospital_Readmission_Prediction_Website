from __future__ import annotations

import time
import pandas as pd

from src.event_stream.simulator.event_builder import build_events_from_row
from src.event_stream.simulator.producer import create_producer, send_event


DATA_PATH = "data/raw/diabetic_data.csv"
TOPIC_NAME = "hospital-events"


def main():
    df = pd.read_csv(DATA_PATH, na_values=["?", "None", "NULL", "null", "NA", "N/A", ""], low_memory=False)

    producer = create_producer("localhost:9092")

    sample_df = df.sample(5, random_state=42)

    for _, row in sample_df.iterrows():
        events = build_events_from_row(row)

        for event in events:
            send_event(
                producer=producer,
                topic=TOPIC_NAME,
                key=str(event["encounter_id"]),
                event=event,
            )
            print(f"Sent event: {event['event_type']} | encounter_id={event['encounter_id']}")
            time.sleep(1)

    print("Simulation completed.")


if __name__ == "__main__":
    main()