# mnemonic-io-rag
Chat with the contents of mnemonic.io

## Contains 
* quick analysis of mnemonic.io, 
* webscraper, 
* quick semantic analysis of content, 
* LangChain Retrieval-Agent deployed with LangServe with Docker on heroku

Try the app here: https://mnemonic-retrieval-agent-6c56586efc83.herokuapp.com/retrieval-agent/playground/

API docs: https://mnemonic-retrieval-agent-6c56586efc83.herokuapp.com/docs

Takes 20-30 seconds to start if it is sleeping. The content is currently static, and not regularly updated. Last scraped on feb. 16 2024.

## TODOs

- [x] Initial sitemap analysis
- [x] Scrape contents
- [x] Index in vectorstore
- [x] Semantic analysis content 
- [ ] Optimize retrieval strategy
- [x] Prompts
- [x] UI (LangServe playground)
- [x] Deployment
- [ ] Improve readme
- [ ] Deeper exploratory analysis
- [ ] Example prompts/question
- [x] LangSmith setup and logging
- [ ] Scraper pipeline to Qdrant
- [ ] Move scraper to AWS Lambda
- [ ] Schedule/trigger scraper with AWS EventBridge 
