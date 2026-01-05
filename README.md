# Automatic Space Weather Data Retrieval, Processing and Visualization System
As it turns out it's going to be my **bachelor's thesis** ;)

### Example Chart
![demo_chart](documents/demo/demo_chart.gif)

### Switching Space Weather Parameters
![demo_chart](documents/demo/demo_switching.gif)

## Description
This repo contains code and thesis text for my bachelor's thesis(as the name indicates ;D). It's a system for a fully automatic retrieval, processing and vizualization of selected
parameters of space weather. As mentioned the flow is fully automated using GH Actions and code written in both Python and Go, which also happened to be contenerized for convenience ;D

## Possible future steps
- extending vizualization
- migrating vizualization module to another(faster) framework
- adding simple ML module 
- increasing data retrieval frequency

## Websites 

- [Dashboard](https://inzynierka-sskrzypczyk.streamlit.app/)
- [Thesis Online](https://szymonskrzypczyk.github.io/inzynierka/)

## Project structure
> - 📂 [`.github/workflows/`](.github/workflows/) - workflows working with GitHub Actions
> - 📂 [`dashboard/`](dashboard/) - all resources related to space weather visualization
> - 📂 [`db/`](db/) - all resources related to data saving to a database
> - 📂 [`docs/`](docs/) - static site resources for thesis hosting
> - 📂 [`documents/`](documents/) - all markdown documents, sketches, etc.
> - 📂 [`retrieval/`](retrieval/) - all resources related to data retrieval
> - 📄 [`requirements.txt`](requirements.txt) - root directory python requirements for **Streamlit**
> - 📄 [`detailed_guide.md`](detailed_guide.md) - project setup guide
> - 📄 [`mkdocs.yaml`](mkdocs.yaml) - page structure for online thesis

## [Setup guide](detailed_guide.md)