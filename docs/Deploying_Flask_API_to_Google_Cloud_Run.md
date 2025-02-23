# Deploying Flask API to Google Cloud Run

This document provides step-by-step instructions on deploying your Flask API to Google Cloud Run.

## **Step 1: Ensure You Are Logged into Google Cloud**
Before deploying, ensure that you are logged in to Google Cloud. If this opens a browser, log in with your Google account:
```bash
gcloud auth login
```

## **Step 2: Set the Correct Google Cloud Project**
Confirm that you're using the correct Google Cloud project by running:
```bash
gcloud config set project subdomain-systems-llc
```

## **Step 3: Build and Push the Docker Image**
1. **Build the Docker image** using the following command:
   ```bash
   docker build -t gcr.io/subdomain-systems-llc/sds-newsletter-shopify .
   ```
2. **Push the Docker image** to Google Container Registry:
   ```bash
   docker push gcr.io/subdomain-systems-llc/sds-newsletter-shopify
   ```

## **Step 4: Deploy the Flask App to Cloud Run**
Deploy the application using the following command:
```bash
gcloud run deploy newsletter-app \
    --image gcr.io/subdomain-systems-llc/sds-newsletter-shopify \
    --platform managed \
    --region us-central1 \
    --add-cloudsql-instances=subdomain-systems-llc:us-central1:sds-prod-shopify \
    --allow-unauthenticated
```

## **Step 5: Verify Deployment**
After deployment, Cloud Run will provide a **Service URL** for your API. Test the deployment by running:
```bash
curl -X GET https://newsletter-app-487991307165.us-central1.run.app/
```
If the API is running correctly, you should see the expected response.

## **Step 6: Check Logs and Debugging**
If there are any issues, you can view the logs with:
```bash
gcloud run logs read newsletter-app --region=us-central1
```

## **Step 7: Confirm Database Connectivity**
To ensure your Cloud Run instance can connect to the Cloud SQL database, run:
```bash
gcloud sql instances describe sds-prod-shopify --format=json | jq .ipAddresses
```
This will display the IP addresses assigned to your database.

---
🚀 Your Flask API is now deployed and running on Google Cloud Run! If you need further optimizations, consider setting up **Cloud SQL Auth Proxy** for enhanced security. ✅

