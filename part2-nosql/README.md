# Part 2: NoSQL Database Analysis

## Overview

This part analyzes the suitability of MongoDB for FlexiMart's product catalog and implements basic MongoDB operations to demonstrate NoSQL database capabilities.

## Files

- `nosql_analysis.md` - Theoretical analysis of RDBMS limitations, NoSQL benefits, and trade-offs
- `mongodb_operations.js` - MongoDB operations including queries, aggregations, and updates
- `products_catalog.json` - Sample product catalog data with nested structures
- `README.md` - This file

## Setup Instructions

### 1. Install MongoDB

```bash
# macOS
brew install mongodb-community

# Or download from https://www.mongodb.com/try/download/community
```

### 2. Start MongoDB Service

```bash
# macOS with Homebrew
brew services start mongodb-community

# Or run directly
mongod --dbpath /path/to/data/directory
```

### 3. Load Data

```bash
# Import products catalog
mongoimport --db fleximart_catalog --collection products --file products_catalog.json --jsonArray
```

### 4. Run MongoDB Operations

```bash
# Using mongosh (MongoDB Shell)
mongosh
use fleximart_catalog
load("mongodb_operations.js")

# Or run individual operations
mongosh fleximart_catalog mongodb_operations.js
```

## Operations Included

1. **Load Data** - Import product catalog JSON into MongoDB collection
2. **Basic Query** - Find Electronics products with price < ₹50,000
3. **Review Analysis** - Aggregate to find products with average rating >= 4.0
4. **Update Operation** - Add a new review to a product
5. **Complex Aggregation** - Calculate average price by category

## Key Concepts Demonstrated

- **Flexible Schema** - Products with different attributes in the same collection
- **Embedded Documents** - Reviews stored within product documents
- **Aggregation Pipeline** - Complex data analysis using MongoDB aggregation framework
- **Array Operations** - Working with nested arrays (reviews, tags)

## Analysis Sections

The `nosql_analysis.md` file covers:
- **Section A**: Limitations of RDBMS for diverse product catalogs
- **Section B**: How MongoDB solves these problems
- **Section C**: Trade-offs and disadvantages of MongoDB
