# Groq Cloud Storage Autosummarizer

This project is designed to automatically append a summary to any document uploaded to a Google Cloud Storage (GCS) bucket, using the Groq API for summarization and Google Cloud Platform services such as Pub/Sub and Cloud Storage.

## Overview
- Google Cloud Storage: Stores documents that are uploaded.
- Google Cloud Pub/Sub: Sends notifications when a new file is uploaded to the bucket.
- Groq API: Processes the content of the document to generate a concise summary using the LLaMA model.
- Google Cloud Functions: Responds to Pub/Sub messages, downloads the document, and then appends a summary to the document.

## Workflow
1. Upload Document: A user uploads a document to the designated Google Cloud Storage bucket.
2. Pub/Sub Notification: Once the document is uploaded, a Pub/Sub message is triggered, notifying the subscriber (the Python script) about the new file.
3. Download Document: The script retrieves the document from the GCS bucket.
4. Summarize: The document content is passed to the Groq API, which processes the text and returns a summary.
5. Output: The summary is appended back to the document. It can also be stored separately.

## Setup Instructions

### Groq Setup:

1. Sign up for the Groq API and generate an API key.
2. Store the API key securely in a Python file or as an environment variable.
3. Python Dependencies: Install the required Python libraries as specified in `requirements.txt`

### Google Cloud Setup:
1. Create a Google Cloud project and enable Cloud Storage and Pub/Sub.
2. Set up a Pub/Sub topic and subscription.
3. Create a Cloud Storage bucket for file uploads.
4. Ensure that you have a service account with the necessary permissions and download the service account key as a .json file.
5. Set the environment variable to point to your GCP service account credentials.

## Outcomes
The application successfully demonstrates how to integrate high-performance AI models (via Groq) with cloud infrastructure to create a robust document summarization pipeline.
The system can scale across multiple documents and handle real-time uploads, making it a valuable tool for processing and summarizing large text-based datasets.

## Future Improvements
### Handling Large Documents:

Initially, the system struggled with very large documents due to the limitations in handling large text data with Pub/Sub and the Groq API. This requires optimizing the code to manage file size and encoding properly.

### Advanced NLP
Further features could include entity extraction, keyword generation, or multi-document summarization for more complex datasets.
### Cloud Function Deployment
This entire process can be moved to Google Cloud Functions for serverless execution, reducing the need for a long-running script.

## Conclusion
This project highlights the powerful combination of Google Cloud Platform's scalability and the speed of the Groq API for machine learning tasks like text summarization. With further improvements, this architecture can be expanded into a production-level system capable of handling large volumes of data with minimal latency.