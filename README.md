# genai

GenerativeAI Course

### Recordings


1. GenAI 2024 Training - session 10_52-20240915_190043-Meeting Recording.mp4
   * Link: [GenAI 2024 Training - session 12_52-20240922_190159-Meeting Recording.mp4](https://rathinamtrainers365.sharepoint.com/:v:/r/sites/GenAI/Shared%20Documents/010-Recordings/GenAI%202024%20Training%20-%20session%2012_52-20240922_190159-Meeting%20Recording.mp4?csf=1&web=1&e=CezlZk)
	* Topics Discussed
	- Building Text embeddings from documents

2. GenAI 2024 Training - session 11_52-20240921_190148-Meeting Recording.mp4
	* Link: [GenAI 2024 Training - session 12_52-20240922_190159-Meeting Recording.mp4](https://rathinamtrainers365.sharepoint.com/:v:/r/sites/GenAI/Shared%20Documents/010-Recordings/GenAI%202024%20Training%20-%20session%2012_52-20240922_190159-Meeting%20Recording.mp4?csf=1&web=1&e=CezlZk)
	* Topics Discussed
	- Information on CONTEXT-CACHING
	- PDF RAG - Build RAG on image on Each page
	- Save Embeddings to CSV
	- Load Embeddings from CSV
	- Prompt question




Setup involved below activities
![Setup](./Docs/gcp-setup.png)

1. GCP account setup
2. GCP CLI setup
3. Enable VERTEX APIs
4. Create VM with ML model on cloud
5. Query VM from GCP CLI
6. Query from SDK
7. Query from Python Script
8. Query from Postman
9. Query from CURL
10. Selection of different ML model
11. Working with AI Studio

* Curl Hello world
  `curl \ -H 'Content-Type: application/json' \ -d '{"contents":[{"parts":[{"text":"Explain how AI works"}]}]}' \ -X POST 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=YOUR_API_KEY'`
* 

## Other pointers

magika gitpython
