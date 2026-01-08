// FlexiMart MongoDB Operations
// Database: fleximart_catalog
// Collection: products

// ============================================================================
// Operation 1: Load Data
// ============================================================================
// Import the provided JSON file into collection 'products'
//
// IMPORTANT: Before running other operations, you must first import the data:
// 
// Using mongoimport command line tool:
//   mongoimport --db fleximart_catalog --collection products --file products_catalog.json --jsonArray
//
// Or using mongosh:
//   1. Start mongosh: mongosh
//   2. Switch to database: use fleximart_catalog
//   3. Load the file (if using mongosh file execution)
//
// The products_catalog.json file contains an array of product documents.
// Each document has: product_id, name, category, price, stock, specifications, reviews, tags, etc.

use('fleximart_catalog');

// Verify data was loaded
const productCount = db.products.countDocuments();
print(`Operation 1: ${productCount} products loaded into 'products' collection`);


// ============================================================================
// Operation 2: Basic Query
// ============================================================================
// Find all products in "Electronics" category with price less than 50000
// Return only: name, price, stock

db.products.find(
    { 
        category: "Electronics",
        price: { $lt: 50000 }
    },
    {
        _id: 0,
        name: 1,
        price: 1,
        stock: 1
    }
).pretty();

print("\nOperation 2: Found Electronics products with price < 50000");


// ============================================================================
// Operation 3: Review Analysis
// ============================================================================
// Find all products that have average rating >= 4.0
// Use aggregation to calculate average from reviews array

db.products.aggregate([
    {
        $project: {
            product_id: 1,
            name: 1,
            category: 1,
            avg_rating: {
                $avg: "$reviews.rating"
            },
            review_count: {
                $size: { $ifNull: ["$reviews", []] }
            }
        }
    },
    {
        $match: {
            avg_rating: { $gte: 4.0 },
            review_count: { $gt: 0 }
        }
    },
    {
        $project: {
            _id: 0,
            product_id: 1,
            name: 1,
            category: 1,
            avg_rating: { $round: ["$avg_rating", 2] },
            review_count: 1
        }
    }
]).pretty();

print("\nOperation 3: Products with average rating >= 4.0");


// ============================================================================
// Operation 4: Update Operation
// ============================================================================
// Add a new review to product "ELEC001"
// Review: {user: "U999", rating: 4, comment: "Good value", date: ISODate()}

db.products.updateOne(
    { product_id: "ELEC001" },
    {
        $push: {
            reviews: {
                user_id: "U999",
                username: "NewUser",
                rating: 4,
                comment: "Good value",
                date: new Date().toISOString().split('T')[0]
            }
        }
    }
);

// Verify the update
db.products.findOne(
    { product_id: "ELEC001" },
    { _id: 0, product_id: 1, name: 1, reviews: 1 }
).pretty();

print("\nOperation 4: Added new review to ELEC001");


// ============================================================================
// Operation 5: Complex Aggregation
// ============================================================================
// Calculate average price by category
// Return: category, avg_price, product_count
// Sort by avg_price descending

db.products.aggregate([
    {
        $group: {
            _id: "$category",
            avg_price: { $avg: "$price" },
            product_count: { $sum: 1 }
        }
    },
    {
        $project: {
            _id: 0,
            category: "$_id",
            avg_price: { $round: ["$avg_price", 2] },
            product_count: 1
        }
    },
    {
        $sort: { avg_price: -1 }
    }
]).pretty();

print("\nOperation 5: Average price by category (sorted descending)");
