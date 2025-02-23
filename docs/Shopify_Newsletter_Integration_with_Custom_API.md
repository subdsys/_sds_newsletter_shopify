# Shopify Newsletter Integration with Custom API

This document provides step-by-step instructions on how to integrate your Shopify store's newsletter signup with your custom API running on Google Cloud Run.

## **Step 1: Create a New JavaScript File**

1. **Go to Shopify Admin** → **Online Store** → **Themes** → **Edit Code**.
2. Navigate to **`Assets`**.
3. Click **"Add a new asset"**.
4. Select **"Create a blank file"**.
5. Name the file: `newsletter-form.js`.
6. **Paste the following JavaScript code** inside `newsletter-form.js`:

```js
 document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("newsletterForm");
    const emailInput = document.getElementById("email");
    const responseMessage = document.getElementById("responseMessage");

    if (!form) return; // Prevent errors if form doesn't exist

    form.addEventListener("submit", async function(event) {
        event.preventDefault(); // Stop redirecting

        const email = emailInput.value.trim();
        responseMessage.style.display = "none";

        if (!email) {
            responseMessage.style.color = "red";
            responseMessage.textContent = "❌ Please enter a valid email.";
            responseMessage.style.display = "block";
            return;
        }

        try {
            const response = await fetch("https://newsletter-app-487991307165.us-central1.run.app/subscribe", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: `email=${encodeURIComponent(email)}`
            });

            const result = await response.json();
            
            if (response.ok) {
                responseMessage.style.color = "green";
                responseMessage.textContent = result.message || "✅ Subscription successful!";
                form.reset(); // Clear input after success
            } else {
                responseMessage.style.color = "red";
                responseMessage.textContent = result.error || "❌ Subscription failed.";
            }

        } catch (error) {
            responseMessage.style.color = "red";
            responseMessage.textContent = "⚠️ An error occurred. Please try again.";
        }

        responseMessage.style.display = "block";
    });
});
```

## **Step 2: Add JavaScript to Shopify Theme**

1. **Open `theme.liquid`** (found in **Layout** section).
2. Scroll to the **head** section before the closing `</head>` tag.
3. **Add the following line to load the JavaScript file:**

```liquid
<script src="{{ 'newsletter-form.js' | asset_url }}" defer></script>
```

4. Click **Save**.

## **Step 3: Modify the Shopify Newsletter Form**

Replace the default Mailchimp form with the following code in your theme (usually in **Footer** or **Popup Newsletter Section**):

```liquid
<form id="newsletterForm">
    <input type="email" name="email" id="email" placeholder="Enter your email" required>
    <button type="submit">Subscribe</button>
</form>

<p id="responseMessage" style="display:none; margin-top: 10px; font-weight: bold;"></p>
```

## **Step 4: Save and Test**

1. **Go to your Shopify store** and enter a test email.
2. **Ensure the page does NOT reload** after submitting.
3. **Confirm the success message appears below the form**.
4. **Check the database to confirm the entry:**
   ```sql
   SELECT * FROM subscriber;
   ```
5. **Monitor Cloud Run logs for any errors:**
   ```bash
   gcloud run logs read newsletter-app --region=us-central1
   ```

## **Summary of Changes**

| Change                       | Description                                         |
| ---------------------------- | --------------------------------------------------- |
| Created `newsletter-form.js` | Handles AJAX form submission to prevent page reload |
| Added JS to `theme.liquid`   | Loads the custom JavaScript for the newsletter form |
| Modified Newsletter Form     | Updated the form to use the new API                 |

🚀 **Your Shopify store is now successfully integrated with your custom newsletter API!**

