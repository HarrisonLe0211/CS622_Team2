# CS622_Team2

# Welcome to Team 2's Team Project

“Experimental Room Allocation System for Hotels/Resorts” by Cipriano Garza, Rothpanhaseth Im, Tshering Sherpa, and Harrison Le, presents a project aimed at optimizing hotel room allocation using advanced data structures, primarily focusing on Treaps.

# Summary

The team proposes a system that improves hotel management by employing a Treap, a combination of binary search trees and heaps. The current hotel room management systems are often inefficient, with many hotels still using outdated methods. The solution is designed to enhance both customer satisfaction and revenue through more efficient room allocation. The presentation covers the current state of the industry, explains how Treaps and alternative data structures like Red-Black Trees and Skip Lists work, and provides a performance comparison of these structures.

# Description

    -   Current State of Hotel Management: Many hotels use outdated manual methods or limited software solutions. Efficient room allocation is vital for  operational efficiency, but adoption of advanced systems remains low.
	-   Solution - Treap: The team introduces Treap, a data structure that balances tree properties and heap properties to ensure efficient insertion, search, and deletion operations. It helps handle dynamic room allocations better than traditional methods.
	-   Alternative Structures: They also explore Red-Black Trees and Skip Lists, comparing their strengths and weaknesses to Treaps in terms of balancing complexity and performance.
	-   Performance Analysis: Metrics such as insert, search, and delete operation times are discussed, showing Treap’s effectiveness in optimizing room allocation.
	-   Conclusion: Treaps offer a balanced and efficient solution for hotels, though they might require custom implementation due to limited support in standard libraries.

# Install Python Pandas Library to read Excel File
```bash
pip install pandas
```

# Install Streamlit
```bash
pip install streamlit
```

# Install Graphviz
```bash
pip install graphviz
```

# Host Local Streamlit
```bash
cd BRAS
streamlit run streamlit_app.py
```

# Conduct Analysis of Treap 
```bash
cd BRAS
python treap_performance.py
or
python3 treap_performance.py
```

# Compare 3 Data Structure Performance of Insert, Delete, Search Operations
```bash
cd BRAS
python compare_performance.py
or
python3 compare_performance.py
```