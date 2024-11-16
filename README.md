# Optimal-Path-Finding

LINK TO THE APP: [CLICK HERE](https://optimalpathfinding-qv2bdgqrrnw7huhbhhvz5g.streamlit.app/)

**Problem Statement**

This is a problem related to the shortest path problem (NP-Hard). Here the goal is to find the shortest path of a knight for two given points where one is the starting and the other one is the ending point respectively. Nothing is mentioned about the chessboard dimensions so it's freely chosen while implementing the problem and given a list of choices to select from those. 

**Solution**

The given problem can be tackled in many different ways. BFS, Bidirectional BFS, and DFS are some of the algorithms which can be utilized to solve this problem. Here I have used BFS and Bi-direction BFS as these are the most appropriate ones to solve problems related to shorted path or path finding where each edge is of equal weight or unweighted.

**Workflow Diagram of BFS**
![bfs workflow](https://github.com/user-attachments/assets/3ea6ef7e-4b75-45af-a2ae-8161a953c7a4)

**Workflow Diagram of Bidirectional BFS**
![bi-bfs](https://github.com/user-attachments/assets/22480261-95a8-478f-98d7-223265c5423f)

**Performance Comparision**

I have not considered DFS as it is not suitable for shortest or unweighted graphs or paths and also it traverses through each path individually which increases the time and space complexity. Here I have considered BFS and Bidirectional BFS. Bidirectional BFS reduces the computation time as well as halves the time and also reduces the space complexity as it start searching from both directions (start and end). The below plot shows the comparison between the time taken to compute the solution by both algorithms. 

![image](https://github.com/user-attachments/assets/5793ca86-fa1b-4626-a3eb-bad7f0024e01)


**Saving the Dot File**

The following code can be used to save the generated file in a dot file using  the Graphviz library which can be further visualised. 
```c
def generate_dot_file(paths, filename):
    """Generate a Graphviz DOT file from the paths."""
    with open(filename, 'w') as f:
        f.write("digraph knight_paths {\n")
        f.write("    node [shape=circle];\n")
        
        for path in paths:
            for i in range(len(path) - 1):
                # generating and saving the node pair in (0_0) format to visualize this using Google Colab
                node_from = f'"{path[i][0]}_{path[i][1]}"'  # e.g., (0, 0) becomes "0_0"
                node_to = f'"{path[i + 1][0]}_{path[i + 1][1]}"'  # e.g., (2, 1) becomes "2_1"
                f.write(f'    {node_from} -> {node_to};\n')
        
        f.write("}\n")
```

***Visualizing the Dot File***

In general, when we install GraphViz in our local machine due to some environmental issue we can't visualize this in our local machine. So, the easiest way to visualize this file is using the Google Colab. Just by using the below 3 lines of code the generated dot file can be visualized on google colab. 

```c
# Install Graphviz in the Colab environment
!apt-get install graphviz

# Generate the image from the DOT file
!dot -Tpng /content/knight_paths.dot -o /content/image.png
```

