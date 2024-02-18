# Web scraper for mnemonic.io

Looping through all the links in https://www.mnemonic.io/sitemap.xml, scraping content from urls containing www.mnemonic.io

```bash
scrapy crawl mnemonicspider -O output.json
```

Outputs json, example:

```json
{
    "title": "Security Report 2018", 
    "ingress": "In this year's report we share our predictions for 2018, and the trends we observed from our 24x7 Security Operations Center", 
    "content": "mnemonic releases our Security Report to share insight from our team of security experts and Security Operations Center. Topics from this year's report include:Security Report 2018 also includes the guest article:", 
    "url": "https://www.mnemonic.io/resources/security-report/security-report-2018/", 
    "category": "resources", 
    "subcategory": "security-report"
}
```

