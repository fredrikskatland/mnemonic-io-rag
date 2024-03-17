# mnemonic-io-rag
Chat with the contents of mnemonic.io

## Contains 
* quick analysis of mnemonic.io, 
* webscraper, 
* quick semantic analysis of content, 
* LangChain Retrieval-Agent deployed with LangServe with Docker on heroku

Try the app here: 
Retrival agent (Agent does the work. More thourogh, but slower):
* https://mnemonic-retrieval-agent-6c56586efc83.herokuapp.com/retrieval-agent/playground/

Self query chain (Chain with meetadata filers in query. Faster, but needs good and precise prompts):
* https://mnemonic-retrieval-agent-6c56586efc83.herokuapp.com/self-query-qdrant/playground/

Docs:
https://mnemonic-retrieval-agent-6c56586efc83.herokuapp.com/self-query-qdrant/playground/

Takes 20-30 seconds to start if it is sleeping. The sitemap is checked every hour (at 41 minutes) and any changes will trigger a scrape and indexing of the new content.

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
- [x] Scraper pipeline to Qdrant
- [ ] Move scraper to AWS Lambda (skipped, going for EC2)
- [ ] Schedule/trigger scraper with AWS EventBridge (skipped, going for cronjob)
- [x] Only scrape when sitemap has changed
- [x] Move scraper to EC2
- [x] Schedule/trigger scraper with cronjob (at 41 minutes, every hour)
- [x] Self query chain
- [ ] Query analysis chain
- [ ] RAG Strategy evaluation
