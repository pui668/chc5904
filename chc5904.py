import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt
import io

# --- Page Title ---
st.title("📖 Character Interaction Network Analysis")

# --- Introduction ---
st.markdown("""
## 📊 Introduction
In this project, we analyze the relationships between characters in a classic Chinese text using **network analysis** techniques. 
The goal is to uncover the **central characters**, their **communities**, and the **strength of their interactions**.

This report walks through:
1. **The Raw Data**: Displaying the raw character interactions.
2. **Network Graph**: Visualizing character relationships as a social network.
3. **Centrality Metrics**: Identifying the most influential characters.
4. **The Code**: Explaining how the analysis was done.
5. **Comparison with Gephi**: Why the Gephi results are visually superior.
""")

# --- Embedded CSV Data ---
st.markdown("### Step 1: Raw Data")
st.markdown("This dataset contains character interactions, showing who interacts with whom and how frequently.")
csv_data = """
Source,Target,Weight
賈珍,賈蓉,7
賾敬,賾珍,1
賾敬,賾蓉,1
王夫人,賾寶玉,3
賾母,賾珍,2
王夫人,賾母,9
王夫人,賾蓉,1
王夫人,王熙鳳,11
秦可卿,賾寶玉,1
王夫人,賾珍,2
賾寶玉,賾珍,3
秦可卿,賾母,1
王夫人,秦可卿,1
王熙鳳,賾母,4
平兒,王熙鳳,2
賾政,賾赦,5
賾珍,賾赦,7
賾政,賾珍,5
林黛玉,賾母,1
林黛玉,賾璉,2
秦可卿,賾璉,1
王熙鳳,秦可卿,1
襲人,賾母,3
王熙鳳,賾珍,3
王熙鳳,賾寶玉,8
林黛玉,王熙鳳,1
王熙鳳,賾璉,3
王夫人,迎春,2
寶珠,賾珍,1
賾寶玉,賾母,5
薛寶釵,迎春,3
王夫人,薛寶釵,2
王熙鳳,薛寶釵,1
王熙鳳,迎春,1
賾母,賾蓉,1
賾蓉,賾赦,1
賾母,賾赦,3
林黛玉,迎春,2
林黛玉,賾寶玉,9
薛寶釵,賾寶玉,2
林黛玉,薛寶釵,4
賾寶玉,迎春,2
平兒,香菱,2
王熙鳳,香菱,1
賾珍,賾璉,6
平兒,賾璉,1
王熙鳳,賾蓉,2
賾璉,賾赦,3
賾政,賾璉,2
賾寶玉,賾政,3
賾政,賾母,3
林黛玉,王夫人,1
賾探春,迎春,2
賾敬,賾赦,1
賾政,賾敬,1
賾珍,賳環,1
賳璉,賳環,1
賳環,賳蓉,1
賳璉,賳蓉,1
襲人,賳寶玉,4
秋紋,賳母,1
史大姑娘,賳母,1
秋紋,鴛鴦,1
薛寶釵,香菱,1
賳惜春,迎春,1
林黛玉,賳探春,1
賳惜春,賳探春,1
薛寶釵,賳惜春,1
薛寶釵,賳探春,1
林黛玉,賳惜春,1
賳母,賳環,1
薛寶釵,賳環,1
王夫人,賳環,1
王熙鳳,賳環,1
豐兒,迎春,1
史大姑娘,薛寶釵,1
秦可卿,賳蓉,2
"""

# --- Step 1: Load Data into a DataFrame ---
df = pd.read_csv(io.StringIO(csv_data))

# Display the raw data table
st.dataframe(df)

# --- Step 2: Build the Network ---
st.markdown("### Step 2: Network Visualization")
st.markdown("This interactive network graph shows the relationships between characters. The thickness of edges represents the frequency of interactions.")

# Create a NetworkX graph from the DataFrame
G = nx.Graph()
for index, row in df.iterrows():
    G.add_edge(row['Source'], row['Target'], weight=row['Weight'])

# Visualize the network using PyVis
net = Network(height="600px", width="100%", notebook=True)
net.from_nx(G)
net.show("network.html")

# Display the interactive PyVis network graph
st.write("Interactive Character Network:")
HtmlFile = open("network.html", 'r', encoding='utf-8')
source_code = HtmlFile.read()
st.components.v1.html(source_code, height=600)

