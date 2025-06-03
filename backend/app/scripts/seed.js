db = db.getSiblingDB('CA-norm-DB');

// Create a unique index on the username field
db.users.createIndex({ "username": 1 }, { unique: true });

// Check if admin user exists
if (!db.users.findOne({ "username": "admin" })) {
    db.users.insertOne({
        "email": "admin@example.com",
        "hashed_password": "$2b$12$XLM8xpy5U1M9k7n8JiRJaeFv4bxQqz5TS1edn8Pxwi1YzVbyzUYmC",
        "active": true,
        "role": "admin",
        "username": "admin"
    });
    print("Admin user 'admin' created successfully.");
} else {
    print("Admin user 'admin' already exists.");
}