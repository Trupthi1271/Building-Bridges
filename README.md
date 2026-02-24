# Building Bridges

An interactive Python application that solves the classic ACM-ICPC "Building Bridges" problem using graph theory and minimum spanning tree algorithms.

## Overview

The City Council of New Altonville plans to build a bridge system connecting all downtown buildings. This application determines the optimal bridge configuration that minimizes both the number of bridges and their total length.

## Problem Statement

Given a grid of buildings, find the minimum number of bridges needed to connect all buildings. If complete connectivity is impossible, minimize the number of disconnected groups while keeping the total bridge length minimal.

**Rules:**
- Buildings are represented by connected `#` symbols on a grid
- Bridges must be straight lines (horizontal or vertical) along grid edges
- Each bridge connects exactly two buildings
- Bridges can cross each other on different levels

## Features

- **Interactive GUI** - Built with Tkinter for easy input and visualization
- **Real-time Calculation** - Instant bridge computation using Kruskal's MST algorithm
- **Visual Representation** - Grid-based display of buildings and bridge connections
- **Pre-built Examples** - 4 sample city configurations included
- **Audio Feedback** - Background music and sound effects

## Installation

### Prerequisites

- Python 3.x
- pip package manager

### Required Dependencies

```bash
pip install pillow pygame
```

Note: `tkinter` is included with most Python installations.

## Usage

### Running the Application

```bash
python first_window.py
```

### Input Format

Enter grid dimensions followed by the grid layout:

```
rows columns
grid_row_1
grid_row_2
...
```

**Example:**
```
3 5
#...#
..#..
#...#
```

Where:
- `#` represents a building square
- `.` represents an empty square

### Sample Cities

**City 1** - Multiple buildings requiring bridges
```
3 5
#...#
..#..
#...#
```
Output: `4 bridges of total length 4`

**City 2** - No possible connections
```
3 5
##...
.....
....#
```
Output: `No bridges are possible.`

**City 3** - Single connected building
```
3 5
#.###
#.#.#
###.#
```
Output: `No bridges are needed.`

**City 4** - Partial connectivity
```
3 5
#.#..
.....
....#
```
Output: `1 bridge of total length 1`

## Algorithm

The application implements **Kruskal's Minimum Spanning Tree (MST)** algorithm with Union-Find data structure:

1. **Building Detection** - Group adjacent `#` cells into buildings
2. **Bridge Discovery** - Identify all valid bridge connections
3. **Sorting** - Order bridges by length (shortest first)
4. **Greedy Selection** - Connect buildings without creating cycles
5. **Result Analysis** - Calculate disconnected groups if any

**Time Complexity:** O(E log E) where E is the number of possible bridges  
**Space Complexity:** O(V + E) where V is the number of buildings

## Project Structure

```
Building-Bridges/
├── first_window.py          # Application entry point
├── main.py                  # Core logic and GUI
├── CITY1.py - CITY4.py      # City visualizations
├── *.png                    # Image assets
├── *.mp3                    # Audio files
└── README.md                # Documentation
```

## Output Types

- `No bridges are needed` - Single building or all connected
- `No bridges are possible` - Buildings cannot be connected
- `N bridge(s) of total length L` - Optimal solution found
- `X disconnected groups` - Remaining unconnected groups

## Credits

**Problem Source:** ACM-ICPC World Finals (1991-2006)  
**Original Problem:** "Building Bridges" - Baylor University

## License

This project is for educational purposes demonstrating graph algorithms and GUI development.