# --- Step 3: Display Centrality Metrics ---
st.markdown("### Step 3: Centrality Metrics")
st.markdown("Here we calculate centrality metrics to identify key characters in the network.")

# Degree Centrality
degree_centrality = nx.degree_centrality(G)
st.subheader("Top 5 Characters by Degree Centrality")
top_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
st.write(pd.DataFrame(top_degree, columns=["Character", "Degree Centrality"]))

# Betweenness Centrality
betweenness_centrality = nx.betweenness_centrality(G)
st.subheader("Top 5 Characters by Betweenness Centrality")
top_betweenness = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
st.write(pd.DataFrame(top_betweenness, columns=["Character", "Betweenness Centrality"]))

# --- Step 4: Display Gephi Results ---
st.markdown("### Step 4: Gephi Visualization")
st.markdown("""
While the interactive PyVis graph is useful for exploring the network, the **Gephi** results provide a more refined visual representation.

- **Gephi** offers more flexibility in terms of layout, color schemes, and community detection.
- The **modularity** and **color coding** in Gephi highlight the social clusters clearly.
- The thickness and opacity of edges in Gephi make the frequencies of interactions more visually distinct.

Here is the final result generated from **Gephi**:
""")

# Display Gephi-generated image
st.image("Final.png", caption="Gephi Visualization of Character Interactions")

# --- Step 5: Code Walkthrough ---
st.markdown("### Step 5: Code Walkthrough")
st.markdown("In this section, we explain the code used to process the text and generate the network.")
st.markdown("""
1. **Text Processing**: We used **jieba** for tokenizing the text and identifying character names.
2. **Interaction Recording**: We recorded interactions between characters whenever they appeared in the same sentence.
3. **Network Construction**: We built a **NetworkX** graph to represent the relationships, using **PyVis** to create an interactive visualization.
4. **Centrality Calculations**: We used **NetworkX** to calculate metrics like **degree centrality** and **betweenness centrality** to identify key characters.
""")

# Display the full code for processing the text and generating the CSV
code = '''
import jieba
import re
from collections import Counter
import csv

base_directory = r'C:\\Users\\puipu\\Documents\\MScGAH\\CHC5904\\Second Hands on Assignment'

with open(f'{base_directory}\\chapters_10_20.txt', 'r', encoding='utf-8') as file:
    text = file.read()

character_variations = {
    '賈寶玉': ['賈寶玉', '寶玉', '玉兄', '賈公子', '賈二爺'],
    '林黛玉': ['林黛玉', '黛玉', '林妹妹', '林姑娘', '黛'],
    '薛寶釵': ['薛寶釵', '寶釵', '薛小姐', '薛姑娘', '釵姐', '薛姨媽'],
    '襲人': ['襲人', '花襲人', '襲姑娘'],
    '鴛鴦': ['鴛鴦', '鴛鴦姐'],
    '賈母': ['賈母', '老祖宗', '賈老太君', '賈老祖', '老太太', '太君'],
    '賈政': ['賈政', '政老爺', '賈二老爺'],
    '王熙鳳': ['王熙鳳', '鳳姐', '鳳丫頭', '熙鳳'],
    '賈璉': ['賈璉', '璉二爺', '璉哥', '賾璉二爺'],
    # Add more characters and their variations here...
}

def find_characters_in_window(window):
    present_characters = set()
    for main_character, variations in character_variations.items():
        if any(variation in window for variation in variations):
            present_characters.add(main_character)
    return present_characters

sentences = re.split(r'[。！？]', text)

interactions = []

for sentence in sentences:
    tokens = jieba.lcut(sentence)  
    present_characters = find_characters_in_window(tokens) 
    
    if len(present_characters) > 1: 
        sorted_pairs = set()
        for character1 in present_characters:
            for character2 in present_characters:
                if character1 != character2: 
                    sorted_pair = tuple(sorted([character1, character2]))
                    sorted_pairs.add(sorted_pair)
        interactions.extend(sorted_pairs)

interaction_counts = Counter(interactions)

with open(f'{base_directory}\\character_interactions_with_nicknames.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Source', 'Target', 'Weight'])
    for (source, target), weight in interaction_counts.items():
        csvwriter.writerow([source, target, weight])

print("Character interactions saved to 'character_interactions_with_nicknames.csv'.")
'''

st.code(code, language="python")

st.markdown("This is the full Python code used for processing the text and generating the graph.")
