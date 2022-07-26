## MARK-TO-MARKET ON TESOURO DIRETO (0. README)

---

### 0.0 tl;dr

A web application built on Python to create visualizations and help analyze possible gains with mark-to-market operations on bonds issued and sold by the Brazilian government.
[Click here to access the web app.](https://simulacao-marcacao-a-mercado.herokuapp.com/)

---

### 0.1 PROJECT PURPOSE AND CONCEPTION

At the time this readme is being written in its first version, the world is still mid-way on its recovery from the Covid-19 pandemic and inflation is just a natural consequence of the measures governments all around the world took to kick-start their recover from the economic challenges that were born altogether with isolation measures.

Brazil, like many other countries, had to bring its interest rates up as in attempt to slow down its most-feared inflation, however it would be more proper to say Brazilian consumers took a major hit when inflation rose from about 3.5% (July 2019) to about 12% three years later. The interest rate on the same period first went down from 6.5% to its lowest 2% in late 2020, then shot up to 13.25% in July 2022.

With more raises on interest rates yet to come and likely more inflation as well, Brazilian people have been presented with a few scarce opportunities, one of them being the subject of this project: gains with mark-to-market operations on bonds sold by the Brazilian government. Finally, since the treasury's official website outputs less information than maybe one would want, the main goal here is to build a web application with visualizations and more data to allow some in-depth analysis.

---

### 0.2 DATA AND TOOLS USED

The only data source used was the original information given by the official treasury website, which were further filtered to select only the ones more susceptible to vary and yield gains. As per the tools:

1. VS Code as a Python IDE;
2. Streamlit as a framework to create the web application;
3. Heroku to deploy the application itself; _and_
4. Git and github for version control.

---

### 0.3 SKILLS SHOWN

1. General Python coding;
2. Math on a high-school level - more specifically compound interest concepts;
3. Creation of application with working frameworks;
4. Data visualizations;
5. Basic concepts and commands of versionalization with git;
6. DataFrame manipulation (pandas); _and_
7. Heroku and Github integration.

---

### 0.4 PREMISES

1. Only bonds with fixed rates (LTN) and indexed to inflation without biannual payments (NTN-B Principal) were used, since these are the ones more susceptible to vary and yield gains on like operations;
2. No taxes (such as income tax) were taken into account; _and_
3. Fees were not considered. Most banks and brokers have zeroed those.

---

### 0.5 PIPELINE (PROJECT PHASES)

<img width="924" alt="image" src="https://user-images.githubusercontent.com/108877184/181509224-57dd0476-0811-4cc9-9ec7-a59815940c5d.png">

---

### 0.6 FURTHER DEVELOPMENT SUGGESTIONS

Ideas to build on top of this project and extend it.

1. Create scheduler to fetch data and update dataframe;
2. Evaluate mobile responsivity and adaptability;
3. Create another series of data with bonds emitted by banks (CDB) and let the user choose the percentage of "CDI" indexed by using another slider; _and_
4. Allow user to simulate operations with LFT bonds (indexed to "Selic") and also those which will yield biannual returns.
