# Mood of the Queue App

> Simple, straightforward app to log tickets' moods and show them in a bar chart

---

## Features

- Log team mood with emoji and optional notes
- Visualize mood distribution over a date range
- Stores data in Google Sheets for easy sharing and backup
- Latest note for each mood shown as tooltip in chart

## Project layout

```
mood-of-queue/
├── .gitignore
├── README.md
├── requirements.txt
├── storage.py # Google Sheets wrapper
└── app.py # Streamlit app
```

## How it works

- **Logging:** Select a mood emoji and optionally add a note. Click "Submit" to log.
- **Visualization:** View a bar chart of mood counts for a selected date range. Hover to see the latest note for each mood.

## Google Sheets Setup

- For now, the app uses this public google sheet: https://docs.google.com/spreadsheets/d/1ofGH4pAq6IMjRmUp-3BQxZ2F8WzmJoo3LN__TWyfDto/edit?usp=sharing -> I've enabled it with editor permissions, in case you want to test manual changes in the file itself.
- Create a Google Sheet with columns: `timestamp`, `mood`, `note`.
- Share it with your service account email (from your Google Cloud credentials).

## Further Notes

- This project was rather nice!
- I found myself split, 20% coding - 80% setting up the repo and convincing Streamlit to behave.
- In my helper file storage.py -> got a quick Copilot fix to declare a function to support a tooltip msg.
- Emojis are actually numeric values below the hood -> I am assuming this can be a placeholder for a more stable solution (perhaps a text-mining classifier that reads tickets, infer mood value, and sends back to this logger?)

---

## Setup

1. **Clone the repository**

    ```sh
    git clone <your-repo-url>
    cd mood-of-queue
    ```

2. **Install dependencies**

    ```sh
    pip install -r requirements.txt
    ```

3. **Set up environment variables**

    Create a `.env` file in the project root with the following variables:

    ```
    SERVICE_ACCOUNT_JSON='<your Google service account JSON as a single line>'
    GOOGLE_SHEET_ID='<your Google Sheet ID>'
    GOOGLE_SHEET_NAME='<your Sheet name>'
    ```

    > See the provided `.env` example for formatting.

4. **Run the app**

    ```sh
    streamlit run app.py
    ```

    The app will open in your browser.