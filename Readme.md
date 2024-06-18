# Library API

This repository contains a simple API for managing books in a library system. It allows library staff to track and update the status of books, including whether they are borrowed, who borrowed them, and when.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/library-api.git
   cd library-api
   ```

2. Create a `.env` file in the project root and define your environment variables:

   ```plaintext
   SQLALCHEMY_DATABASE_URL=sqlite:///./app/library.db
   ```

   Replace `sqlite:///./app/library.db` with your desired database URL if using a different database system.

3. Build and run the Docker container:

   ```bash
   docker-compose up --build
   ```

4. The FastAPI application will be accessible at `http://localhost:8000`.

## License

[MIT License](LICENSE)
