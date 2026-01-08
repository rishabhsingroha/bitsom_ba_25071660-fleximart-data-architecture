# NoSQL Database Analysis for FlexiMart Product Catalog

## Section A: Limitations of RDBMS (150 words)

Relational databases face significant challenges when managing FlexiMart's diverse product catalog. Products have vastly different attributes: laptops require specifications like RAM, processor, and storage capacity, while shoes need size, color, and material information. In a relational model, this would require either creating separate tables for each product type (leading to schema proliferation) or using a sparse table with many nullable columns (wasting storage and complicating queries).

Frequent schema changes become problematic when adding new product categories. Each new product type with unique attributes requires ALTER TABLE statements, which can lock tables and disrupt operations. For instance, adding a "Home Appliances" category with attributes like "wattage" and "energy_rating" would require modifying the products table structure, potentially affecting existing queries and applications.

Storing customer reviews as nested data is particularly challenging. Reviews contain arrays of ratings, comments, and dates that don't fit naturally into normalized tables. While possible through junction tables, this creates complex joins and makes it difficult to query products with their reviews efficiently. The relational model forces a separation between products and reviews that doesn't match the natural data structure.

## Section B: NoSQL Benefits (150 words)

MongoDB's flexible document structure elegantly solves these problems. Each product can be stored as a self-contained document with its own schema, allowing laptops to have "ram" and "processor" fields while shoes have "size" and "color" fields, all within the same collection. This schema flexibility means adding new product types requires no database migrations—simply insert documents with new attribute structures.

Embedded documents enable storing reviews directly within product documents as arrays. This denormalization improves read performance since fetching a product automatically includes its reviews in a single query, eliminating complex joins. The nested structure matches how applications typically consume this data, making development more intuitive.

Horizontal scalability addresses growth challenges. MongoDB's sharding capabilities allow distributing the product catalog across multiple servers as data volume increases, something that's more complex with traditional relational databases. This makes MongoDB ideal for e-commerce platforms expecting rapid growth in product inventory and customer reviews.

## Section C: Trade-offs (100 words)

Two key disadvantages of MongoDB compared to MySQL for this catalog: First, MongoDB lacks ACID transactions across multiple documents, making it challenging to maintain referential integrity between products, orders, and inventory. Complex operations requiring consistency across collections are more difficult to implement reliably.

Second, MongoDB's flexible schema can become a liability without strict application-level validation. Inconsistent data structures across documents can complicate querying and reporting. Unlike MySQL's schema enforcement, MongoDB relies on application code to maintain data consistency, increasing the risk of data quality issues if developers aren't disciplined about validation.
