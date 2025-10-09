## 🧾 Project Overview

As part of a real business project in the **media and journalism industry**, I developed an **interactive NPS (Net Promoter Score) dashboard in Power BI** that integrates both **quantitative metrics** and **qualitative customer feedback**.

The goal was to analyze reader feedback on digital news content and platform experience - a critical factor in understanding **audience satisfaction and trust** within the publishing sector.

Since the underlying data was spread across multiple Excel files, I built a **Python-based preprocessing pipeline** to:
- Automatically read and merge all Excel datasets  
- Clean and standardize free-text comments  
- Use **OpenAI’s GPT-4 model** to classify open responses into thematic categories  
  (e.g., *Cost*, *App performance*, *Journalistic quality*, etc.)  

The dataset consisted of **German-language customer feedback**, making this a multilingual NLP use case.  
GPT-4 successfully handled the zero-shot classification task without translation, demonstrating strong **multilingual generalization capabilities** even in non-English contexts.

This automated text classification enabled direct filtering of qualitative feedback by topic within the **Power BI dashboard**, linking it to quantitative KPIs such as NPS scores.  
As a result, the dashboard provides actionable insights into **reader satisfaction, content perception, recurring issues, and key improvement areas** - without the need for manual comment coding.

---

### 📊 Key Performance Indicators (KPIs)

The Power BI dashboard includes several key metrics to monitor customer sentiment and operational performance:

- **Net Promoter Score (NPS)** – overall customer loyalty and satisfaction  
- **Response Rate** – share of users providing feedback  
- **Topic Frequency** – most mentioned categories from comment classification  
- **Sentiment Trends** – evolution of promoter, passive, and detractor shares  
- **Category-based NPS** – breakdown of NPS by main feedback themes  
- **Temporal Insights** – Time-based performance comparison  

These KPIs allow management to quickly identify areas for improvement and track the impact of implemented changes.

---

### 🧠 Why Zero-Shot Classification instead of Sentiment Analysis?

The project initially included a **sentiment analysis** step to identify whether user comments were positive, neutral, or negative.  
However, since the **NPS score (0–10)** already reflects the respondent’s satisfaction level, an additional sentiment layer would have been redundant.

Instead, the focus was shifted to a **zero-shot topic classification** approach using GPT-4.  
This method complements the NPS data by revealing **what users are talking about** rather than **how they feel** - uncovering the main drivers behind positive or negative feedback (e.g., price, app usability, journalistic quality, etc.).  
Additionally, the zero-shot approach allowed each comment to be **assigned to multiple relevant categories** simultaneously, reflecting the multidimensional nature of real customer feedback.For example, a single comment could relate both to *Cost* and *App Usability*, which would be lost in single-label classification methods.

---

### 🧩 Tech Stack

- **Python** → Data preprocessing, merging, GPT-4 text classification  
- **Power BI** → Data modeling, visualization, KPI tracking  
- **Excel / CSV data sources**  
- **Zero-shot text classification with GPT-4**

---

### 💡 Outcome

A fully functional **NPS insights dashboard** that combines:
- Structured NPS and score data, and  
- Automatically categorized qualitative feedback  

to enable **data-driven decision-making in customer experience management**.

---

### 📸 Dashboard Preview

Here’s a preview of the **NPS dashboard** in Power BI:

![Dashboard Screenshot](https://github.com/vivusia/nps-dashboard/blob/main/nps%20dashboard%20screenshot%20blurred.png)
![Dashboard Screenshot](https://github.com/vivusia/nps-dashboard/blob/main/nps%20dashboard%20screenshot%202%20blurred.png)

> *Note: The screenshots are intentionally blurred to protect confidential business data and comply with data privacy requirements.*

The image above shows how the classified comment data, NPS, and other KPIs integrate visually in the dashboard.
